pipeline {
    agent any

    environment {
        AWS_REGION="ap-south-1"
        LAMBDA_FUNCTION="LambdaFunctionOverHttps"
        S3_BUCKET_NAME="dev-ops-bkt"
        S3_KEY_NAME="lambda_package.zip"
    }

    stages {
        stage('Checkout code') {
           steps {
                checkout scm
            }
        }
        stage('Zip Lambda Code') {
            steps {
                sh'''
                    rm -f lambda_package.zip
                    zip lambda_package.zip lambda_handler.py
                '''
            }
        }
        stage('Upload Zip to S3') {
            steps {
                withAWS(credentials:'aws-cred', region:"${AWS_REGION}") {
                    sh '''
                        aws s3 cp lambda_package.zip s3://$S3_BUCKET_NAME/$S3_KEY_NAME
                    '''
                }
            }
        }
        stage('Deploying to Lambda from S3') {
            steps {
                withAWS(credentials:'aws-cred', region:"${AWS_REGION}") {
                    sh '''
                        aws lambda get-function --function-name $LAMBDA_FUNCTION
                        if [ 0 -eq $? ]; then
                            echo "Lambda exists → updating its code..."
                            aws lambda update-function-code \
                                --function-name $LAMBDA_FUNCTION \
                                --s3-bucket $S3_BUCKET_NAME \
                                --s3-key $S3_KEY_NAME
                        else
                            echo "Lambda does NOT exist → creating a new one..."
                            aws lambda create-function \
                                --function-name $LAMBDA_FUNCTION \
                                --runtime python3.9 \
                                --handler lambda_handler.lambda_handler \
                                --role arn:aws:iam::597727830496:role/lambda-apigateway-role \
                                --code S3Bucket=$S3_BUCKET_NAME,S3Key=$S3_KEY_NAME \
                                --package-type Zip \
                                --timeout 20 \
                                --memory-size 128
                        fi
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Something went wrong.'
        }
    }
}
