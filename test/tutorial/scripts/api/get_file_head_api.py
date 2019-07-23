from hca import HCAConfig
from hca.dss import DSSClient
import sys
import csv
import json
import pprint

hca_config = HCAConfig()
hca_config[
    "DSSClient"
].swagger_url = f"https://dss.data.humancellatlas.org/v1/swagger.json"
dss = DSSClient(config=hca_config)

print(dss.head_file(uuid="666ff3f0-67a1-4ead-82e9-3f96a8c0a9b1", replica="aws"))
