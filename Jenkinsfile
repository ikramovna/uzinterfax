pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clone your Git repository
                git branch: 'main', url: 'https://github.com/ikramovna/uzinterfax.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                echo "Setting up virtual environment..."
                python3 -m venv .venv
                source .venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                echo "Running linting with pylint..."
                source .venv/bin/activate
                pylint main/
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                echo "Running security scan with bandit..."
                source .venv/bin/activate
                bandit -r main/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                echo "Running tests with pytest..."
                source .venv/bin/activate
                pytest --cov=main
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Building Docker image..."
                docker build -t uzinterfax_web .
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                echo "Checking for existing container..."

                # Stop the container if it's running
                if [ "$(docker ps -q -f name=uzinterfax_web_1)" ]; then
                    echo "Stopping existing container..."
                    docker stop uzinterfax_web_1
                fi

                # Remove the container if it exists
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

        stage('Run Tests in Container') {
            steps {
                sh '''
                echo "Running tests inside the container..."
                docker exec uzinterfax_web_1 python manage.py test
                '''
            }
        }

        stage('Static File Collection') {
            steps {
                sh '''
                echo "Collecting static files..."
                docker exec uzinterfax_web_1 python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Clean Up') {
            steps {
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
            echo 'Linting, security scan, build, tests, and static file collection completed successfully!'
        }
        failure {
            echo 'Build or tests failed. Check the logs for details.'
        }
    }
}
