pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clone your Git repository
                git branch: 'main', url: 'https://github.com/ikramovna/uzinterfax.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build your Django application's Docker image
                sh 'docker build -t uzinterfax_web .'
            }
        }

        stage('Run Docker Container') {
            steps {
                // Stop and remove any running or stopped container with the same name
                sh '''
                # Stop the container if it's running
                if [ "$(docker ps -q -f name=uzinterfax_web_1)" ]; then
                    echo "Stopping existing container..."
                    docker stop uzinterfax_web_1
                fi

                # Remove the container if it exists (even if stopped)
                if [ "$(docker ps -aq -f name=uzinterfax_web_1)" ]; then
                    echo "Removing existing container..."
                    docker rm uzinterfax_web_1
                fi

                # Run a new container
                echo "Starting a new container..."
                docker run -d --name uzinterfax_web_1 -p 8000:8000 uzinterfax_web
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // Run Django tests inside the container
                sh '''
                echo "Running tests..."
                docker exec uzinterfax_web_1 python manage.py test
                '''
            }
        }

        stage('Static File Collection') {
            steps {
                // Collect static files for deployment
                sh '''
                echo "Collecting static files..."
                docker exec uzinterfax_web_1 python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Clean Up') {
            steps {
                // Stop and remove the container after tests
                sh '''
                echo "Cleaning up container..."
                docker stop uzinterfax_web_1 || true
                docker rm uzinterfax_web_1 || true
                '''
            }
        }
    }

    post {
        always {
            // Clean up workspace
            echo "Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo 'Build, tests, and static file collection completed successfully!'
        }
        failure {
            echo 'Build failed. Check the logs for details.'
        }
    }
}
