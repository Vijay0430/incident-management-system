pipeline {

    agent any

    environment {
        scannerHome = tool 'sonarqube'
    }

    stages {

        stage('Code Clone') {

            steps {

                git branch: 'main',
                url: 'https://github.com/Vijay0430/incident-management-system.git'
            }
        }

        stage('SonarQube Scan') {

            steps {

                withSonarQubeEnv('sonarqube') {

                    sh """
                    ${scannerHome}/bin/sonar-scanner \
                    -Dsonar.projectKey=incident-management-system \
                    -Dsonar.projectName=incident-management-system \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://34.205.64.9:1234
                    """
                }
            }
        }
        
        
        stage ('build') {
            steps {
                sh ' docker-compose build'
            }
        }
        
        
        stage('scan') {
            steps { 
                sh 'trivy  image demo-01_backend:latest '
                sh 'trivy image demo-01_frontend:latest'
                sh 'trivy image demo-01_worker:latest '
            }
        }
        
        
        stage('deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }
}
