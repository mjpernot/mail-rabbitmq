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
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('rabbit_lib') {
                    git branch: "master", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.dicelab.net/JAC-IDM/rabbitmq-lib.git"
                }
                sh """
                pip2 install mock --user
                pip2 install pika==0.11.0 --user
                test/unit/mail_2_rmq/help_message.py
                test/unit/mail_2_rmq/get_text.py
                test/unit/mail_2_rmq/connect_process.py
                test/unit/mail_2_rmq/load_cfg.py
                test/unit/mail_2_rmq/parse_email.py
                test/unit/mail_2_rmq/process_message.py
                test/unit/mail_2_rmq/check_nonprocess.py
                test/unit/mail_2_rmq/archive_email.py
                test/unit/mail_2_rmq/run_program.py
                test/unit/mail_2_rmq/main.py
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
                    server.credentialsId = 'svc-highpoint-artifactory'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "generic-local/highpoint/mail-rabbitmq/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "generic-local/highpoint/mail-rabbitmq/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "generic-local/highpoint/mail-rabbitmq/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "generic-local/highpoint/mail-rabbitmq/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
}
