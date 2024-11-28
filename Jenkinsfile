pipeline {
    agent {
        docker {
            image 'python:3.9'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                pip install -r requirements.txt
                python manage.py test
                '''
            }
        }
    }
}
