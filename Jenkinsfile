pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'uzinterfax-app:latest'
        DOCKER_FILE = './Dockerfile'
        REPO_URL = 'https://github.com/ikramovna/uzinterfax.git'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out the code from Git'
                git branch: 'main', url: "$REPO_URL"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image'
                sh 'docker build -t $DOCKER_IMAGE -f $DOCKER_FILE .'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests inside the Docker container'
                sh 'docker run --rm $DOCKER_IMAGE bash -c "python manage.py test"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application'
                // Add deployment commands (e.g., SSH, Kubernetes, etc.)
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace'
            cleanWs()
        }
    }
}
