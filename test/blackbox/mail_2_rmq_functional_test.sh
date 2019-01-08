#!/bin/bash
# Black-box testing program for the mail_2_rmq.py program.
# If testing outside of the test environment listed below.  Will need to change
#   the CONFIG_DIR, EMAIL_DIR, and LOG_DIR variables to the new test environment.

BASE_PATH=$PWD

# Change these variables to the test environment setup.
EMAIL_DIR="${BASE_PATH}/email_dir"
LOG_DIR="${BASE_PATH}/logs"
LOG_FILE="${LOG_DIR}/mail_2_rmq.log"
CONFIG_DIR="${BASE_PATH}/config"
EMAIL_ALIAS="mailrabbit"
INGEST_MSG="INFO Message ingested into RabbitMQ"
INVALID_SUBJ="WARNING Invalid email subject"
FAILED_CONN="ERROR Failed to connnect to RabbuitMQ Node"
SAVED_TO="INFO Email saved to"

# Do not change.
err_flag="False"


# Check to see if /etc/aliases is setup for this test.
if [ "$(grep ${EMAIL_ALIAS} /etc/aliases | egrep -c ${CONFIG_DIR})" != 2 ] ; then
    printf "Email alias: ${EMAIL_ALIAS} in /etc/aliases is not setup for functional testing\n"
    printf "Must have the configuration file pointing to: ${CONFIG_DIR}\n"
    printf "Current entry is:  $(grep ${EMAIL_ALIAS} /etc/aliases)\n"
    err_flag="True"
fi


# These checks are for the directories that will contain the test files.
#    All directories must be clear to allow good tests to complete.
#    Check for existing test files and exit if present.
if [ ! -d "${EMAIL_DIR}" ] ; then
    printf "Directory does not exist: ${EMAIL_DIR}...cannot continue\n"
    err_flag="True"
fi

if [ "$(stat -c "%a" "${EMAIL_DIR}")" != 777 ] ; then
    printf "Directory: ${EMAIL_DIR} is set to:  "$(stat -c "%a" "${EMAIL_DIR}")"\n"
    printf "Directory: ${EMAIL_DIR} needs to be set to 777...cannot continue\n"
    err_flag="True"
fi

if [ ! -d "${LOG_DIR}" ] ; then
    printf "Directory does not exist: ${LOG_DIR}...cannot continue\n"
    err_flag="True"
fi

if [ "$(stat -c "%a" "${LOG_DIR}")" != 777 ] ; then
    printf "Directory: ${LOG_DIR} is set to:  "$(stat -c "%a" "${LOG_DIR}")"\n"
    printf "Directory: ${LOG_DIR} needs to be set to 777...cannot continue\n"
    err_flag="True"
fi

if [ ! -z "$(ls ${EMAIL_DIR})" ] ; then
    printf "Files exist in ${EMAIL_DIR}...cannot continue\n"
    err_flag="True"
fi

if [ ! -z "$(ls ${LOG_DIR})" ] ; then
    printf "Files exist in ${LOG_DIR}...cannot continue\n"
    err_flag="True"
fi


# These are test cases for specific types of emails.
# Test case:  Valid email subject from SIPR.
if [ $err_flag != "True" ] ; then
    printf "Test case:  Valid email subject from SIPR...\n"
    echo "Test Message 1" | mailx -s SIPR-test mailrabbit
    sleep 5
    if [ "$(egrep -c "${INGEST_MSG}" "${LOG_FILE}")" == 1 ] ; then
        printf "\tPASSED\n"
        rm -f ${LOG_FILE}
    else
        printf "ERROR: Did not find ingest message:  ${INGEST_MSG}\n"
        printf "Log file:  $(cat ${LOG_FILE})\n"
        err_flag="True"
	fi
else
    printf "Error flag has been detected.  Unable to complete test.\n"
fi

# Test case:  Valid email subject from SG
if [ $err_flag != "True" ] ; then
    printf "Test case:  Valid email subject from SG...\n"
    echo "Test Message 2" | mailx -s SG-test mailrabbit
    sleep 5
    if [ "$(egrep -c "${INGEST_MSG}" "${LOG_FILE}")" == 1 ] ; then
        printf "\tPASSED\n"
        rm -f ${LOG_FILE}
    else
        printf "ERROR: Did not find ingest message:  ${INGEST_MSG}\n"
        printf "Log file:  $(cat ${LOG_FILE})\n"
        err_flag="True"
    fi
else
    printf "Error flag has been detected.  Unable to complete test.\n"
fi

# Test case:  Invalid email subject from SIPR.
if [ $err_flag != "True" ] ; then
    printf "Test case:  Invalid email subject from SIPR...\n"
    echo "Test Message 3" | mailx -s SIPR-test1 mailrabbit
    sleep 5
    if [ "$(egrep -c "${INVALID_SUBJ}" "${LOG_FILE}")" == 1 ] ; then
        if [ "$(egrep -c "${INGEST_MSG}" "${LOG_FILE}")" == 1 ] ; then
            printf "\tPASSED\n"
            rm -f ${LOG_FILE}
        else
            printf "ERROR: Did not find ingest message:  ${INGEST_MSG}\n"
            printf "Log file:  $(cat ${LOG_FILE})\n"
            err_flag="True"
        fi
    else
        printf "ERROR: Did not find invalid message:  ${INVALID_SUBJ}\n"
        printf "Log file:  $(cat ${LOG_FILE})\n"
        err_flag="True"
    fi
else
    printf "Error flag has been detected.  Unable to complete test.\n"
fi

# Test case:  Invalid email subject from SG
if [ $err_flag != "True" ] ; then
    printf "Test case:  Invalid email subject from SG...\n"
    echo "Test Message 4" | mailx -s SG-test2 mailrabbit
    sleep 5
    if [ "$(egrep -c "${INVALID_SUBJ}" "${LOG_FILE}")" == 1 ] ; then
        if [ "$(egrep -c "${INGEST_MSG}" "${LOG_FILE}")" == 1 ] ; then
            printf "\tPASSED\n"
            rm -f ${LOG_FILE}
        else
            printf "ERROR: Did not find ingest message:  ${INGEST_MSG}\n"
            printf "Log file:  $(cat ${LOG_FILE})\n"
            err_flag="True"
        fi
    else
        printf "ERROR: Did not find invalid message:  ${INVALID_SUBJ}\n"
        printf "Log file:  $(cat ${LOG_FILE})\n"
        err_flag="True"
    fi
else
    printf "Error flag has been detected.  Unable to complete test.\n"
fi

# Test case:  Non-connection to RabbitMQ.
if [ $err_flag != "True" ] ; then
    printf "Test case:  Non-connection to RabbitMQ...\n"
    echo "Test Message 5" | mailx -s SIPR-test mailrabbit_2
    sleep 5
    if [ "$(egrep -c "${FAILED_CONN}" "${LOG_FILE}")" == 1 ] ; then
        if [ "$(egrep -c "${SAVED_TO}" "${LOG_FILE}")" == 1 ] ; then
            if [ ! -z "$(ls ${EMAIL_DIR})" ] ; then
                printf "\tPASSED\n"
                rm -f ${EMAIL_DIR}/isse-guard-test-SIPR-test-*
                rm -f ${LOG_FILE}
            else
                printf "Archive email files does not exist in ${EMAIL_DIR}\n"
                err_flag="True"
            fi
        else
            printf "ERROR: Did not find Saved email to message:  ${INGEST_MSG}\n"
            printf "Log file:  $(cat ${LOG_FILE})\n"
            err_flag="True"
        fi
    else
        printf "ERROR: Did not find failed connection message:  ${INVALID_SUBJ}\n"
        printf "Log file:  $(cat ${LOG_FILE})\n"
        err_flag="True"
    fi
else
    printf "Error flag has been detected.  Unable to complete test.\n"
fi

