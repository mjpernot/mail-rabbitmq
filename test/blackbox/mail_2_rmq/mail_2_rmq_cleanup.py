#!/usr/bin/python
# Classification (U)

"""Program:  mail_2_rmq_cleanup.py

    Description:  Cleanup the test exchange and queues.

    Usage:
        test/unit/mail_2_rmq/mail_2_rmq_cleanup.py

    Arguments:

"""

# Libraries and Global Variables
from __future__ import print_function

# Standard
import os
import sys
import pika

# Local
sys.path.append(os.getcwd())
import rabbit_lib.rabbitmq_class as rmq_cls  # pylint:disable=R0402,E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


def load_module(mod_name, mod_path):

    """Function:  load_module

    Description:  Load a Python module dynamically.

    Arguments:
        (input) mod_name -> Name of the module to load.
        (input) mod_path -> Directory path to the module to load.
        (output) Returns the module handler.

    """

    sys.path.append(mod_path)
    return __import__(mod_name)


def cleanup_queue(rmq, drop_exch, connect_status):

    """Function:  cleanup_queue

    Description:  Cleanup the test queues.

    Arguments:
        (input) rmq -> RabbitMQ instance class.
        (input) drop_exch (True|False) -> To drop the exchange.
        (input) connect_status -> Status of RabbitMQ connection.

    """

    try:
        rmq.channel.queue_declare(queue=rmq.queue_name, passive=True)
        rmq.clear_queue()
        rmq.drop_queue()

        if drop_exch:
            rmq.drop_exchange()

        rmq.close_channel()

        if rmq.channel.is_closed:

            ste = rmq.connection._impl.connection_state  # pylint:disable=W0212

            if connect_status and ste > 0:
                rmq.close()

                if ste == 0:
                    print(f"\t{rmq.queue_name} dropped")

                else:
                    print("\tFailed to close connection")
                    print(f"\tConnection: {rmq.connection}")
                    print(f"\tConnection State: {ste}")

            else:
                print("\tConnection not opened")

        else:
            print("\tFailure:  Channel did not close")
            print(f"\tChannel: {rmq.channel}")

    except pika.exceptions.ChannelClosed as msg:
        print("\tWarning:  Unable to locate queue")
        print(f"Error Msg: {msg}")


def mail_2_rmq_cleanup(cfg, queue_name, drop_exch=False):

    """Function:  mail_2_rmq_cleanup

    Description:  Cleanup the test exchanges and queues.

    Arguments:
        (input) cfg -> RabbitMQ configuration module handler.
        (input) queue_name -> Name of queue to drop.
        (input) drop_exch (True|False) -> To drop the exchange.

    """

    rmq = rmq_cls.RabbitMQPub(
        cfg.user, cfg.japd, cfg.host, cfg.port,
        exchange_name=cfg.exchange_name, exchange_type=cfg.exchange_type,
        queue_name=queue_name, routing_key=queue_name, x_durable=cfg.x_durable,
        q_durable=cfg.q_durable, auto_delete=cfg.auto_delete)

    if isinstance(rmq, rmq_cls.RabbitMQPub):
        connect_status, err_msg = rmq.connect()
        ste = rmq.connection._impl.connection_state  # pylint:disable=W0212

        if isinstance(rmq.connection,
                      pika.adapters.blocking_connection.BlockingConnection) \
                and ste > 0 and connect_status:

            rmq.open_channel()

            if rmq.channel.is_open:
                rmq.setup_exchange()

                try:
                    rmq.channel.exchange_declare(exchange=rmq.exchange,
                                                 passive=True)
                    rmq.create_queue()
                    cleanup_queue(rmq, drop_exch, connect_status)

                except pika.exceptions.ChannelClosed as msg:
                    print("\tWarning:  Unable to find an exchange")
                    print(f"Error Msg: {msg}")

            else:
                print("\tFailure:  Unable to open channel")
                print(f"\tChannel: {rmq.channel}")

        else:
            print("\tFailure:  Unable to open connection")
            print(f"\tConnection: {rmq.connection}")
            print(f"\tError Msg: {err_msg}")

    else:
        print("\tFailure:  Unable to initialize")
        print(f"\tClass: {rmq_cls.RabbitMQPub}")


def main():

    """Function:  main

    Description:  Control the cleanup of exchanges and queues.

    Arguments:

    """

    cfg = load_module("rabbitmq", "test/unit/mail_2_rmq/config")
    print("\nmail_2_rmq cleanup...")
    mail_2_rmq_cleanup(cfg, "isse_error_test", False)
    mail_2_rmq_cleanup(cfg, "SG-test", False)
    mail_2_rmq_cleanup(cfg, "SIPR-test", True)
    print("Everything cleaned up")


if __name__ == "__main__":
    sys.exit(main())
