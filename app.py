import boto3
from botocore.client import Config
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

BUCKET = "flock-fl-param"
BUCKET_REGION = "us-east-2"

s3 = boto3.client(
    's3',
    config=Config(signature_version="s3v4"),
    region_name=BUCKET_REGION
)


@app.post("/upload")
def upload():
    # Accepts a bucket and filename parameters in the body
    filename = request.json.get('filename')

    # Checks if the filename already exists in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=filename)
    if 'Contents' in response:
        return make_response(jsonify(error='File already exists!'), 400)

    # Creates a presigned URL for the client to upload the file
    url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': BUCKET,
            'Key': filename
        }
    )
    return jsonify(url=url)
