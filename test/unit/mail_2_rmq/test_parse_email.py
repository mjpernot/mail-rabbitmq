#!/usr/bin/python
# Classification (U)

"""Program:  test_parse_email.py

    Description:  Unit testing of parse_email in mail_2_rmq.py.

    Usage:
        cat test/unit/mail_2_rmq/test_mail.txt |\
        test/unit/mail_2_rmq/test_parse_email.py

    Arguments:
        None

"""

# Libraries and Global Variables

# Standard
import sys
import os

# Third-party

# Local
sys.path.append(os.getcwd())
import mail_2_rmq
import version

# Version
__version__ = version.__version__


def test_parse_email():

    """Function:  test_parse_email

    Description:  Test mail_2_rmq.parse_email function.

    Arguments:
        None

    """

    subj = "SIPR-test"
    to = "mailrabbit@euukmowks9001j.dodiis.ic.gov"
    frm = "mark.pernot@euukmowks9001j.dodiis.ic.gov"

    msg = mail_2_rmq.parse_email()

    if msg['subject'] == subj and msg['to'] == to and msg['from'] == frm:
        print("\tPASS")

    else:
        print("\tFAILURE")
        print("Looking for \n\tTO: %s\n\tFROM: %s\n\tSUBJECT: %s"
              % (to, frm, subj))
        print("Found \n\tTO: %s\n\tFROM: %s\n\tSUBJECT: %s"
              % (msg['to'], msg['from'], msg['subject']))


def main():

    """Function:  main

    Description:  Control the testing of units (functions).

    Variables:
        None

    Arguments:
        None

    """

    print("\nmail_2_rmq.parse_email unit testing...")
    test_parse_email()


if __name__ == "__main__":
    sys.exit(main())
