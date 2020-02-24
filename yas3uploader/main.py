#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=E1101
"""
Upload file to S3
"""
import hashlib
import argparse
import sys
import json
import os
import boto3
from boto3.s3.transfer import TransferConfig
S3_CFG = TransferConfig(multipart_threshold=5 * 1024 ** 3)
JSON_CFG = os.path.expanduser('~/.s3_uplconfig.json')


def create_parser():
    """
    argument parser
    """
    parser = argparse.ArgumentParser(
        prog='send_s3',
        description='send file to S3 and return a link',
        epilog='(c) WTFPL 1.0',
        add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str)
    group.add_argument('-c', '--create-config', action="store_true")

    try:
        with open(JSON_CFG) as config_file:
            data = json.load(config_file)
        url = data['url']
        bucket = data['bucket']
        key = data['key']
        keyid = data['keyid']
    except Exception as err:
        print(f'Problem with config file  {err}')
        parser.add_argument('-u', '--url', type=str, required=1)
        parser.add_argument('-k', '--key', type=str, required=1)
        parser.add_argument('-i', '--keyid', type=str, required=1)
        parser.add_argument('-b', '--bucket', type=str, required=1)
    else:
        parser.add_argument('-u', '--url', type=str, default=url)
        parser.add_argument('-k', '--key', type=str, default=key)
        parser.add_argument('-i', '--keyid', type=str, default=keyid)
        parser.add_argument('-b', '--bucket', type=str, default=bucket)
    return parser


def upload(file, url, key, keyid, bucket):
    """
    upload to s3 function
    :param file: file to upload
    :param url: url with s3 server
    :param key: username for s3
    :param keyid: password for s3
    :param bucket: s3 bucket
    :return:
    """
    s_3 = boto3.resource('s3',
                         endpoint_url=url,
                         aws_secret_access_key=key,
                         aws_access_key_id=keyid,
                         region_name="auto")
    try:
        with open(file, "rb") as upload_file:
            filehash = hashlib.sha256(upload_file.read()).hexdigest()
            s_3.Bucket(bucket).upload_file(file, f'{filehash}-{file}', Config=S3_CFG)
    except Exception as err:
        return err
    else:
        return f'Uploaded file url: {url}/{bucket}/{filehash}-{file}'


def create_config(url, key, keyid, bucket):
    """
    create config file
    :param url: url with s3 server
    :param key: username for s3
    :param keyid: password for s3
    :param bucket: s3 bucket
    :return:
    """
    data = {}
    data["url"] = url
    data["bucket"] = bucket
    data["key"] = key
    data["keyid"] = keyid
    try:
        with open(JSON_CFG, 'w') as config_file:
            json.dump(data, config_file)
    except Exception as err:
        return err
    else:
        return data


def main():
    """
    some magic
    :return:
    """
    parser = create_parser()
    n_s = parser.parse_args(sys.argv[1:])
    if n_s.create_config:
        print(create_config(n_s.url, n_s.key, n_s.keyid, n_s.bucket))
    if n_s.file:
        print(upload(n_s.file, n_s.url, n_s.key, n_s.keyid, n_s.bucket))


if __name__ == '__main__':
    main()
