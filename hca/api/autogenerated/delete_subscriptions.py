"""This file is autogenerated according to HCA api spec. Don't modify."""
from ...added_command import AddedCommand

class DeleteSubscriptions(AddedCommand):
    """Class containing info to reach the get endpoint of files."""

    @classmethod
    def _get_base_url(cls):
        return "https://hca-dss.czi.technology/v1"

    @classmethod
    def _get_endpoint_info(cls):
        return {'seen': False, 'body_params': {}, 'positional': [{'argument': 'uuid', 'required': True, 'required_for': ['/subscriptions/{uuid}'], 'description': 'A RFC4122-compliant ID for the subscription.', 'type': 'string', 'format': None, 'pattern': '[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}'}], 'options': {'replica': {'array': False, 'required': True, 'required_for': ['/subscriptions/{uuid}'], 'description': 'Replica to delete from. Can be one of aws, gcp, or azure.', 'type': 'string', 'format': None, 'pattern': None, 'metavar': None, 'in': 'query', 'hierarchy': ['replica']}}, 'description': 'Delete a registered event subscription. The associated query will no longer trigger a callback\nif a matching document is added to the system.\n'}
