#!/bin/bash
# Unit testing program for the mail_2_rmq.py program.
# This will run all the units tests for this program and clean it up.
# Will need to run this from the base directory where the class file 
#   is located at.

/usr/bin/python test/unit/mail_2_rmq/archive_email.py
/usr/bin/python test/unit/mail_2_rmq/check_nonprocess.py
/usr/bin/python test/unit/mail_2_rmq/connect_process.py
/usr/bin/python test/unit/mail_2_rmq/connect_rmq.py
/usr/bin/python test/unit/mail_2_rmq/convert_bytes.py
/usr/bin/python test/unit/mail_2_rmq/filter_subject.py
/usr/bin/python test/unit/mail_2_rmq/get_text.py
/usr/bin/python test/unit/mail_2_rmq/help_message.py
/usr/bin/python test/unit/mail_2_rmq/load_cfg.py
/usr/bin/python test/unit/mail_2_rmq/main.py
/usr/bin/python test/unit/mail_2_rmq/parse_email.py
/usr/bin/python test/unit/mail_2_rmq/process_attach.py
/usr/bin/python test/unit/mail_2_rmq/process_file.py
/usr/bin/python test/unit/mail_2_rmq/process_from.py
/usr/bin/python test/unit/mail_2_rmq/process_message.py
/usr/bin/python test/unit/mail_2_rmq/process_subj.py
/usr/bin/python test/unit/mail_2_rmq/run_program.py
/usr/bin/python test/unit/mail_2_rmq/process_debug.py
