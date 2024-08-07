pipeline {
    agent any

    stages {
        stage('checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/feezahlee/python-scripts.git']])
            }
        }
        stage('build') {
            steps {
                git branch: 'main', url: 'https://github.com/feezahlee/python-scripts.git'
                sh 'python3 apache_secure2.py'
            }
        }
        stage('Test') {
            steps {
                echo 'the job has been tested'
            }
        }
    }
}
