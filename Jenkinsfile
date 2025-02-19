pipeline {
    agent any

    environment {
        // Set up AWS credentials
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')  // Store this in Jenkins credentials store
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')  // Store this in Jenkins credentials store
        AWS_DEFAULT_REGION = 'ap-south-1'  // Set the appropriate AWS region
        GITHUB_REPO_URL = 'https://github.com/iraghu/glue-project.git'  // GitHub repo URL
        FILE_PATH = 'glue_scripts/LandingToRawScript.py'  // Path to the file in your repo
        S3_BUCKET = 'gluerawbucket'  // The name of your S3 bucket
    }

    stages {
        stage('Clone GitHub Repository') {
            steps {
                script {
                    // Clone the GitHub repository
                    sh 'git clone ${GITHUB_REPO_URL}'
                }
            }
        }

        stage('Copy File to S3') {
            steps {
                script {
                    // Copy the file to S3
                    sh """
                        aws s3 cp ${FILE_PATH} s3://${S3_BUCKET}/ --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'File successfully copied to S3!'
        }
        failure {
            echo 'There was an error during the process.'
        }
    }
}
