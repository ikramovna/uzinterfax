pipeline {
    agent any

    environment {
        IMAGE_NAME = "uzinterfax_web"
        CONTAINER_NAME = "uzinterfax_web_2"
        APP_PORT = "8000"
        DEPLOY_HOST = "161.35.208.242"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out the code..."
                git branch: 'main', url: 'https://github.com/ikramovna/uzinterfax.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                echo "Setting up virtual environment..."
                python3 -m venv .venv
                bash -c "source .venv/bin/activate && pip install -r requirements.txt"
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                echo "Running linting with pylint..."
                bash -c "source .venv/bin/activate && pylint --rcfile=.pylintrc main/ || true"
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                echo "Running security scan with bandit..."
                bash -c "source .venv/bin/activate && bandit -r main/"
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                echo "Running tests with pytest..."
                bash -c "source .venv/bin/activate && pytest --cov=main"
                '''
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'deploy-credentials', usernameVariable: 'REMOTE_USER', passwordVariable: 'REMOTE_PASS')]) {
                    sh '''
                    echo "Deploying application on remote server..."
                    sshpass -p "$REMOTE_PASS" ssh -o StrictHostKeyChecking=no $REMOTE_USER@$DEPLOY_HOST "cd uzinterfax/ && docker-compose up -d --build"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully: Checkout, Test, Docker Build, and Deploy!"
        }
        failure {
            echo "Pipeline failed. Check the logs for details."
        }
    }
}
