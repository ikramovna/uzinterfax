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
                // Stop any running instance of the container
                sh 'docker stop uzinterfax_web_1 || true && docker rm uzinterfax_web_1 || true'
                // Run the container in detached mode
                sh 'docker run -d --name uzinterfax_web_1 -p 8000:8000 uzinterfax_web'
            }
        }

        stage('Run Tests') {
            steps {
                // Run Django tests inside the container
                sh 'docker exec uzinterfax_web_1 python manage.py test'
            }
        }

        stage('Static File Collection') {
            steps {
                // Collect static files for deployment
                sh 'docker exec uzinterfax_web_1 python manage.py collectstatic --noinput'
            }
        }

        stage('Clean Up') {
            steps {
                // Stop and remove the container after tests
                sh 'docker stop uzinterfax_web_1 && docker rm uzinterfax_web_1'
            }
        }
    }

    post {
        always {
            // Clean up workspace
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
