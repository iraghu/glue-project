pipeline {
    agent any
 
    environment {
        AWS_REGION = 'ap-south-1'
        S3_BUCKET = 'gluerawbucket'
        GLUE_JOB_NAME = 'RawToRefinedScript-cicdJob'
        GLUE_SCRIPT_PATH = 'glue_scripts\\LandingToRawScript.py'
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
                withAWS(credentials: 'credentials', region: "${AWS_REGION}") {
                    bat '''
                    aws glue update-job --job-name ${GLUE_JOB_NAME} --job-update '
                    {
                        "Command": {
                            "Name": "glueetl",
                            "ScriptLocation": "s3://${S3_BUCKET}/glue-scripts/your-script.py",
                            "PythonVersion": "3"
                        }
                    }'
                    '''
                }
            }
        }
 
        stage('Trigger Glue Job') {
            steps {
                withAWS(credentials: 'aws-glue-credentials', region: "${AWS_REGION}") {
                    sh "aws glue start-job-run --job-name ${GLUE_JOB_NAME}"
                }
            }
        }
    }
}
