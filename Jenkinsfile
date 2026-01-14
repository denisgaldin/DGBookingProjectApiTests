pipeline {
    agent any

    environment {
        ENVIRONMENT = 'test'
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -m pytest --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure(
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                )
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/allure-results/**', allowEmptyArchive: true
        }

        failure {
            echo 'The build failed!'
        }
    }
}
