from flask import Flask, render_template, request
import boto3
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ========================
# Get AWS Credentials from user input or environment
# ========================
ACCESS_KEY =  # write your credential here
SECRET_KEY =  # write your credential here
S3_REGION = 'us-east-1'  # or let user input this too
S3_BUCKET = f"photo-gallery-bucket-{ACCESS_KEY.lower()[-6:]}"  # make unique bucket name using user's key

#/////////////////////////////////////////////////
def make_bucket_public(bucket_name):
    public_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }]
    }

    s3.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(public_policy)
    )


# ========================
# Create AWS S3 Client
# ========================
s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=S3_REGION
)

# ========================
# Create S3 Bucket if not exists
# ========================
def create_bucket(bucket_name):
    existing_buckets = s3.list_buckets()
    if not any(bucket['Name'] == bucket_name for bucket in existing_buckets['Buckets']):
        if S3_REGION == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': S3_REGION}
            )
        print(f"Bucket '{bucket_name}' created successfully!")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

create_bucket(S3_BUCKET)
make_bucket_public(S3_BUCKET)


# ========================
# Flask Routes
# ========================

@app.route('/')
def index():
    images = s3.list_objects_v2(Bucket=S3_BUCKET).get('Contents', [])
    image_urls = [f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{img['Key']}" for img in images]
    return render_template('index.html', images=image_urls)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    filename = secure_filename(file.filename)
    
    # Upload file to S3 with public-read permission
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        filename,
        ExtraArgs={
            'ContentType': file.content_type,  # Maintain the content type of the file
            'ACL': 'public-read'  # This ensures that the file is publicly accessible
        }
    )
    
    return 'File uploaded successfully! <a href="/">Go back to gallery</a>'

    


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    s3.delete_object(Bucket=S3_BUCKET, Key=key)
    return 'Photo deleted! <a href="/">Go back to gallery</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
