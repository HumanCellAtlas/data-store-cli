#!/usr/bin/env python3.6

"""
Run "pip install crcmod python-magic boto3" to install this script's dependencies.
"""
import argparse
import logging
import mimetypes
import os
import uuid

import boto3
from boto3.s3.transfer import TransferConfig
from io import open

from .packages.checksumming_io import ChecksummingBufferedReader, S3Etag


logging.basicConfig(level=logging.INFO)


def encode_tags(tags):
    return [dict(Key=k, Value=v) for k, v in tags.items()]


def _mime_type(filename):
    type_, encoding = mimetypes.guess_type(filename)
    if encoding:
        return encoding
    if type_:
        return type_
    raise RuntimeError("Can't discern mime type")


def _copy_from_s3(path, destination_bucket, s3, tx_cfg):
    bucket_end = path.find("/", 5)
    bucket_name = path[5: bucket_end]
    dir_path = path[bucket_end + 1:]

    src_bucket = s3.Bucket(bucket_name)
    file_uuids = []
    key_names = []
    logging.info("Key Names:")
    for obj in src_bucket.objects.filter(Prefix=dir_path):
        # Empty files with no name were throwing errors
        if obj.key == dir_path:
            continue

        logging.info(obj.key)

        file_uuids.append(str(uuid.uuid4()))
        key_names.append(obj.key)

    return file_uuids, key_names


def upload_to_cloud(files, staging_bucket, replica, from_cloud=False):
    """
    Upload files to cloud.

    :param files: If from_cloud, files is a aws s3 directory path to files with appropriate metadata uploaded.
                  Else, a list of binary files to upload.
    :param staging_bucket: The aws bucket to upload the files to.
    :param replica: The cloud replica to write to. One of 'aws', 'gc', or 'azure'. No functionality now.
    :return: a list of each file's unique key name.
    """
    tx_cfg = TransferConfig(multipart_threshold=S3Etag.etag_stride,
                            multipart_chunksize=S3Etag.etag_stride)
    s3 = boto3.resource("s3")
    destination_bucket = s3.Bucket(staging_bucket)
    file_uuids = []
    key_names = []

    if from_cloud:
        file_uuids, key_names = _copy_from_s3(files[0], destination_bucket, s3, tx_cfg)

    else:
        for raw_fh in files:
            with ChecksummingBufferedReader(raw_fh) as fh:
                file_uuid = str(uuid.uuid4())
                key_name = "{}/{}".format(file_uuid, os.path.basename(fh.raw.name))
                destination_bucket.upload_fileobj(fh, key_name, Config=tx_cfg)
                sums = fh.get_checksums()
                metadata = {
                    "hca-dss-s3_etag": sums["s3_etag"],
                    "hca-dss-sha1": sums["sha1"],
                    "hca-dss-sha256": sums["sha256"],
                    "hca-dss-crc32c": sums["crc32c"],
                    "hca-dss-content-type": _mime_type(fh.raw.name)
                }

                s3.meta.client.put_object_tagging(Bucket=destination_bucket.name,
                                                  Key=key_name,
                                                  Tagging=dict(TagSet=encode_tags(metadata))
                                                  )
                file_uuids.append(file_uuid)
                key_names.append(key_name)

    return file_uuids, key_names
