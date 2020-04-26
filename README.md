# image-to-svg
Create a Serverless Image to SVG Conversion tool which is compatible with Cricut!

This will include a single run script which will allow you to deploy a serverless system which will
enable anyone who visits your page to convert any JPG or PNG into an SVG compatible with Cricut.

Manually deployable, the terraform is a work in progress.


# Manual Installation

First, you'll need an AWS Account. Configure it and your credentials, and get ready for deployment. Start with the S3 Bucket.

Deploy the bucket and set it up for Static Website hosting.

From there, go to IAM. You'll need to create three roles, one for each lambda function.

## Role 1: svg-converter-lambda-role

Create a Lambda role with two policies:

1) The AWS CloudWatchLogsFullAccess policy
2) a custom policy called `svg-converter-bucket-policy` with the following policy document:
```

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketPolicy",
                "s3:GetObject",
                "s3:PutObject",
            ],
            "Resource": [
                "arn:aws:s3:::<your bucket name>",
                "arn:aws:s3:::<your bucket name>/",
                "arn:aws:s3:::<your bucket name>/*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:HeadBucket"
            ],
            "Resource": "*"
        }
    ]
}


```

# Role 2: The generate_post_url_role

Again, a lambda role with the CloudWatch Logs access, and the `generate_post_url_policy`:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [

                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<your bucket name>"

            ]
        }
    ]
}



```

# Role 3: delete_bucket_file role

Include that Cloudwatch logs policy, and create a custom one which includes:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [

                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::<your bucket name>"

            ]
        }
    ]
}



```

Once done, `cd` into the processfunction directory, and run

`mkvirutalenv processfunction --no-site-packages`

`workon processfunction`

`pip3 install -r requirements.txt`

Modify the config.yaml file appropriately

`lambda deploy`

Repeat this process for the posturlgenerator and deletefunction directories.

Your lambda functions are now online.


Now, on to API Gateway!

Create two APIs, one which points at the processfunction lambda function, the other to the posturlgenerator lambda function.

For the API for the posturlgenerator function, create a GET method and in the Integration request, under Mapping Templates, add a Content-Type of application/json, with the following value:

```

{
"operation":"$input.params('operation')",
"fileName":"$input.params('fileName')"
}

```

Enable CORS and deploy it.


In the processfunction API, create a GET method, modify the Mapping template to include a Content-Type of application/json with:

```
{
"bucketName":"$input.params('bucketName')",
"fileName":"$input.params('fileName')"
}
```

Once you have your final API Gateway endpoints, go to the `index.html` file in the root of this directory, modify the `upload_download_url` and `process_url` variables to match their respective API Gateway Endpoints, then upload it to your S3 bucket. In your bucket, make sure the file is public. You can then access it from your browser and begin processing JPGs and PNGs into SVGs!
