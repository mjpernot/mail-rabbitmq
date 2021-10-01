pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('rabbit_lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/rabbitmq-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install mock==2.0.0 --user
                pip2 install pika==1.2.0 --user
                ./test/unit/mail_2_rmq/archive_email.py
                ./test/unit/mail_2_rmq/camelize.py
                ./test/unit/mail_2_rmq/check_nonprocess.py
                ./test/unit/mail_2_rmq/connect_process.py
                ./test/unit/mail_2_rmq/create_rq.py
                ./test/unit/mail_2_rmq/filter_subject.py
                ./test/unit/mail_2_rmq/get_email_addr.py
                ./test/unit/mail_2_rmq/get_text.py
                ./test/unit/mail_2_rmq/help_message.py
                ./test/unit/mail_2_rmq/load_cfg.py
                ./test/unit/mail_2_rmq/main.py
                ./test/unit/mail_2_rmq/parse_email.py
                ./test/unit/mail_2_rmq/process_attach.py
                ./test/unit/mail_2_rmq/process_file.py
                ./test/unit/mail_2_rmq/process_from.py
                ./test/unit/mail_2_rmq/process_message.py
                ./test/unit/mail_2_rmq/process_subj.py
                ./test/unit/mail_2_rmq/run_program.py
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                script {
                    sh './test/unit/sonarqube_code_coverage.sh'
                    sh 'rm -rf lib'
                    sh 'rm -rf rabbit_lib'
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mail-rabbitmq/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mail-rabbitmq/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mail-rabbitmq/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mail-rabbitmq/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
    post {
        always {
            cleanWs disableDeferredWipeout: true
        }
    }
}
