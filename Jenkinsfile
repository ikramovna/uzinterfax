pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clone your Git repository
                git branch: 'main', url: 'https://github.com/ikramovna/uzinterfax.git'
            }
        }

        stage('Lint') {
            steps {
                sh 'pylint main/'
            }
        }

        stage('Security Scan') {
            steps {
                sh 'bandit -r main/'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --cov=main'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build your Django application's Docker image
                sh '''
                echo "Building Docker image..."
                sudo docker build -t uzinterfax_web .
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                // Stop and remove any running or stopped container with the same name
                sh '''
                echo "Checking for existing container..."

                # Stop the container if it's running
                if [ "$(sudo docker ps -q -f name=uzinterfax_web_1)" ]; then
                    echo "Stopping existing container..."
                    sudo docker stop uzinterfax_web_1
                fi

                # Remove the container if it exists
                if [ "$(sudo docker ps -aq -f name=uzinterfax_web_1)" ]; then
                    echo "Removing existing container..."
                    sudo docker rm uzinterfax_web_1
                fi

                # Run a new container
                echo "Starting a new container..."
                sudo docker run -d --name uzinterfax_web_1 -p 8000:8000 uzinterfax_web
                '''
            }
        }

        stage('Run Tests in Container') {
            steps {
                // Run Django tests inside the container
                sh '''
                echo "Running tests inside the container..."
                sudo docker exec uzinterfax_web_1 python manage.py test
                '''
            }
        }

        stage('Static File Collection') {
            steps {
                // Collect static files for deployment
                sh '''
                echo "Collecting static files..."
                sudo docker exec uzinterfax_web_1 python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Clean Up') {
            steps {
                // Stop and remove the container after tests
                sh '''
                echo "Cleaning up container..."
                sudo docker stop uzinterfax_web_1 || true
                sudo docker rm uzinterfax_web_1 || true
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
            echo 'Linting, security scan, build, tests, and static file collection completed successfully!'
        }
        failure {
            echo 'Build or tests failed. Check the logs for details.'
        }
    }
}
