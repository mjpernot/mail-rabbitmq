#!/usr/bin/python
# Classification (U)

"""Program:  mail_2_rmq.py

    Description:  Process an email message and send it to the proper
        RabbitMQ queue.

    Usage:
        -M option
        email_alias: "| /PROJECT_PATH/mail_2_rmq.py -c file -d path -M
            [-y flavor_id]"

        All other options.
        mail_2_rmq.py -c file -d path [-C] [-y flavor_id]
            [ -v | -h ]

    Arguments:
        -c file => ISSE Guard configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.
        -M => Receive email messages from email pipe and process.
        -C => Check for non-processed messages in email archive directory.
        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -M and -C are XOR options.

    Notes:
        RabbitMQ configuration file format (config/rabbitmq.py.TEMPLATE).

            # RabbitMQ Configuration file
            user = "USER"
            japd = "PASSWORD"
            host = "HOSTNAME"
            # RabbitMQ Exchange name for each instance run.
            exchange_name = "EXCHANGE_NAME"
            # List of valid queues in RabbitMQ.
            # Note:  Queues names must be UpperCamelCase style.
            valid_queues = ["QueueName1", "QueueName2", ...]
            # Name of error queue to handle incorrectly routed emails.
            err_queue = "ERROR_QUEUE_NAME"
            # Name of queue for handling file attachments.
            file_queue = "FILE_QUEUE_NAME"
            # Archive directory path for non-processed email files.
            email_dir = "DIRECTORY_PATH/email_dir"
            # Directory path and file name to the program log.
            log_file = "DIRECTORY_PATH/logs/mail_2_rmq.log"
            # Directory path to temporary staging directory.
            tmp_dir = "DIRECTORY_PATH/tmp"
            # Do not modify settings below unless you know what you are doing.
            # Filter out strings within the subject line.
            # Do not modify unless you understand regular expressions.
            subj_filter = ["\[.*\]"]
            # Types of attachments to extract from email.
            attach_types = ["application/pdf"]
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Do queues automatically delete once message is processed.
            auto_delete = False

    Example:
        alias: "| /opt/local/mail_2_rmq.py -M -c rabbitmq -d /opt/local/config"

        mail_2_rmq.py -c file -d path -C

"""

# Libraries and Global Variables

# Standard
from __future__ import print_function
import sys
import os
import datetime

# Third-party
import email.Parser
import re
import base64

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def load_cfg(cfg_name, cfg_dir, **kwargs):

    """Function:  load_cfg

    Description:  Load the RabbitMQ configuration file and validate the
        contents of the file.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.
        (output) cfg -> Configuration module handler.
        (output) status_flag -> True|False - successfully validate config file.
        (output) combined_msg -> List of error messages detected.

    """

    status_flag = True
    combined_msg = []
    cfg = gen_libs.load_module(cfg_name, cfg_dir)
    status, err_msg = gen_libs.chk_crt_dir(cfg.email_dir, write=True,
                                           read=True)

    if not status:
        status_flag = status
        combined_msg.append(err_msg)

    status, err_msg = gen_libs.chk_crt_dir(os.path.dirname(cfg.log_file),
                                           write=True, read=True)

    if not status:
        status_flag = status
        combined_msg.append(err_msg)

    status, err_msg = gen_libs.chk_crt_dir(cfg.tmp_dir, write=True, read=True)

    if not status:
        status_flag = status
        combined_msg.append(err_msg)

    return cfg, status_flag, combined_msg


def create_rq(cfg, q_name, r_key, **kwargs):

    """Function:  create_rq

    Description:  Create and return a RabbitMQ instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) q_name -> Queue name in RabbitMQ.
        (input) r_key -> Routing key in RabbitMQ.
        (output) RabbitMQ instance.

    """

    return rabbitmq_class.RabbitMQPub(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=q_name, routing_key=r_key, x_durable=cfg.x_durable,
        q_durable=cfg.q_durable, auto_delete=cfg.auto_delete)


def parse_email(**kwargs):

    """Function:  parse_email

    Description:  Accept email from standard in and process email to be used
        for RabbitMQ.

    Arguments:
        (output) Email instance.

    """

    cmdline = gen_libs.get_inst(sys)
    parser = email.Parser.Parser()

    return parser.parsestr("".join(cmdline.stdin.readlines()))


def archive_email(rmq, log, cfg, msg, **kwargs):

    """Function:  archive_email

    Description:  Save an email to file in an archive directory.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) msg -> Email message instance.

    """

    e_file = rmq.exchange + "-" + rmq.queue_name + "-" \
        + datetime.datetime.strftime(datetime.datetime.now(),
                                     "%Y%m%d-%H%M%S") + ".email.txt"
    log.log_info("Saving email to: %s" %
                 (cfg.email_dir + os.path.sep + e_file))
    gen_libs.write_file(cfg.email_dir + os.path.sep + e_file, "w", msg)
    log.log_info("Email saved to:  %s" % (e_file))


def get_text(msg, **kwargs):

    """Function:  get_text

    Description:  Walks the tree of a email and returns the text of the email.

    Arguments:
        (input) msg -> Email message instance.
        (output) All texts in email joined together in a single string.

    """

    msg_list = []

    for part in msg.walk():

        if part.get_content_maintype() == "multipart" \
           or not part.get_payload(decode=True):

            continue

        msg_list.append(part.get_payload(decode=True))

    return "".join(msg_list)


def connect_process(rmq, log, cfg, msg, **kwargs):

    """Function:  connect_process

    Description:  Connect to RabbitMQ and injest email message.

    Arguments:
        (input) rmq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) msg -> Email message instance.
        (input) kwargs:
            fname -> File name of email/attachment.

    """

    fname = kwargs.get("fname", None)
    log.log_info("Connection info: %s->%s" % (cfg.host, cfg.exchange_name))
    connect_status, err_msg = rmq.create_connection()

    if connect_status and rmq.channel.is_open:
        log.log_info("Connected to RabbitMQ mode")

        # Process email or file/attachment.
        if fname:
            log.log_info("Processing file/attachment...")

            with open(fname, "r") as f_hldr:
                t_msg = f_hldr.read()

        elif rmq.queue_name == cfg.err_queue:
            log.log_info("Processing error message...")
            t_msg = "From: " + msg["from"] + " To: " + msg["to"] \
                    + " Subject: " + msg["subject"] + " Body: " \
                    + get_text(msg)

        else:
            log.log_info("Processing email body...")
            t_msg = get_text(msg)

        if t_msg and rmq.publish_msg(t_msg):
            log.log_info("Message ingested into RabbitMQ")

        else:
            log.log_err("Failed to injest message into RabbitMQ")
            archive_email(rmq, log, cfg, msg)

    else:
        log.log_err("Failed to connnect to RabbitMQ Node...")
        log.log_err("Message:  %s" % (err_msg))
        archive_email(rmq, log, cfg, msg)


def filter_subject(subj, cfg, **kwargs):

    """Function:  filter_subject

    Description:  Filter out strings from the message subject line.

    Arguments:
        (input) subj -> Message subject line.
        (input) cfg -> Configuration settings module for the program.
        (output) subj -> Filtered message subject line.

    """

    for f_str in cfg.subj_filter:
        subj = re.sub(f_str, "", subj).strip()

    return subj


def camelize(data_str, **kwargs):

    """Function:  camelize

    Description:  Camelcases a string.

    Arguments:
        (input) data_str -> String to be camelcased.
        (output) CamelCased string.

    """

    return "".join(item.capitalize() for item in re.split("([^a-zA-Z0-9])",
                                                          data_str)
                   if item.isalnum())


def process_attach(msg, log, cfg, **kwargs):

    """Function:  process_attach

    Description:  Locate, extract, and process attachment from email based on
        specified attachment types.

    Arguments:
        (input) msg -> Email message instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (output) fname -> Name of encoded attachment file.

    """

    fname = None
    log.log_info("Locating attachments...")

    if msg.is_multipart():

        for item in msg.walk():

            if item.get_content_type() in cfg.attach_types:
                tname = os.path.join(cfg.tmp_dir, item.get_filename())
                log.log_info("Attachment detected: %s" % (item.get_filename()))
                open(tname, "wb").write(item.get_payload(decode=True))
                fname = tname + ".encoded"
                base64.encode(open(tname, 'rb'), open(fname, 'wb'))
                err_flag, err_msg = gen_libs.rm_file(tname)

                if err_flag:
                    log.log_warn("process_attach:  Message: %s" % (err_msg))

                break

    return fname


def process_message(cfg, log, **kwargs):

    """Function:  process_message

    Description:  Capture email message, process email body or email
        attachment, and send the data to RabbitMQ.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.

    """

    log.log_info("Parsing email...")
    msg = parse_email()
    subj = filter_subject(msg["subject"], cfg)
    subj = camelize(subj)
    log.log_info("Instance creation")

    # Is email subject a valid queue.
    if subj in cfg.valid_queues:
        log.log_info("Valid email subject:  %s" % (subj))
        rmq = create_rq(cfg, subj, subj)
        connect_process(rmq, log, cfg, msg)

    else:
        fname = process_attach(msg, log, cfg)

        if fname:
            log.log_info("Valid file attachment:  %s" % (fname))
            rmq = create_rq(cfg, cfg.file_queue, cfg.file_queue)
            connect_process(rmq, log, cfg, msg, fname=fname)
            err_flag, err_msg = gen_libs.rm_file(fname)

            if err_flag:
                log.log_warn("process_message:  Message: %s" % (err_msg))

        else:
            log.log_warn("Invalid email subject:  %s" % (subj))
            rmq = create_rq(cfg, cfg.err_queue, cfg.err_queue)
            connect_process(rmq, log, cfg, msg)


def check_nonprocess(cfg, log, **kwargs):

    """Function:  check_nonprocess

    Description:  Process any non-processed email files in the directory
        provided.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.

    """

    print("check_nonprocess:  Stub holder.  Yet to be developed")


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Create a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.

    """

    cmdline = gen_libs.get_inst(sys)
    args_array = dict(args_array)
    func_dict = dict(func_dict)
    cfg, status_flag, err_msgs = load_cfg(args_array["-c"], args_array["-d"])

    if status_flag:
        log = gen_class.Logger(
            cfg.log_file, cfg.log_file, "INFO",
            "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%SZ")
        str_val = "=" * 80
        log.log_info("%s:%s Initialized" % (cfg.host, cfg.exchange_name))
        log.log_info("%s" % (str_val))
        log.log_info("Exchange Name:  %s" % (cfg.exchange_name))
        log.log_info("Exchange Type:  %s" % (cfg.exchange_type))
        log.log_info("Valid Queues:  %s" % (cfg.valid_queues))
        log.log_info("Email Archive:  %s" % (cfg.email_dir))
        log.log_info("%s" % (str_val))

        try:
            flavor_id = args_array.get("-y", cfg.exchange_name)
            prog_lock = gen_class.ProgramLock(cmdline.argv, flavor_id)

            # Intersect args_array & func_dict to find which functions to call.
            for opt in set(args_array.keys()) & set(func_dict.keys()):
                func_dict[opt](cfg, log, **kwargs)

            del prog_lock

        except gen_class.SingleInstanceException:
            log.log_warn("mail_2_rmq lock in place for: %s" % (flavor_id))

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
        dir_chk_list -> contains options which will be directories.
        func_dict -> dictionary list for the function calls or other options.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.
        opt_xor_dict -> contains dict with key that is xor with it's values.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d"]
    func_dict = {"-M": process_message, "-C": check_nonprocess}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d", "-y"]
    opt_xor_dict = {"-M": ["-C"], "-C": ["-M"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):
        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
