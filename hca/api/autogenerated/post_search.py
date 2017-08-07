"""This file is autogenerated according to HCA api spec. Don't modify."""
from ...added_command import AddedCommand

class PostSearch(AddedCommand):
    """Class containing info to reach the get endpoint of files."""

    @classmethod
    def _get_base_url(cls):
        return "https://hca-dss.czi.technology/v1"

    @classmethod
    def _get_endpoint_info(cls):
        return {'seen': False, 'body_params': {}, 'positional': [], 'options': {}, 'description': 'Accepts Elasticsearch JSON query and returns matching bundle identifiers\n'}
