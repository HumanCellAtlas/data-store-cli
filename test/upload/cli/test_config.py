from argparse import Namespace

import responses
import boto3

from ... import CapturingIO
from .. import UploadTestCase, mock_current_upload_area

import hca

from hca.upload.cli.list_area_command import ListAreaCommand


class TestConfig(UploadTestCase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.deployment_stage = 'test'
        self.upload_bucket_name = 'org-humancellatlas-upload-{}'.format(self.deployment_stage)
        self.upload_bucket = boto3.resource('s3').Bucket(self.upload_bucket_name)
        self.upload_bucket.create()

        self.area = mock_current_upload_area()
        self.upload_bucket.Object('/'.join([self.area.uuid, 'file1.fastq.gz'])).put(Body="foo")

    @responses.activate
    def test_we_access_hca_url_by_default(self):

        list_url = 'https://upload.{stage}.data.humancellatlas.org/v1/area/{uuid}/files_info'.format(
            stage=self.deployment_stage,
            uuid=self.area.uuid)
        responses.add(responses.PUT, list_url, json={}, status=200)

        with CapturingIO('stdout') as stdout:
            ListAreaCommand(Namespace(long=True))

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, list_url)

    @responses.activate
    def test_we_access_configured_upload_service_api_endpoint(self):
        config = hca.get_config()
        config.upload.upload_service_api_url_template = "http://upload.example.com/v1"
        config.save()

        list_url = 'http://upload.example.com/v1/area/{uuid}/files_info'.format(uuid=self.area.uuid)
        responses.add(responses.PUT, list_url, json={}, status=200)

        with CapturingIO('stdout') as stdout:
            ListAreaCommand(Namespace(long=True))

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, list_url)
