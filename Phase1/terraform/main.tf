provider "aws" {
  region = var.region
}

####Create the S3 Bucket
#Create bucket with provided name in the vars file
#apply the appropriate policy to it
#Static website hosting
#save the ARN


####Create the role for Lambda

############################################
# IAM - Role & Permissions for our lambda
############################################

resource "aws_iam_role" "lambda_role" {
  name = "serverless_website_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

}


#and here we need to modify that resource for s3 to be the ${s3.arn}
resource "aws_iam_role_policy" "lambda_policy" {
  name = "serverless_lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
          "Effect": "Allow",
          "Action": "s3:*",
          "Resource": "*"
        }
    ]
}
EOF

}


####Prepare lambda functions
##something like pip3 install virtualenv && export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 && source `which virtualenvwrapper.sh` && mkvirtualenv testenv --no-site-packages && workon testenv && cd ~/Github/image-to-svg/posturlgenerator/ && pip3 install -r requirements.txt

####Deploy Lambda Functions
#do a terraform deployment of the lambda functions so that the api gateway can more easily reference it

####Set up API Gateways

#deploy the two api gateways, modify CORS, spit out the output of the gateway endpoints, instruct user to modify html file in two locations
