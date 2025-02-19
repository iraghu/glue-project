pipeline {
    agent any

    environment {
        // AWS credentials (configured in Jenkins or using environment variables)
        AWS_ACCESS_KEY_ID = aws-quad-credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = aws-quad-credentials('aws-secret-access-key')
        AWS_DEFAULT_REGION = 'ap-south-1'  // adjust the region as necessary
        echo AWS_ACCESS_KEY_ID
    }

    stages {
        stage('Download File from GitHub') {
            steps {
                script {
                    // URL of the raw file in the GitHub repository
                    def fileUrl = 'https://raw.githubusercontent.com/iraghu/glue-project/main/glue_scripts/LandingToRawScript.py'
                    
                    // Use curl to download the file from GitHub
                    sh "curl -o downloaded_file.py ${fileUrl}"
                }
            }
        }
        
        stage('Upload to S3') {
            steps {
                script {
                    // AWS CLI command to upload the file to the S3 bucket
                    sh "aws s3 cp downloaded_file.py s3://gluerawbucket/glue-scripts-cicd/file/"
                }
            }
        }
    }
}
