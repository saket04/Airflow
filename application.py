import os,time,sys
from flask import Flask, render_template, request, redirect, send_file
import boto3
import configparser
import multiprocessing
all_processes = []
UPLOAD_FOLDER = "uploads"
BUCKET = "aws-b2b-python-demo"
aws_access_key_id = '###############'
aws_secret_access_key = '#########################'
region = 'us-east-1'

def inc_cpu(val):
    while val:
        range(10000)  # some payload code
        time.sleep(1.0)

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,
    region_name= region)

    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,
    region_name= region)

    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)
    return output

def list_files(BUCKET):
    """
    Function to list files in a given S3 bucket
    """
    import boto3
    contents = []
    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,
    region_name= region)
    my_bucket = s3.Bucket(BUCKET)
    try:
        for file in my_bucket.objects.all():
            print(file.key)
            contents.append(file)
    except Exception as e:
        pass
    return contents


app = Flask(__name__)

@app.route('/')
def entry_point():
    return render_template('main.html')

@app.route("/storage")
def storage():
    contents = list_files(BUCKET)
    print(contents[0])
    return render_template('myStorage.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)
        return redirect("/storage")


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

@app.route('/inc_cpu')
def increase():
    val = True
    for i in range(0, 500):
        process = multiprocessing.Process(target=inc_cpu, args=(val,))
        process.start()
        process.join()
        all_processes.append(process)
    return "The CPU Value is increasing"

@app.route('/dec_cpu')
def decrease():
    print("The all process",len(all_processes))
    if len(all_processes) != 0:

        for process in all_processes:
            process.terminate()
    return "The CPU Value is decreasing"


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000,debug=True)


