#!/usr/bin/python
# Classification (U)

"""Program:  mail_2_rmq.py

    Description:  Process an email message and send it to the proper
        RabbitMQ queue.

    Usage:
        -M option
        email_alias: "| /{directory_path}/mail_2_rmq.py -M -c file -d path"

        All other options.
        mail_2_rmq.py [ -C ] [ -c file -d path ] [ -v | -h ]

    Arguments:
        -M => Receive email messages from email pipe and process.
        -C => Check for non-processed messages in email archive directory.
        -c file => ISSE Guard configuration file.  Required argument.
        -d dir path => Directory path for option '-c'.  Required argument.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides all other options.
        NOTE 2:  -M and -C are XOR options.

    Notes:
        The configuration file below is required to run this program.  Create
        them and replace those variables (i.e. <VARIABLE>) with a value.

        Configuration file format (rabbitmq.py).  The configuration file format
        is for the initial environment setup for the program.
            # RabbitMQ Configuration file
            # Classification (U)
            # Unclassified until filled.
            user = "<USER>"
            passwd = "<PASSWORD>"
            host = "<HOSTNAME>"
            # RabbitMQ listening port, default is 5672.
            port = 5672
            # RabbitMQ Exchange name for each instance run.
            exchange_name = "<EXCHANGE_NAME>"
            # Type of exchange:  direct, topic, fanout, headers
            exchange_type = "direct"
            # Is exchange durable: True|False
            x_durable = True
            # Are queues durable: True|False
            q_durable = True
            # Do queues delete once message is processed:  True|False
            auto_delete = False
            # List of valid queues in RabbitMQ.
            valid_queues = [ "QUEUE_NAME1", "QUEUE_NAME2", ... ]
            # Name of error queue to handle incorrect email subjects.
            err_queue = "<ERROR_QUEUE_NAME>"
            # Archive directory path for non-processed email files.
            email_dir = "/<DIRECTORY_PATH>/email_dir"
            # Directory path and file name to the program log.
            log_file = "/<DIRECTORY_PATH>/logs/mail_2_rmq.log"
            # Filter out strings within the subject line.
            # Do not modify this setting unless you understand regular
            #   expressions.
            subj_filter = ["\[.*\]"]

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
import email.Parser
import re

# Third-party

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import rabbit_lib.rabbitmq_class as rabbitmq_class
import version

# Version
__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:
        (input) **kwargs:
            None

    """

    print(__doc__)


def load_cfg(cfg_name, cfg_dir, **kwargs):

    """Function:  load_cfg

    Description:  Load the RabbitMQ configuration file and validate the
        contents of the file.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.
        (input) **kwargs:
            None
        (output) cfg -> Configuration module handler.
        (output) status_flag -> True|False - successfully validate config file.

    """

    status_flag = True

    cfg = gen_libs.load_module(cfg_name, cfg_dir)

    status, err_msg = gen_libs.chk_crt_dir(cfg.email_dir, write=True,
                                           read=True)

    if not status:
        status_flag = status

    status, err_msg = gen_libs.chk_crt_dir(os.path.dirname(cfg.log_file),
                                           write=True, read=True)

    if not status:
        status_flag = status

    return cfg, status_flag


def create_rq(cfg, q_name, r_key, **kwargs):

    """Function:  create_rq

    Description:  Create and return a RabbitMQ instance.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) q_name -> Queue name in RabbitMQ.
        (input) r_key -> Routing key in RabbitMQ.
        (input) **kwargs:
            None
        (output) RabbitMQ instance.

    """

    return rabbitmq_class.RabbitMQPub(cfg.user, cfg.passwd, cfg.host, cfg.port,
                                      cfg.exchange_name, cfg.exchange_type,
                                      q_name, r_key, cfg.x_durable,
                                      cfg.q_durable, cfg.auto_delete)


def parse_email(**kwargs):

    """Function:  parse_email

    Description:  Accept email from standard in and process email to be used
        for RabbitMQ.

    Arguments:
        (input) **kwargs:
            None
        (output) Email in list format.

    """

    p = email.Parser.Parser()

    return p.parsestr("".join(sys.stdin.readlines()))


def archive_email(rq, log, cfg, msg, **kwargs):

    """Function:  archive_email

    Description:  Save an email to file in an archive directory.

    Arguments:
        (input) rq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) msg -> Email message instance.
        (input) **kwargs:
            None

    """

    e_file = rq.exchange + "-" + rq.queue_name + "-" \
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
        (input) **kwargs:
            None
        (output) All texts in email joined together in a single string.

    """

    msg_list = []

    for part in msg.walk():

        if part.get_content_maintype() == "multipart" \
           or not part.get_payload(decode=True):
            continue

        msg_list.append(part.get_payload(decode=True))

    return "".join(msg_list)


def connect_process(rq, log, cfg, msg, **kwargs):

    """Function:  connect_process

    Description:  Connect to RabbitMQ and injest email message.

    Arguments:
        (input) rq -> RabbitMQ class instance.
        (input) log -> Log class instance.
        (input) cfg -> Configuration settings module for the program.
        (input) msg -> Email message instance.
        (input) **kwargs:
            None

    """

    log.log_info("Connection info: %s->%s" % (cfg.host, cfg.exchange_name))

    connect_status, err_msg = rq.create_connection()

    if connect_status and rq.channel.is_open:
        log.log_info("Connected to RabbitMQ mode")

        # Send entire email to error queue, otherwise just the body.
        if rq.queue_name == cfg.err_queue:
            t_msg = "From: " + msg["from"] + " To: " + msg["to"] \
                    + " Subject: " + msg["subject"] + " Body: " \
                    + get_text(msg)

        else:
            t_msg = get_text(msg)

        if rq.publish_msg(t_msg):
            log.log_info("Message ingested into RabbitMQ")

        else:
            log.log_err("Failed to injest message into RabbitMQ")

            archive_email(rq, log, cfg, msg)

    else:
        log.log_err("Failed to connnect to RabbitMQ Node...")
        log.log_err("Message:  %s" % (err_msg))

        archive_email(rq, log, cfg, msg)


def filter_subject(subj, cfg, **kwargs):

    """Function:  filter_subject

    Description:  Filter out strings from the message subject line.

    Arguments:
        (input) subj -> Message subject line.
        (input) cfg -> Configuration settings module for the program.
        (input) **kwargs:
            None
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
        (input) **kwargs:
            None
        (output) CamelCased string.

    """

    return "".join(item.capitalize() for item in re.split("([^a-zA-Z0-9])",
                                                          data_str)
                   if item.isalnum())


def process_message(cfg, log, **kwargs):

    """Function:  process_message

    Description:  Capture email message, process it, and send to RabbitMQ.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (input) **kwargs:
            None

    """

    log.log_info("Parsing email...")
    msg = parse_email()
    subj = filter_subject(msg["subject"], cfg)
    subj = camelize(subj)
    log.log_info("Instance creation")

    # Is email subject a valid queue.
    if subj in cfg.valid_queues:
        log.log_info("Valid email subject:  %s" % (subj))
        rq = create_rq(cfg, subj, subj)

    else:
        log.log_warn("Invalid email subject:  %s" % (subj))
        rq = create_rq(cfg, cfg.err_queue, cfg.err_queue)

    connect_process(rq, log, cfg, msg)


def check_nonprocess(cfg, log, **kwargs):

    """Function:  check_nonprocess

    Description:  Process any non-processed email files in the directory
        provided.

    Arguments:
        (input) cfg -> Configuration settings module for the program.
        (input) log -> Log class instance.
        (input) **kwargs:
            None

    """

    print("check_nonprocess:  Stub holder.  Yet to be developed")


def run_program(args_array, func_dict, **kwargs):

    """Function:  run_program

    Description:  Creates class instance and controls flow of the program.
        Create a program lock to prevent other instantiations from running.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) func_dict -> Dictionary list of functions and options.
        (input) **kwargs:
            None

    """

    args_array = dict(args_array)
    func_dict = dict(func_dict)

    cfg, status_flag = load_cfg(args_array["-c"], args_array["-d"])

    if not status_flag:
        print("Error:  Problem in configuration file.")

    else:
        log = gen_class.Logger(cfg.log_file, cfg.log_file, "INFO",
                               "%(asctime)s %(levelname)s %(message)s",
                               "%Y-%m-%dT%H:%M:%SZ")
        str_val = "=" * 80
        log.log_info("%s:%s Initialized" % (cfg.host, cfg.exchange_name))
        log.log_info("%s" % (str_val))
        log.log_info("Exchange Name:  %s" % (cfg.exchange_name))
        log.log_info("Exchange Type:  %s" % (cfg.exchange_type))
        log.log_info("Valid Queues:  %s" % (cfg.valid_queues))
        log.log_info("Email Archive:  %s" % (cfg.email_dir))
        log.log_info("%s" % (str_val))

        try:
            flavor_id = cfg.exchange_name
            prog_lock = gen_class.ProgramLock(sys.argv, flavor_id)

            # Intersect args_array & func_dict to find which functions to call.
            for opt in set(args_array.keys()) & set(func_dict.keys()):

                func_dict[opt](cfg, log, **kwargs)

            del prog_lock

        except gen_class.SingleInstanceException:
            log.log_warn("mail_2_rmq lock in place for: %s" % (flavor_id))

        log.log_close()


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

    dir_chk_list = ["-d"]
    func_dict = {"-M": process_message, "-C": check_nonprocess}
    opt_req_list = ["-c", "-d"]
    opt_val_list = ["-c", "-d"]
    opt_xor_dict = {"-M": ["-C"], "-C": ["-M"]}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and arg_parser.arg_xor_dict(args_array, opt_xor_dict) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

        run_program(args_array, func_dict)


if __name__ == "__main__":
    sys.exit(main())
