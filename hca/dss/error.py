from ..util.exceptions import SwaggerAPIException
from .. import logger

class APIException(SwaggerAPIException):
    def __init__(self, *args, **kwargs):
        print(self.response.headers)
        if 'response' in kwargs:
            if kwargs['response']['headers']['AWS-Request-ID']:
                logger.error("%s", "AWS-Request-ID: {}".format(kwargs['response']['headers']["AWS-Request-ID"]))
        super(APIException, self).__init__(*args, **kwargs)
