pipeline {
    agent any
 
    environment {
        AWS_REGION = 'ap-south-1'
        S3_BUCKET = 'gluerawbucket'
        GLUE_JOB_NAME = 'RawToRefinedScript-cicdJob'
        GLUE_SCRIPT_PATH = 'glue_scripts/LandingToRawScript.py'
    }
 
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/iraghu/glue-project.git'
            }
        }
 
        stage('Upload Script to S3') {
            steps {
                echo "Hello1"
                echo GLUE_SCRIPT_PATH
                withAWS(credentials: 'credentials', region: "${AWS_REGION}") {
                    echo "Hello2"
                    bat """
                    aws s3 cp ${GLUE_SCRIPT_PATH} s3://${S3_BUCKET}/glue-scripts-cicd/${GLUE_SCRIPT_PATH}"
                    """
                    echo "Hello3"
                }
            }
        }
 
        
        stage('Update Glue Job') {
            steps {
                script {
                    // Updating AWS Glue job using AWS CLI
                    withAWS(credentials: 'credentials', region: "${AWS_REGION}") {
                    def updateJobCommand = """
                    aws glue create-job --name RawToRefinedScript-cicdJob --role=arn:aws:iam::442116323705:role/glues3, --command="{Name:glueetl,ScriptLocation:s3://gluerawbucket/glue-scripts-cicd/glue_scripts/LandingToRawScript.py,PythonVersion:3}"
                    """
                    
                    // Run the AWS CLI command to update the Glue job
                    bat updateJobCommand
                }
                }
            }
        }
    
    }
}
