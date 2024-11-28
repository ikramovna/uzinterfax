pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/your-django-project.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("django-app:${env.BUILD_ID}")
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }
        stage('Deploy') {
    steps {
        script {
            sh 'docker-compose -f docker-compose.prod.yml up -d'
        }
    }
}

    }
    post {
        always {
            cleanWs()
        }
    }
}
