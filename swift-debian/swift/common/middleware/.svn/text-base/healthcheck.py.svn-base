# Copyright (c) 2010-2012 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# #######################################################
# --Autumn Wang 2012/05/03
# Added the realhealthcheck API for functional monitoring 
#
#

from webob import Request, Response
from swift.common.client import Connection, ClientException


class HealthCheckMiddleware(object):
    """
    Healthcheck middleware used for monitoring.

    If the path is /healthcheck, it will respond with "OK" in the body
    """

    def __init__(self, app, conf, *args, **kwargs):
        self.app = app
        self.auth_url = conf.get('auth_url', 'http://localhost:8080/v1.0')
        self.check_account = conf.get('check_account', 'healthcheck')
        self.check_secrete = conf.get('check_secrete', 'health@check123')
        self.check_file = conf.get('check_file', 'healthcheck.txt')

    def GET(self, req):
        """Returns a 200 response with "OK" in the body."""
        return Response(request=req, body="OK", content_type="text/plain")

    def __real_check__(self, req):
        """
        The real health check for swift object store:
        It will simulate the client to upload and download a file so that all the layers are checked
        """
        try:
            swift_client = Connection(self.auth_url, self.check_account, self.check_secrete, retries=2)
            swift_client.put_object(self.check_account, self.check_file, 'OK')
            (head, content) = swift_client.get_object(self.check_account, self.check_file)
            return Response(request=req, body= content, content_type="text/plain")
        except ClientException as ce:
            body = "Object not found : %s/%s\n" % (self.check_account, self.check_file)
            return Response(request=req, body = body, status = ce.http_status, content_type="text/plain")
        except Exception as e:
            return Response(request=req, body= e.message, status = "506 Other Exception", content_type="text/plain")
        
    def __call__(self, env, start_response):
        req = Request(env)
        if req.path == '/healthcheck':
            return self.GET(req)(env, start_response)
        elif req.path == '/realhealthcheck':
            return self.__real_check__(req)(env, start_response)
        else:
            return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    def healthcheck_filter(app):
        return HealthCheckMiddleware(app, conf)
    return healthcheck_filter
