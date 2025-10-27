#!/usr/bin/python
# Classification (U)

"""Program:  mail_2_rmq.py

    Description:  Process an email message and send it to the proper
        RabbitMQ queue.

    Usage:
        -M option:
        email_alias: "| /path/mail_2_rmq.py -c file -d path -M"
        cat email_file | /path/mail_2_rmq.py -c file -d path -M

        -C option:
        mail_2_rmq.py -c file -d path -C {file* file1 file2 ...}

        Other options:
            mail_2_rmq.py [ -v | -h ]

    Arguments:
        -c file => RabbitMQ configuration file.
        -d dir path => Directory path for -c option.

        -M => Receive email messages from a pipe.

        -C file(s) => Name(s) of the email files to read.  Can also use
            wildcard expansion for file names.

        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -M and -C are XOR options.

        WARNING: If sending a text attachment, it must be encoded when it is
            emailed.

    Notes:
        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).

            # RabbitMQ Configuration file
            user = "USER"
            japd = "PSWORD"
            host = "IP_ADDRESS"
            host_list = []
            exchange_name = "EXCHANGE_NAME"
            valid_queues = ["QueueName1", "QueueName2"]
            file_queues = ["FileQueueName1", "FileQueueName2"]
            err_queue = "ERROR_QUEUE_NAME"
            err_file_queues = "ERROR_FILE_QUEUE_NAME"
            email_dir = "DIRECTORY_PATH/email_dir"
            log_file = "DIRECTORY_PATH/mail_2_rmq.log"
            queue_dict = {}
            err_addr_queue = "ERROR_ADDR_QUEUE_NAME"
            # For Debugging use
            debug_address = "debug_name@domain"
            debug_valid_queues = ["DebugQueue"]
            debug_queue_dict = {"debug_name@domain": "DebugQueue"}

            # Only change these entries if neccessary.
            attach_types
            subj_filter
            port
            exchange_type
            x_durable
            q_durable
            auto_delete
            heartbeat
            tmp_dir

        Note:  If connecting to a multiple node RabbitMQ cluster, use the
            host_list entry.

    Example:
        alias: "| /opt/local/mail_2_rmq.py -M -c rabbitmq -d /opt/local/config"
        cat email_file | mail_2_rmq.py -c rabbitmq -d config -M
        mail_2_rmq.py -c rabbitmq -d config -C /opt/mail/email*.eml

"""

# Libraries and Global Variables

# Standard
import sys
import os
import datetime
import re
import base64
import io
from email.parser import Parser

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .rabbit_lib import rabbitmq_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import rabbit_lib.rabbitmq_class as rabbitmq_class  # pylint:disable=R0402
    import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def load_cfg(cfg_name, cfg_dir):

    """Function:  load_cfg

    Description:  Load the RabbitMQ configuration file and validate the
        contents of the file.

    Arguments:
        (input) cfg_name -> Configuration file name
        (input) cfg_dir -> Directory path to the configuration file
        (output) cfg -> Configuration module handler
        (output) status_flag -> True|False - successfully validate config file
        (output) combined_msg -> List of error messages detected

    """

    status_flag = True
    combined_msg = []
    cfg = gen_libs.load_module(cfg_name, cfg_dir)
    status, err_msg = gen_libs.chk_crt_dir(
        cfg.email_dir, write=True, read=True)

    if not status:
        status_flag = status
        combined_msg.append(err_msg)

    status, err_msg = gen_libs.chk_crt_dir(
        os.path.dirname(cfg.log_file), write=True, read=True)

    if not status:
        status_flag = status
        combined_msg.append(err_msg)

    status, err_msg = gen_libs.chk_crt_dir(cfg.tmp_dir, write=True, read=True)

    if not status:
        status_flag = status
        combined_msg.append(err_msg)

    return cfg, status_flag, combined_msg


def archive_email(rmq, log, cfg, msg):

    """Function:  archive_email

    Description:  Save an email to file in an archive directory.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) msg -> Email message instance

    """

    e_file = rmq.exchange + "-" + rmq.queue_name + "-" \
        + datetime.datetime.strftime(
            datetime.datetime.now(), "%Y%m%d-%H%M%S") \
        + f".{os.getpid()}.email.txt"
    f_file = os.path.join(cfg.email_dir, e_file)
    log.log_info(f"[{os.getpid()}] Saving email to: {f_file}")
    gen_libs.write_file(f_file, "w", msg)
    log.log_info(f"[{os.getpid()}] Email saved to: {e_file}")


def get_text(msg):

    """Function:  get_text

    Description:  Walks the tree of a email and returns the text of the email.

    Arguments:
        (input) msg -> Email message instance
        (output) All texts in email joined together in a single string

    """

    msg_list = []

    for part in msg.walk():
        if part.get_content_maintype() == "multipart" \
           or not part.get_payload(decode=True):
            continue

        if part.get_content_type() == "text/plain":
            data = part.get_payload(decode=True)

            if not isinstance(data, str):
                data = data.decode("UTF-8")

            msg_list.append(data)

    return "".join(msg_list)


def connect_process(rmq, log, cfg, msg, **kwargs):

    """Function:  connect_process

    Description:  Publish email message to RabbitMQ.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) msg -> Email message instance
        (input) kwargs:
            fname -> File name of email/attachment

    """

    fname = kwargs.get("fname", None)

    # Process email or file/attachment.
    if fname:
        log.log_info(f"[{os.getpid()}] Processing file/attachment...")

        with open(fname, mode="r", encoding="UTF-8") as f_hldr:
            t_msg = f_hldr.read()

        bname = os.path.splitext(os.path.basename(fname))[0]
        t_msg = str({"AFilename": bname, "File": t_msg})

    elif rmq.queue_name == cfg.err_queue:
        log.log_info(f"[{os.getpid()}] Processing error message...")
        t_msg = "From: " + msg["from"] + " To: " + msg["to"] \
                + " Subject: " + msg["subject"] + " Body: " \
                + (get_text(msg) or "")

    else:
        log.log_info(f"[{os.getpid()}] Processing email body...")
        t_msg = get_text(msg)

    if t_msg and rmq.publish_msg(t_msg):
        log.log_info(f"[{os.getpid()}] Message ingested into RabbitMQ")

    else:
        log.log_err(f"[{os.getpid()}] Failed to injest message into RabbitMQ")
        archive_email(rmq, log, cfg, msg)


def filter_subject(subj, cfg):

    """Function:  filter_subject

    Description:  Filter out strings from the message subject line.

    Arguments:
        (input) subj -> Message subject line
        (input) cfg -> Configuration settings module for the program
        (output) subj -> Filtered message subject line

    """

    return re.sub(cfg.subj_filter, "", subj).strip()


def convert_bytes(data):

    """Function:  convert_bytes

    Description:  Converts a string to bytes.

    Arguments:
        (input) data -> Data string
        (output) -> Bytes or None

    """

    if isinstance(data, bytes):
        return data

    if isinstance(data, str):
        return data.encode()

    return None


def process_attach(msg, log, cfg):

    """Function:  process_attach

    Description:  Locate, extract, and process attachment from email based on
        specified attachment types.

    Arguments:
        (input) msg -> Email message instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (output) fname -> Name of encoded attachment file

    """

    fname_list = []
    log.log_info(f"[{os.getpid()}] Locating attachments...")

    if not msg.is_multipart():
        return fname_list

    for item in msg.walk():

        if item.get_content_type() in cfg.attach_types \
           and item.get_filename():
            tname = os.path.join(cfg.tmp_dir, item.get_filename())
            log.log_info(
                f"[{os.getpid()}] Attachment detected: {item.get_filename()}")
            log.log_info(
                f"[{os.getpid()}] Attachment type: {item.get_content_type()}")
            data = convert_bytes(item.get_payload(decode=True))

            if data is None:
                log.log_warn(
                    f"[{os.getpid()}] Unable to convert attach to bytes")
                continue

            with io.open(tname, mode="wb") as fhdr:
                fhdr.write(data)

            fname = tname + ".encoded"
            fname_list.append(fname)
            in_file = io.open(tname, mode="rb")     # pylint:disable=R1732
            out_file = io.open(fname, mode="wb")    # pylint:disable=R1732
            base64.encode(in_file, out_file)
            in_file.close()
            out_file.close()
            err_flag, err_msg = gen_libs.rm_file(tname)

            if err_flag:
                log.log_warn(
                    f"[{os.getpid()}] process_attach:  Message: {err_msg}")

        elif item.get_filename():
            log.log_warn(
                f"[{os.getpid()}] Invalid attachment detected:"
                f" {item.get_filename()}")
            log.log_warn(
                f"[{os.getpid()}] Attachment type: {item.get_content_type()}")

    return fname_list


def process_from(cfg, log, msg, from_addr):

    """Function:  process_from

    Description:  Process email using its From line.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) msg -> Email message body
        (input) from_addr -> Email From line

    """

    fname_list = process_attach(msg, log, cfg)

    if fname_list:
        for fname in fname_list:
            log.log_info(
                f"[{os.getpid()}] Valid From address:"
                f" {from_addr} with file attachment: {fname}")
            pub_to_rmq(
                cfg, log, cfg.queue_dict[from_addr], cfg.queue_dict[from_addr],
                msg, fname=fname)

    else:
        log.log_warn(
            f"[{os.getpid()}] Missing attachment for email address:"
            f" {from_addr}")
        connect_rmq(cfg, log, cfg.err_addr_queue, cfg.err_addr_queue, msg)


def connect_rmq(cfg, log, qname, rkey, msg, **kwargs):

    """Function:  connect_rmq

    Description:  Set up and connect to RabbitMQ, check for connection
        problems.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) qname -> Queue name for RabbitMQ
        (input) rkey -> Rkey value for RabbitMQ
        (input) msg -> Message body
        (input) kwargs:
            fname -> Name of attachment file

    """

    config = {"fname": kwargs.get("fname")} if kwargs.get("fname", False) \
        else {}
    rmq = rabbitmq_class.create_rmqpub(cfg, qname, rkey)
    log.log_info(
        f"[{os.getpid()}] connect_rmq: Connection info:"
        f" {cfg.host}->{cfg.exchange_name}")
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        log.log_info(
            f"[{os.getpid()}] connect_rmq: Connected to RabbitMQ mode")
        connect_process(rmq, log, cfg, msg, **config)

    else:
        log.log_err(
            f"[{os.getpid()}] connect_rmq: Failed to connect to RabbitMQ")
        log.log_err(f"[{os.getpid()}] connect_rmq: Message:  {err_msg}")
        archive_email(rmq, log, cfg, msg)

    if connect_status:
        rmq.close()


def pub_to_rmq(cfg, log, qname, rkey, msg, **kwargs):

    """Function:  pub_to_rmq

    Description:  Consolidate arguments for the call to RMQ and clean up file.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) qname -> Queue name for RabbitMQ
        (input) rkey -> Rkey value for RabbitMQ
        (input) msg -> Email message body
        (input) kwargs:
            fname -> Name of attachment file

    """

    fname = kwargs.get("fname")
    log.log_info(f"[{os.getpid()}] pub_to_rmq: Publishing: {fname}")
    connect_rmq(cfg, log, qname, rkey, msg, fname=fname)
    err_flag, err_msg = gen_libs.rm_file(fname)

    if err_flag:
        log.log_warn(f"[{os.getpid()}] pub_to_rmq: Message: {err_msg}")


def process_file(cfg, log, subj, msg):

    """Function:  process_file

    Description:  Process email with a file attachment or process as an invalid
        message.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) subj -> Email subject line
        (input) msg -> Email message body

    """

    fname_list = process_attach(msg, log, cfg)

    if fname_list and subj in cfg.file_queues:
        for fname in fname_list:
            log.log_info(
                f"[{os.getpid()}] Valid subject with file attachment: {fname}")
            pub_to_rmq(cfg, log, subj, subj, msg, fname=fname)

    elif fname_list:
        for fname in fname_list:
            log.log_info(
                f"[{os.getpid()}] Invalid subject with file attached: {fname}")
            pub_to_rmq(
                cfg, log, cfg.err_file_queue, cfg.err_file_queue, msg,
                fname=fname)

    else:
        log.log_warn(f"[{os.getpid()}] Invalid email subject: {subj}")
        connect_rmq(cfg, log, cfg.err_queue, cfg.err_queue, msg)


def archive_email_debug(rmq, log, cfg, msg):

    """Function:  archive_email_debug

    Description:  Save an email to file in an archive directory.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) msg -> Email message instance

    """

    log.log_debug(f"[{os.getpid()}] Start of archive_email_debug")
    e_file = rmq.exchange + "-" + rmq.queue_name + "-" \
        + datetime.datetime.strftime(
            datetime.datetime.now(), "%Y%m%d-%H%M%S") \
        + f".{os.getpid()}.email.txt"
    log.log_debug(f"[{os.getpid()}] e_file: {e_file}")
    f_file = os.path.join(cfg.email_dir, e_file)
    log.log_debug(f"[{os.getpid()}] f_file: {f_file}")
    log.log_info(f"[{os.getpid()}] Saving email to: {f_file}")
    gen_libs.write_file(f_file, "w", msg)
    log.log_info(f"[{os.getpid()}] Email saved to: {e_file}")
    log.log_debug(f"[{os.getpid()}] End of archive_email_debug")


def get_text_debug(msg, log):

    """Function:  get_text_debug

    Description:  Walks the tree of a email and returns the text of the email.

    Arguments:
        (input) msg -> Email message instance
        (input) log -> Log class instance
        (output) All texts in email joined together in a single string

    """

    log.log_debug(f"[{os.getpid()}] Start of get_text_debug")
    msg_list = []

    for part in msg.walk():
        log.log_debug(f"[{os.getpid()}] get_text: Top of msg.walk loop")

        if part.get_content_maintype() == "multipart" \
           or not part.get_payload(decode=True):
            log.log_debug(f"[{os.getpid()}] Multipart or no payload detected")
            log.log_debug(f"[{os.getpid()}] Continue to next iteration")
            continue

        if part.get_content_type() == "text/plain":
            log.log_debug(f"[{os.getpid()}] Content type is text/plain")
            log.log_debug(f"[{os.getpid()}] Get payload")
            data = part.get_payload(decode=True)
            log.log_debug(f"[{os.getpid()}] Got payload")

            if not isinstance(data, str):
                log.log_debug(f"[{os.getpid()}] Data is not a string")
                log.log_debug(f"[{os.getpid()}] Start decode on data")
                data = data.decode("UTF-8")
                log.log_debug(f"[{os.getpid()}] Finish decode on data")

            log.log_debug(f"[{os.getpid()}] Appending data to list")
            msg_list.append(data)

        log.log_debug(f"[{os.getpid()}] get_text: Bottom of msg.walk loop")

    log.log_debug(f"[{os.getpid()}] End of get_text_debug")
    log.log_debug(f"[{os.getpid()}] Joining msg_list together for return")

    return "".join(msg_list)


def connect_process_debug(rmq, log, cfg, msg, **kwargs):

    """Function:  connect_process_debug

    Description:  Publish email message to RabbitMQ.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) msg -> Email message instance
        (input) kwargs:
            fname -> File name of email/attachment

    """

    log.log_debug(f"[{os.getpid()}] Start of connect_process_debug")
    fname = kwargs.get("fname", None)

    # Process email or file/attachment.
    if fname:
        log.log_info(f"[{os.getpid()}] Processing file/attachment...")
        log.log_debug(f"[{os.getpid()}] Open file for reading: {fname}")

        with open(fname, mode="r", encoding="UTF-8") as f_hldr:
            t_msg = f_hldr.read()

        log.log_debug(f"[{os.getpid()}] Finished reading file: {fname}")
        bname = os.path.splitext(os.path.basename(fname))[0]
        log.log_debug(f"[{os.getpid()}] Basename: {bname}")
        t_msg = str({"AFilename": bname, "File": t_msg})
        log.log_debug(f"[{os.getpid()}] Created t_msg for queue")

    elif rmq.queue_name == cfg.err_queue:
        log.log_debug(f"[{os.getpid()}] Queue name detected is error queue")
        log.log_debug(f"[{os.getpid()}] RMQ Queue: {rmq.queue_name}")
        log.log_debug(f"[{os.getpid()}] CFG Queue: {cfg.err_queue}")
        log.log_info(f"[{os.getpid()}] Processing error message...")
        log.log_debug(f"[{os.getpid()}] Calling get_text_debug")
        t_msg = "From: " + msg["from"] + " To: " + msg["to"] \
                + " Subject: " + msg["subject"] + " Body: " \
                + (get_text_debug(msg, log) or "")
        log.log_debug(f"[{os.getpid()}] Finished get_text_debug")

    else:
        log.log_info(f"[{os.getpid()}] Processing email body...")
        log.log_debug(f"[{os.getpid()}] Calling get_text_debug2")
        t_msg = get_text_debug(msg, log)
        log.log_debug(f"[{os.getpid()}] Finished get_text_debug2")

    log.log_debug(f"[{os.getpid()}] Process message if t_msg is detected")

    if t_msg and rmq.publish_msg(t_msg):
        log.log_info(f"[{os.getpid()}] Message ingested into RabbitMQ")

    else:
        log.log_debug(f"[{os.getpid()}] t_msg not detected or publish failed")
        log.log_err(f"[{os.getpid()}] Failed to injest message into RabbitMQ")
        log.log_debug(
            f"[{os.getpid()}] connect_process: Calling archive_email_debug")
        archive_email_debug(rmq, log, cfg, msg)
        log.log_debug(
            f"[{os.getpid()}] connect_process: Finished archive_email_debug")

    log.log_debug(f"[{os.getpid()}] End of connect_process_debug")


def connect_rmq_debug(cfg, log, qname, rkey, msg, **kwargs):

    """Function:  connect_rmq_debug

    Description:  Set up and connect to RabbitMQ, check for connection
        problems.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) qname -> Queue name for RabbitMQ
        (input) rkey -> Rkey value for RabbitMQ
        (input) msg -> Message body
        (input) kwargs:
            fname -> Name of attachment file

    """

    log.log_debug(f"[{os.getpid()}] Start of connect_rmq_debug")
    config = {"fname": kwargs.get("fname")} if kwargs.get("fname", False) \
        else {}
    log.log_debug(f"[{os.getpid()}] Value for config: {config}")
    log.log_debug(f"[{os.getpid()}] Creating RMQ Pub instance")
    rmq = rabbitmq_class.create_rmqpub(cfg, qname, rkey)
    log.log_info(
        f"[{os.getpid()}] connect_rmq: Connection info:"
        f" {cfg.host}->{cfg.exchange_name}")
    log.log_debug(f"[{os.getpid()}] Creating RMQ connection")
    connect_status, err_msg = rmq.create_connection()
    log.log_debug(f"[{os.getpid()}] Created RMQ connection")

    if connect_status and rmq.channel.is_open:
        log.log_info(
            f"[{os.getpid()}] connect_rmq: Connected to RabbitMQ mode")
        log.log_debug(f"[{os.getpid()}] Calling connect_process_debug")
        connect_process_debug(rmq, log, cfg, msg, **config)
        log.log_debug(f"[{os.getpid()}] Finished connect_process_debug")

    else:
        log.log_err(
            f"[{os.getpid()}] connect_rmq: Failed to connect to RabbitMQ")
        log.log_err(f"[{os.getpid()}] connect_rmq: Message:  {err_msg}")
        log.log_debug(
            f"[{os.getpid()}] connect_rmq: Calling archive_email_debug")
        archive_email_debug(rmq, log, cfg, msg)
        log.log_debug(
            f"[{os.getpid()}] connect_rmq: Finished archive_email_debug")

    if connect_status:
        log.log_debug(f"[{os.getpid()}] Closing RMQ connection")
        rmq.close()

    log.log_debug(f"[{os.getpid()}] End of connect_rmq_debug")


def process_attach_debug(msg, log, cfg):                # pylint:disable=R0915

    """Function:  process_attach_debug

    Description:  Locate, extract, and process attachment from email based on
        specified attachment types.

    Arguments:
        (input) msg -> Email message instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (output) fname -> Name of encoded attachment file

    """

    log.log_debug(f"[{os.getpid()}] Start of process_attach_debug")
    fname_list = []
    log.log_info(f"[{os.getpid()}] Locating attachments...")

    if not msg.is_multipart():
        log.log_debug(f"[{os.getpid()}] Multipart not detected")
        log.log_debug(f"[{os.getpid()}] End of process_attach_debug")
        return fname_list

    log.log_debug(f"[{os.getpid()}] Multipart is detected")

    for item in msg.walk():
        log.log_debug(
            f"[{os.getpid()}] process_attach: Top of msg.walk loop")

        if item.get_content_type() in cfg.attach_types \
           and item.get_filename():

            log.log_debug(f"[{os.getpid()}] Detected attachment and file")
            tname = os.path.join(cfg.tmp_dir, item.get_filename())
            log.log_info(
                f"[{os.getpid()}] Attachment detected: {item.get_filename()}")
            log.log_info(
                f"[{os.getpid()}] Attachment type: {item.get_content_type()}")

            # Change 2253.
            ####################
            log.log_debug(f"[{os.getpid()}] Calling gen_libs.convert_bytes")
            data = gen_libs.convert_bytes(item.get_payload(decode=True))
            log.log_debug(f"[{os.getpid()}] Finished gen_libs.convert_bytes")
            ####################

            log.log_debug(f"[{os.getpid()}] Check if data was converted")
            if data is None:
                log.log_warn(
                    f"[{os.getpid()}] Unable to convert attach to bytes")
                log.log_debug(f"[{os.getpid()}] Continue to next loop")
                continue

            log.log_debug(f"[{os.getpid()}] Start writing to: {tname}")
            with io.open(tname, mode="wb") as fhdr:
                fhdr.write(data)
            log.log_debug(f"[{os.getpid()}] Closed writing to: {tname}")

            log.log_debug(f"[{os.getpid()}] Creating fname variable")
            fname = tname + ".encoded"
            fname_list.append(fname)
            log.log_debug(f"[{os.getpid()}] Added {fname} to {fname_list}")

            log.log_debug(f"[{os.getpid()}] Start of reading from {tname}")
            in_file = io.open(tname, mode="rb")         # pylint:disable=R1732
            log.log_debug(f"[{os.getpid()}] Start writing to 2: {fname}")
            out_file = io.open(fname, mode="wb")        # pylint:disable=R1732

            log.log_debug(f"[{os.getpid()}] Base64 encoding data to file")
            base64.encode(in_file, out_file)

            in_file.close()
            log.log_debug(f"[{os.getpid()}] Closed reading from {tname}")
            out_file.close()
            log.log_debug(f"[{os.getpid()}] Closed writing to 2: {fname}")

            log.log_debug(
                f"[{os.getpid()}] process_attach: Removing file: {tname}")
            err_flag, err_msg = gen_libs.rm_file(tname)
            log.log_debug(
                f"[{os.getpid()}] process_attach: Removed file {tname}")

            if err_flag:
                log.log_debug(
                    f"[{os.getpid()}] process_attach: File {tname}, Perms:"
                    f" {oct(os.stat(tname).st_mode)[-3:]}")
                log.log_debug(
                    f"[{os.getpid()}] File Owner: {os.stat(tname).st_uid}")
                log.log_warn(
                    f"[{os.getpid()}] process_attach:  Message: {err_msg}")

        elif item.get_filename():
            log.log_debug(f"[{os.getpid()}] Detected filename in msg only")
            log.log_warn(
                f"[{os.getpid()}] Invalid attachment detected:"
                f" {item.get_filename()}")
            log.log_warn(
                f"[{os.getpid()}] Attachment type: {item.get_content_type()}")

        log.log_debug(
            f"[{os.getpid()}] process_attach: Bottom of msg.walk loop")

    log.log_debug(f"[{os.getpid()}] End of process_attach_debug")

    return fname_list


def process_from_debug(cfg, log, msg, from_addr):

    """Function:  process_from_debug

    Description:  Process email using its From line.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) msg -> Email message body
        (input) from_addr -> Email From line

    """

    log.log_debug(f"[{os.getpid()}] Start of process_from_debug")
    log.log_debug(
        f"[{os.getpid()}] process_from: Calling process_attach_debug")
    fname_list = process_attach_debug(msg, log, cfg)
    log.log_debug(
        f"[{os.getpid()}] process_from: Finished process_attach_debug")

    if fname_list:
        log.log_debug(f"[{os.getpid()}] Detected fname_list: {fname_list}")

        for fname in fname_list:
            log.log_debug(
                f"[{os.getpid()}] process_from: Top of fname_list loop")
            log.log_info(
                f"[{os.getpid()}] Valid From address:"
                f" {from_addr} with file attachment: {fname}")
            log.log_debug(
                f"[{os.getpid()}] process_from: Calling pub_to_rmq_debug")
            pub_to_rmq_debug(
                cfg, log, cfg.debug_queue_dict[from_addr],
                cfg.debug_queue_dict[from_addr], msg, fname)
            log.log_debug(
                f"[{os.getpid()}] process_from: Finished pub_to_rmq_debug")
            log.log_debug(
                f"[{os.getpid()}] process_from: Bottom of fname_list loop")

    else:
        log.log_debug(f"[{os.getpid()}] No fname_list detected")
        log.log_warn(
            f"[{os.getpid()}] Missing attachment for email address:"
            f" {from_addr}")
        log.log_debug(
            f"[{os.getpid()}] process_from: Calling connect_rmq_debug: error")
        connect_rmq_debug(
            cfg, log, cfg.err_addr_queue, cfg.err_addr_queue, msg)
        log.log_debug(
            f"[{os.getpid()}] process_from: Finished connect_rmq_debug: error")

    log.log_debug(f"[{os.getpid()}] End of process_from_debug")


def pub_to_rmq_debug(                           # pylint:disable=R0913,R0917
        cfg, log, qname, rkey, msg, fname):

    """Function:  pub_to_rmq_debug

    Description:  Consolidate arguments for the call to RMQ and clean up file.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) qname -> Queue name for RabbitMQ
        (input) rkey -> Rkey value for RabbitMQ
        (input) msg -> Email message body
        (input) fname -> Name of attachment file

    """

    log.log_debug(f"[{os.getpid()}] pub_to_rmq: Calling connect_rmq_debug")
    connect_rmq_debug(cfg, log, qname, rkey, msg, fname=fname)
    log.log_debug(f"[{os.getpid()}] pub_to_rmq: Finished connect_rmq_debug")
    log.log_debug(f"[{os.getpid()}] pub_to_rmq: Removing file: {fname}")
    err_flag, err_msg = gen_libs.rm_file(fname)
    log.log_debug(f"[{os.getpid()}] pub_to_rmq: Removed file {fname}")

    if err_flag:
        log.log_debug(
            f"[{os.getpid()}] pub_to_rmq: File {fname}, Perms:"
            f" {oct(os.stat(fname).st_mode)[-3:]}")
        log.log_debug(
            f"[{os.getpid()}] pub_to_rmq: File Owner:"
            f" {os.stat(fname).st_uid}")
        log.log_warn(f"[{os.getpid()}] pub_to_rmq: Message: {err_msg}")


def process_file_debug(cfg, log, subj, msg):

    """Function:  process_file_debug

    Description:  Process email with a file attachment or process as an invalid
        message.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) subj -> Email subject line
        (input) msg -> Email message body

    """

    log.log_debug(f"[{os.getpid()}] Start of process_file_debug")
    log.log_debug(
        f"[{os.getpid()}] process_file: Calling process_attach_debug")
    fname_list = process_attach_debug(msg, log, cfg)
    log.log_debug(
        f"[{os.getpid()}] process_file: Finished process_attach_debug")

    if fname_list and subj in cfg.file_queues:
        log.log_debug(f"[{os.getpid()}] Found {subj} in {cfg.file_queues}")
        log.log_debug(f"[{os.getpid()}] Detected list: {fname_list}")

        for fname in fname_list:
            log.log_debug(
                f"[{os.getpid()}] process_file: Top of fname_list loop")
            log.log_info(
                f"[{os.getpid()}] Valid subject with file attachment: {fname}")
            log.log_debug(
                f"[{os.getpid()}] process_file: Calling pub_to_rmq_debug")
            pub_to_rmq_debug(cfg, log, subj, subj, msg, fname)
            log.log_debug(
                f"[{os.getpid()}] process_file: Finished pub_to_rmq_debug")
            log.log_debug(
                f"[{os.getpid()}] process_file: Bottom of fname_list loop")

    elif fname_list:
        log.log_debug(f"[{os.getpid()}] Only detected fname_list")
        log.log_debug(f"[{os.getpid()}] Detected list 2: {fname_list}")

        for fname in fname_list:
            log.log_debug(f"[{os.getpid()}] Top of fname_list second loop")
            log.log_info(
                f"[{os.getpid()}] Invalid subject with file attached: {fname}")
            log.log_debug(
                f"[{os.getpid()}] process_file 2: Calling pub_to_rmq_debug")
            pub_to_rmq_debug(
                cfg, log, cfg.err_file_queue, cfg.err_file_queue, msg, fname)
            log.log_debug(
                f"[{os.getpid()}] process_file 2: Finished pub_to_rmq_debug")
            log.log_debug(f"[{os.getpid()}] Bottom of fname_list second loop")

    else:
        log.log_debug(f"[{os.getpid()}] No fname_list or subject detected")
        log.log_warn(f"[{os.getpid()}] Invalid email subject: {subj}")
        log.log_debug(
            f"[{os.getpid()}] process_file: Calling connect_rmq_debug: error")
        connect_rmq_debug(cfg, log, cfg.err_queue, cfg.err_queue, msg)
        log.log_debug(
            f"[{os.getpid()}] process_file: Finished connect_rmq_debug: error")

    log.log_debug(f"[{os.getpid()}] End of process_file_debug")


def process_debug(cfg, subj, msg, from_addr):

    """Function:  process_debug

    Description:  Process for debugging.  Will determine whether to process on
        subject, from address or attachment.

    Note: A new log instance will be initiated and all debugging entries will
        be sent to this debug log.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) subj -> Email subject line
        (input) msg -> Email message body
        (input) from_addr -> Email From line

    """

    log_file = os.path.join(
        os.path.dirname(cfg.log_file),
        "debug_" + os.path.basename(cfg.log_file))
    date = "." + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    log = gen_class.Logger(
        log_file, log_file + date, "DEBUG",
        "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
    log.log_info(f"[{os.getpid()}] {'=' * 80}")
    log.log_info(
        f"[{os.getpid()}] {cfg.host}:{cfg.exchange_name} Initialized")
    log.log_debug(f"[{os.getpid()}] Start of debugging")

    if subj in cfg.debug_valid_queues:
        log.log_debug(f"[{os.getpid()}] Detected valid subject: {subj}")
        log.log_info(f"[{os.getpid()}] Valid email subject: {subj}")
        log.log_debug(f"[{os.getpid()}] process: Calling connect_rmq_debug")
        connect_rmq_debug(cfg, log, subj, subj, msg)
        log.log_debug(f"[{os.getpid()}] process: Finished connect_rmq_debug")

    elif from_addr and from_addr in list(cfg.debug_queue_dict.keys()):
        log.log_debug(f"[{os.getpid()}] Detected valid from addr: {from_addr}")
        log.log_debug(f"[{os.getpid()}] Calling process_from_debug")
        process_from_debug(cfg, log, msg, from_addr)
        log.log_debug(f"[{os.getpid()}] Finished process_from_debug")

    else:
        log.log_debug(f"[{os.getpid()}] Processing as all others")
        log.log_debug(f"[{os.getpid()}] Calling process_file_debug")
        process_file_debug(cfg, log, subj, msg)
        log.log_debug(f"[{os.getpid()}] Finished process_file_debug")

    log.log_debug(f"[{os.getpid()}] End of debugging")

    log.log_close()


def read_email(cfg, log, **kwargs):

    """Function:  read_email

    Description:  Reads files and parses the email messages, then sends emails
        for further processing.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) kwargs:
            args -> ArgParser class instance

    """

    log.log_info(f"[{os.getpid()}] Reading and parsing email...")
    args = kwargs.get("args")
    parser = Parser()

    for fname in args.get_val("-C"):
        with open(fname, mode="r", encoding="UTF-8") as fhdr:
            msg = parser.parsestr("".join(fhdr.readlines()))
            process_message(cfg, log, msg=msg)


def capture_email(cfg, log, **kwargs):                  # pylint:disable=W0613

    """Function:  capture_email

    Description:  Captures the email from standard in and parses the email
        message, before sending the email for further processing.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) kwargs:
            args -> ArgParser class instance

    """

    log.log_info(f"[{os.getpid()}] Capturing and parsing email...")
    parser = Parser()
    msg = parser.parsestr("".join(sys.stdin.readlines()))
    process_message(cfg, log, msg=msg)


def process_message(cfg, log, **kwargs):

    """Function:  process_message

    Description:  Parses email message, processes email body or attachment and
        based on subject, from address and/or attachment, send the data to
        queue in RabbitMQ.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) kwargs:
            msg -> Email Parser class instance

    """

    log.log_info(f"[{os.getpid()}] Get email metadata")
    msg = kwargs.get("msg")
    subj = gen_libs.pascalize(filter_subject(msg["subject"], cfg))
    email_list = gen_libs.find_email_addr(msg["from"])
    from_addr = email_list[0] if email_list else None

    if subj in cfg.valid_queues:
        log.log_info(f"[{os.getpid()}] Process subject")
        log.log_info(f"[{os.getpid()}] Valid email subject: {subj}")
        connect_rmq(cfg, log, subj, subj, msg)

    elif from_addr and from_addr in list(cfg.queue_dict.keys()):
        log.log_info(f"[{os.getpid()}] Process from address")
        process_from(cfg, log, msg, from_addr)

    elif from_addr and hasattr(
       cfg, "debug_address") and from_addr == cfg.debug_address:
        log.log_info(f"[{os.getpid()}] Process debug")
        log.log_info(f"[{os.getpid()}] Starting seperate debug log")
        process_debug(cfg, subj, msg, from_addr)
        log.log_info(f"[{os.getpid()}] Closed seperate debug log")

    else:
        log.log_info(f"[{os.getpid()}] Process attachment")
        process_file(cfg, log, subj, msg)


def run_program(args, func_dict):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Create a program lock to prevent other instantiations from running.

    Arguments:
        (input) args -> ArgParser class instance
        (input) func_dict -> Dictionary list of functions and options

    """

    func_dict = dict(func_dict)
    cfg, status_flag, err_msgs = load_cfg(
        args.get_val("-c"), args.get_val("-d"))
    date = "." + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")

    if status_flag:
        log = gen_class.Logger(
            cfg.log_file, cfg.log_file + date, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        log.log_info(f"[{os.getpid()}] {'=' * 80}")
        log.log_info(
            f"[{os.getpid()}] {cfg.host}:{cfg.exchange_name} Initialized")

        # Intersect args_array & func_dict to find which functions to call
        for opt in set(args.get_args_keys()) & set(func_dict.keys()):
            func_dict[opt](cfg, log, args=args)

        log.log_close()

    else:
        print("Error:  Problem(s) in configuration file.")

        for line in err_msgs:
            print(line)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
        file_perm -> File check options with their perms in octal
        func_dict -> dictionary list for the function calls or other options
        multi_val -> List of options that will have multiple values
        opt_req_list -> contains options that are required for the program
        opt_val_list -> contains options which require values
        opt_xor_dict -> contains dict with key that is xor with it's values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
    file_perm = {"-C": 4}
    func_dict = {"-M": capture_email, "-C": read_email}
    multi_val = ["-C"]
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]
    opt_xor_dict = {"-M": ["-C"], "-C": ["-M"]}

    # Process argument list from command line
    args = gen_class.ArgParser(
        sys.argv, opt_val=opt_val_list, multi_val=multi_val)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_xor_dict(opt_xor_val=opt_xor_dict)              \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk)            \
       and args.arg_file_chk(file_perm_chk=file_perm):
        run_program(args, func_dict)


if __name__ == "__main__":
    sys.exit(main())
