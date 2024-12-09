pipeline {
    agent any

    environment {
        IMAGE_NAME = "uzinterfax_web"
        CONTAINER_NAME = "uzinterfax_web_1"
        APP_PORT = "8000"
        DEPLOY_HOST = "164.92.243.52"
        REMOTE_USER = "root"
        SSH_KEY_PATH = "/path/to/your/private/key"
    }

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
                pylint --rcfile=.pylintrc main/ || true
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
                docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo "Stopping and removing existing container..."
                    sh '''
                    sudo docker ps -aq -f name=uzinterfax_web_1 | xargs -r sudo docker stop || true
                    sudo docker ps -aq -f name=uzinterfax_web_1 | xargs -r sudo docker rm || true
                    echo "Running the new container..."
                    sudo docker run -d --name uzinterfax_web_1 -p 8000:8000 uzinterfax_web
                    '''
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                sh '''
                echo "Running tests inside the container..."
                docker exec ${CONTAINER_NAME} python manage.py test
                '''
            }
        }

        stage('Static File Collection') {
            steps {
                sh '''
                echo "Collecting static files..."
                docker exec ${CONTAINER_NAME} python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying to remote server..."
                sh '''
                ssh -i ${SSH_KEY_PATH} ${REMOTE_USER}@${DEPLOY_HOST} '
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker pull ${IMAGE_NAME}
                    docker run -d --name ${CONTAINER_NAME} -p 8000:8000 ${IMAGE_NAME}
                '
                '''
            }
        }

        stage('Clean Up') {
            steps {
                sh '''
                echo "Cleaning up container..."
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
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
            echo 'Pipeline completed successfully: linting, security scan, build, tests, static file collection, and deployment!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}