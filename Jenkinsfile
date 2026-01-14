pipeline {
    agent any

    stages {

        stage('Setup Python Environment') {
            steps {
                // Создание виртуального окружения
                sh 'python3 -m venv venv'

                // Установка зависимостей
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt --break-system-packages
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // Запуск тестов и генерация Allure результатов
                sh '''
                    . venv/bin/activate
                    python3 -m pytest --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Публикация Allure отчета (при установленном Allure Plugin)
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
            // Архивация Allure результатов
            archiveArtifacts(
                artifacts: '**/allure-results/**',
                allowEmptyArchive: true
            )
        }

        failure {
            echo 'The build failed!'
        }
    }
}
