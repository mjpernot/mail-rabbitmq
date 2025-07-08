#!/usr/bin/python
# Classification (U)

"""Program:  mail_2_rmq.py

    Description:  Process an email message and send it to the proper
        RabbitMQ queue.

    Usage:
        -M options:
        email_alias: "| /path/mail_2_rmq.py -c file -d path -M"
        cat email_file | /path/mail_2_rmq.py -c file -d path -M

        All other options.
        mail_2_rmq.py -c file -d path [-C]
            [ -v | -h ]

    Arguments:
        -c file => RabbitMQ configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.

        -M => Receive email messages from email pipe.

        -C => Check for non-processed messages in email archive directory.

        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -M and -C are XOR options.

    Notes:
        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).

            # RabbitMQ Configuration file
            user = "USER"
            japd = "PSWORD"
            host = "IP_ADDRESS"
            host_list = []
            exchange_name = "EXCHANGE_NAME"
            valid_queues = ["QueueName1", "QueueName2", ...]
            file_queues = ["FileQueueName1", "FileQueueName2", ...]
            err_queue = "ERROR_QUEUE_NAME"
            err_file_queues = "ERROR_FILE_QUEUE_NAME"
            email_dir = "DIRECTORY_PATH/email_dir"
            log_file = "DIRECTORY_PATH/mail_2_rmq.log"
            tmp_dir = "DIRECTORY_PATH/tmp"

            # Only change these entries if neccessary.
            attach_types
            subj_filter
            port
            exchange_type
            x_durable
            q_durable
            auto_delete
            heartbeat

        Note:  If connecting to a multiple node RabbitMQ cluster, use the
            host_list entry.

    Example:
        alias: "| /opt/local/mail_2_rmq.py -M -c rabbitmq -d /opt/local/config"
        cat email_file | mail_2_rmq.py -c rabbitmq -d config -M
        mail_2_rmq.py -c rabbitmq -d config -C

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


def parse_email():

    """Function:  parse_email

    Description:  Accept email from standard in and process email to be used
        for RabbitMQ.

    Arguments:
        (output) Email instance

    """

    parser = Parser()

    return parser.parsestr("".join(sys.stdin.readlines()))


def archive_email(rmq, log, cfg, msg):

    """Function:  archive_email

    Description:  Save an email to file in an archive directory.

    Arguments:
        (input) rmq -> RabbitMQ class instance
        (input) log -> Log class instance
        (input) cfg -> Configuration settings module for the program
        (input) msg -> Email message instance

    """

#    e_file = rmq.exchange + "-" + rmq.queue_name + "-" \
#        + datetime.datetime.strftime(
#            datetime.datetime.now(), "%Y%m%d-%H%M%S") + ".email.txt"
    e_file = rmq.exchange + "-" + rmq.queue_name + "-" \
        + datetime.datetime.strftime(
            datetime.datetime.now(), "%Y%m%d-%H%M%S") \
            + f".{os.getpid()}.email.txt"
    f_file = os.path.join(cfg.email_dir, e_file)
#    log.log_info(f"Saving email to: {cfg.email_dir + os.path.sep + e_file}")
    log.log_info(f"[{os.getpid()}] Saving email to: {f_file}")
#    gen_libs.write_file(cfg.email_dir + os.path.sep + e_file, "w", msg)
    gen_libs.write_file(f_file, "w", msg)
#    log.log_info(f"Email saved to: {e_file}")
    log.log_info(f"[{os.getpid()}] Email saved to: {e_file}")


def get_text(msg):

    """Function:  get_text

    Description:  Walks the tree of a email and returns the text of the email.

    Arguments:
        (input) msg -> Email message instance
        (output) All texts in email joined together in a single string

    """

    print("DEBUG: get_text")

    msg_list = []

    for part in msg.walk():
        print("DEBUG: msg.walk")

        if part.get_content_maintype() == "multipart" \
           or not part.get_payload(decode=True):
            print("DEBUG: multipart")

            continue

        print("DEBUG:  CONTENT_TYPE:", part.get_content_type())
        if part.get_content_type() == "text/plain":
            data = part.get_payload(decode=True)
            print("DEBUG: get_payload")

            if not isinstance(data, str):
                data = data.decode("UTF-8")
                print("DEBUG: decode")

            msg_list.append(data)
            print("DEBUG: append")

    print("DEBUG:", msg_list)

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
#        log.log_info("Processing file/attachment...")
        log.log_info(f"[{os.getpid()}] Processing file/attachment...")

        with open(fname, mode="r", encoding="UTF-8") as f_hldr:
            t_msg = f_hldr.read()

        bname = os.path.splitext(os.path.basename(fname))[0]
        t_msg = str({"AFilename": bname, "File": t_msg})

    elif rmq.queue_name == cfg.err_queue:
#        log.log_info("Processing error message...")
        log.log_info(f"[{os.getpid()}] Processing error message...")
        t_msg = "From: " + msg["from"] + " To: " + msg["to"] \
                + " Subject: " + msg["subject"] + " Body: " \
                + (get_text(msg) or "")

    else:
#        log.log_info("Processing email body...")
        log.log_info(f"[{os.getpid()}] Processing email body...")
        t_msg = get_text(msg)

    if t_msg and rmq.publish_msg(t_msg):
#        log.log_info("Message ingested into RabbitMQ")
        log.log_info(f"[{os.getpid()}] Message ingested into RabbitMQ")

    else:
#        log.log_err("Failed to injest message into RabbitMQ")
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

    #for f_str in cfg.subj_filter:
    #    subj = re.sub(f_str, "", subj).strip()

    #return subj
    return re.sub(cfg.subj_filter, "", subj).strip()


def convert_bytes(data):

    """Function:  convert_bytes

    Description:  Converts a string to bytes.

    Arguments:
        (input) data -> Data string
        (output) -> Bytes string

    """

    return data.encode()


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
#    log.log_info("Locating attachments...")
    log.log_info(f"[{os.getpid()}] Locating attachments...")

    if msg.is_multipart():

        for item in msg.walk():

#            if item.get_content_type() in cfg.attach_types:
            if item.get_content_type() in cfg.attach_types and item.get_filename():
                tname = os.path.join(cfg.tmp_dir, item.get_filename())
#                log.log_info(f"Attachment detected: {item.get_filename()}")
#                log.log_info(f"Attachment type: {item.get_content_type()}")
                log.log_info(
                    f"[{os.getpid()}] Attachment detected:"
                    f" {item.get_filename()}")
                log.log_info(
                    f"[{os.getpid()}] Attachment type:"
                    f" {item.get_content_type()}")

                if item.get_content_type() == "text/plain":
                    with io.open(tname, mode="wb") as fhdr:
                        fhdr.write(convert_bytes(item.get_payload()))
                else:
                    with io.open(tname, mode="wb") as fhdr:
                        fhdr.write(convert_bytes(item.get_payload(decode=True)))

#                with io.open(tname, mode="wb") as fhdr:
#                    fhdr.write(convert_bytes(item.get_payload(decode=True)))
                fname = tname + ".encoded"
                fname_list.append(fname)
                in_file = io.open(tname, mode="rb")
                out_file = io.open(fname, mode="wb")
                base64.encode(in_file, out_file)
                in_file.close()
                out_file.close()
                err_flag, err_msg = gen_libs.rm_file(tname)

                if err_flag:
#                    log.log_warn(f"process_attach:  Message: {err_msg}")
                    log.log_warn(
                        f"[{os.getpid()}] process_attach:  Message: {err_msg}")

            else:
                if item.get_filename():
#                    log.log_warn(
#                        f"Invalid attachment detected: {item.get_filename()}")
#                    log.log_warn(f"Attachment type: {item.get_content_type()}")
                    log.log_warn(
                        f"[{os.getpid()}] Invalid attachment detected:"
                        f" {item.get_filename()}")
                    log.log_warn(
                        f"[{os.getpid()}] Attachment type:"
                        f" {item.get_content_type()}")

    return fname_list


def process_subj(cfg, log, subj, msg):

    """Function:  process_subj

    Description:  Process email using its subject line and open connection and
        validate connection to RabbitMQ.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance
        (input) subj -> Email subject line
        (input) msg -> Email message body

    """

#    log.log_info(f"Valid email subject: {subj}")
    log.log_info(f"[{os.getpid()}] Valid email subject: {subj}")
    connect_rmq(cfg, log, subj, subj, msg)


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
#            log.log_info(
#                f"Valid From address: {from_addr} with file attachment:"
#                f" {fname}")
            log.log_info(
                f"[{os.getpid()}] Valid From address:"
                f" {from_addr} with file attachment: {fname}")
            connect_rmq(
                cfg, log, cfg.queue_dict[from_addr], cfg.queue_dict[from_addr],
                msg, fname=fname)
            err_flag, err_msg = gen_libs.rm_file(fname)

            if err_flag:
#                log.log_warn(f"process_from: Message: {err_msg}")
                log.log_warn(
                    f"[{os.getpid()}] process_from: Message: {err_msg}")

    else:
#        log.log_warn(f"Missing attachment for email address: {from_addr}")
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
#    log.log_info(
#        f"connect_rmq: Connection info: {cfg.host}->{cfg.exchange_name}")
    log.log_info(
        f"[{os.getpid()}] connect_rmq: Connection info:"
        f" {cfg.host}->{cfg.exchange_name}")
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
#        log.log_info("connect_rmq: Connected to RabbitMQ mode")
        log.log_info(
            f"[{os.getpid()}] connect_rmq: Connected to RabbitMQ mode")
        connect_process(rmq, log, cfg, msg, **config)

    else:
#        log.log_err("connect_rmq: Failed to connect to RabbitMQ")
#        log.log_err(f"connect_rmq: Message:  {err_msg}")
        log.log_err(
            f"[{os.getpid()}] connect_rmq: Failed to connect to RabbitMQ")
        log.log_err(f"[{os.getpid()}] connect_rmq: Message:  {err_msg}")
        archive_email(rmq, log, cfg, msg)

    if connect_status:
        rmq.close()
    #rmq.close()


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
#            log.log_info(f"Valid subject with file attachment: {fname}")
            log.log_info(
                f"[{os.getpid()}] Valid subject with file attachment: {fname}")
            connect_rmq(cfg, log, subj, subj, msg, fname=fname)
            err_flag, err_msg = gen_libs.rm_file(fname)

            if err_flag:
#                log.log_warn(f"process_file: Message: {err_msg}")
                log.log_warn(
                    f"[{os.getpid()}] process_file: Message: {err_msg}")

    elif fname_list:
        for fname in fname_list:
#            log.log_info(f"Invalid subject with file attached: {fname}")
            log.log_info(
                f"[{os.getpid()}] Invalid subject with file attached: {fname}")
            connect_rmq(
                cfg, log, cfg.err_file_queue, cfg.err_file_queue, msg,
                fname=fname)
            err_flag, err_msg = gen_libs.rm_file(fname)

            if err_flag:
#                log.log_warn(f"process_file 2: Message: {err_msg}")
                log.log_warn(
                    f"[{os.getpid()}] process_file 2: Message: {err_msg}")

    else:
#        log.log_warn(f"Invalid email subject: {subj}")
        log.log_warn(f"[{os.getpid()}] Invalid email subject: {subj}")
        connect_rmq(cfg, log, cfg.err_queue, cfg.err_queue, msg)


def process_message(cfg, log):

    """Function:  process_message

    Description:  Parses email message, processes email body or attachment and
        based on subject, from address and/or attachment, send the data to
        queue in RabbitMQ.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance

    """

#    log.log_info("Parsing email...")
    log.log_info(f"[{os.getpid()}] Parsing email...")
    msg = parse_email()
    subj = gen_libs.pascalize(filter_subject(msg["subject"], cfg))
    email_list = gen_libs.find_email_addr(msg["from"])
    from_addr = email_list[0] if email_list else None
#    log.log_info("Instance creation")
    log.log_info(f"[{os.getpid()}] Instance creation")

    if subj in cfg.valid_queues:
        process_subj(cfg, log, subj, msg)

    elif from_addr and from_addr in list(cfg.queue_dict.keys()):
        process_from(cfg, log, msg, from_addr)

    else:
        process_file(cfg, log, subj, msg)


def check_nonprocess(cfg, log):                         # pylint:disable=W0613

    """Function:  check_nonprocess

    Description:  Process any non-processed email files in the directory
        provided.

    Arguments:
        (input) cfg -> Configuration settings module for the program
        (input) log -> Log class instance

    """

    print("check_nonprocess:  Stub holder.  Yet to be developed")


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
#        log.log_info(f"{'=' * 80}")
#        log.log_info(f"{cfg.host}:{cfg.exchange_name} Initialized")
        log.log_info(f"[{os.getpid()}] {'=' * 80}")
        log.log_info(
            f"[{os.getpid()}] {cfg.host}:{cfg.exchange_name} Initialized")

        # Intersect args_array & func_dict to find which functions to call
        for opt in set(args.get_args_keys()) & set(func_dict.keys()):
            func_dict[opt](cfg, log)

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
        func_dict -> dictionary list for the function calls or other options
        opt_req_list -> contains options that are required for the program
        opt_val_list -> contains options which require values
        opt_xor_dict -> contains dict with key that is xor with it's values

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5}
    func_dict = {"-M": process_message, "-C": check_nonprocess}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]
    opt_xor_dict = {"-M": ["-C"], "-C": ["-M"]}

    # Process argument list from command line
    args = gen_class.ArgParser(sys.argv, opt_val=opt_val_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_xor_dict(opt_xor_val=opt_xor_dict)              \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):
        run_program(args, func_dict)


if __name__ == "__main__":
    sys.exit(main())
