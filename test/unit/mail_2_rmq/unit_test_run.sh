#!/bin/bash
# Unit testing program for the mail_2_rmq.py program.
# This will run all the units tests for this program and clean it up.
# Will need to run this from the base directory where the class file 
#   is located at.

test/unit/mail_2_rmq/load_cfg.py
test/unit/mail_2_rmq/parse_email.py

#test/unit/mail_2_rmq/test_archive_email.py
#cat test/unit/mail_2_rmq/test_mail.txt | test/unit/mail_2_rmq/test_connect_process.py
#cat test/unit/mail_2_rmq/test_mail.txt | test/unit/mail_2_rmq/test_process_message.py -G
#cat test/unit/mail_2_rmq/test_mail2.txt | test/unit/mail_2_rmq/test_process_message.py -B
##test/unit/mail_2_rmq/mail_2_rmq_cleanup.py
