pipeline {
    agent any

    environment {
        // Define reusable environment variables
        DOCKER_IMAGE = 'uzinterfax-app:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // Fetch code from the repository
                git branch: 'main', url: 'https://github.com/ikramovna/uzinterfax.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Run Tests') {
            steps {
                // Run tests using the Docker container
                sh '''
                docker run --rm $DOCKER_IMAGE bash -c "
                python manage.py test
                "
                '''
            }
        }

        stage('Deploy') {
            steps {
                // Deploy to the production server (example placeholder)
                echo 'Deploying the application...'
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}
