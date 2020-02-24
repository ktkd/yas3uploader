# Overview:
Here is the small python3 app for upload any files to S3 object storage


# install:
`python3 setup.py install`

# configure:
<br> Create persistent config:
`yas3uploader -c -u https://SERVER_NAME:PORT -k KEY -i KEY_ID -b BUCKET_NAME`
<br> Then upload file:
yas3uploader -f FILE_TO_UPLOAD

<br> OR w/o create Persistent config

<br> Upload file:
`yas3uploader -f FILE_TO_UPLOAD -u https://SERVER_NAME:PORT -k KEY -i KEY_ID -b BUCKET_NAME`

# run for help:
`yas3uploader -h`

