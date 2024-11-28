pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ikramovna/uzinterfax.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                echo "Setting up virtual environment..."
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }


         stage('Lint') {
            steps {
                sh '''
                echo "Running linting with pylint..."
                . .venv/bin/activate
                pylint --rcfile=.pylintrc main/
                '''
            }
         }



        stage('Security Scan') {
            steps {
                sh '''
                echo "Running security scan with bandit..."
                . .venv/bin/activate
                bandit -r main/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                echo "Running tests with pytest..."
                . .venv/bin/activate
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

                if [ "$(docker ps -q -f name=uzinterfax_web_1)" ]; then
                    echo "Stopping existing container..."
                    docker stop uzinterfax_web_1
                fi

                if [ "$(docker ps -aq -f name=uzinterfax_web_1)" ]; then
                    echo "Removing existing container..."
                    docker rm uzinterfax_web_1
                fi

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
