#!/bin/bash
# Unit testing program for the mail_2_rmq.py program.
# This will run all the units tests for this program and clean it up.
# Will need to run this from the base directory where the class file 
#   is located at.

test/unit/mail_2_rmq/load_cfg.py
test/unit/mail_2_rmq/parse_email.py
test/unit/mail_2_rmq/archive_email.py
test/unit/mail_2_rmq/connect_process.py
test/unit/mail_2_rmq/process_message.py

