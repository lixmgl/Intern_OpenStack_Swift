# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011,2012 Akira YOSHIYAMA <akirayoshiyama@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# This source code is based ./auth_token.py and ./ec2_token.py.
# See them for their copyright.

"""
Starting point for routing Cisco Token requests.

"""

import httplib
import json
import logging
from webob.dec import wsgify
from urlparse import urlparse
import hmac
from hashlib import sha1
from os.path import basename
from StringIO import StringIO
from time import gmtime, strftime, time
from urllib import quote, unquote
from urlparse import parse_qs

from swift.common import utils as swift_utils

PROTOCOL_NAME = "Cisco Token Authentication"
HTTP_UNAUTHORIZED = 401


class CiscoToken(object):
    """Auth Middleware that handles S3 authenticating client calls"""
    def __init__(self, app, conf):
        """ Common initialization code """

        self.logger = swift_utils.get_logger(conf, log_route='ciscoauth')

        self.logger.debug("Inside Cisco Token Factory" )
        self.app = app
        self.conf = conf

    #@webob.dec.wsgify(RequestClass=webob.exc.Request)
    # pylint: disable=R0914
    def __call__(self, env, start_response):

        """ Handle incoming request. Authenticate. And send downstream. """
        self.logger.debug("Inside Cisco Token Factory" )

        self.logger.debug("X-Auth-Token = %s" %env.get('HTTP_X_AUTH_TOKEN'))
        authtoken =  env.get('HTTP_X_AUTH_TOKEN')
        if authtoken:
           self.logger.debug("Auth Token  exist so  transfer to  next  level")
           return self.app(env, start_response)

        "get the account meta data"
	account = self._get_account(env)
        if not account:
            self.logger.debug("Invalid Account" )
            return self._invalid(env, start_response)	
        
        claim, expires = self._get_signature(env)
        if not claim:
            self.logger.debug("No Valid Claim is found. So passing it to next layer." )
            return self.app(env, start_response)
            #return self._invalid(env, start_response)
       
        if not expires:
            self.logger.debug("Invalid Expiration Time" )
            return self._invalid(env, start_response)

	key = self._get_key(env, account)
        if not key:
            self.logger.debug("Invalid Key" )
            return self._invalid(env, start_response)

        if env['REQUEST_METHOD'] == 'HEAD':
            hmac_val = self._get_hmac(env, expires, key,
                                      request_method='GET')

            self.logger.debug(" HMAC value = %s"%hmac_val )
            self.logger.debug(" claim value = %s"%claim )

            if claim  != hmac_val:
                hmac_val = self._get_hmac(env, expires, key,
                                          request_method='PUT')
                if claim  != hmac_val:
                    return self._invalid(env, start_response)
        else:
            hmac_val = self._get_hmac(env, expires, key)
            self.logger.debug(" HMAC value = %s"%hmac_val )
            self.logger.debug(" claim value = %s"%claim )

            if claim  != hmac_val:
                return self._invalid(env, start_response)

        env['swift.authorize'] = lambda req: None
        env['swift.authorize_override'] = True
        env['REMOTE_USER'] = '.wsgi.swifturl'
        def _start_response(status, headers, exc_info=None):
             if env['REQUEST_METHOD'] == 'GET':
                 already = False
                 for h, v in headers:
                     if h.lower() == 'content-disposition':
                         already = True
                         break
                 if not already:
                     headers.append(('Content-Disposition',
                         'attachment; filename=%s' %
                             (quote(basename(env['PATH_INFO'])))))
             return start_response(status, headers, exc_info)

        return self.app(env, _start_response)
	
    def _get_account(self, env):
        """ Returns just the account for the request, if it's an object GET, PUT, or HEAD request; otherwise, None is returned.
		:param env: The WSGI environment for the request.
		:returns: Account str or None.
	"""
        account = None
        if env['REQUEST_METHOD'] in ('GET', 'PUT', 'HEAD'):
            parts = env['PATH_INFO'].split('/', 4)
            # Must be five parts, ['', 'v1', 'a', 'c', 'o'], must be a v1
            # request, have account, container, and object values, and the
            # object value can't just have '/'s.
            if len(parts) >= 5 and not parts[0] and parts[1] == 'v1' and \
                    parts[2] and parts[3] and parts[4].strip('/'):
                account = parts[2]
        return account
	
    def _get_signature(self, env):

	claim = None
        expires = None        

        claim = env.get('HTTP_X_SIGNATURE')
        expires = env.get('HTTP_X_SIGNATURE_EXPIRES')

        self.logger.debug("X-Signature-Expires = %s" %expires)
        self.logger.debug("X-Signature = %s" %claim)

        if claim and expires :
           try: 
              expires = int(expires)
           except ValueError:
              self.logger.debug("invalid Expiration format" )
              expires = 0
           if expires < time():
              self.logger.debug("X-Signature-Expires < time" )
              expires = 0
           return claim, expires

        if env.get('QUERY_STRING'):
	   claim = None
           expires = None        
           qs = parse_qs(env.get('QUERY_STRING', ''))
           if 'signature' in qs:
               claim = qs['signature'][0]
           if 'signature_expires' in qs:
              try:
                 expires= int(qs['lexpires'][0])
              except ValueError:
                 self.logger.debug("invalid Expiration format" )
                 expires = 0
              if expires < time():
                 self.logger.debug("X-Signature-Expires < time" )
                 expires = 0 
           return claim, expires       

        return claim, expires       

    def _get_key(self, env, account):
        """
	Returns the X-Account-Meta-Temp-AES-Key header value for the
	account, or None if none is set.

	:param env: The WSGI environment for the request.
	:param account: Account str.
	:returns: X-Account-Meta-Temp-URL-Key str value, or None.
	"""
        key = None
        memcache = env.get('swift.cache')
        if memcache:
            key = memcache.get('temp-aes-key/%s' % account)
        if not key:
            #newenv = make_pre_authed_env(env, 'HEAD', '/v1/' + account,
            #                             self.agent)
            #newenv['CONTENT_LENGTH'] = '0'
            #newenv['wsgi.input'] = StringIO('')
            #key = [None]
            newenv = {'REQUEST_METHOD': 'HEAD', 'SCRIPT_NAME': '',
                      'PATH_INFO': '/v1/' + account, 'CONTENT_LENGTH': '0',
                      'SERVER_PROTOCOL': 'HTTP/1.0',
                      'HTTP_USER_AGENT': 'TempURL', 'wsgi.version': (1, 0),
                      'wsgi.url_scheme': 'http', 'wsgi.input': StringIO('')}
            for name in ('SERVER_NAME', 'SERVER_PORT', 'wsgi.errors',
                         'wsgi.multithread', 'wsgi.multiprocess',
                         'wsgi.run_once', 'swift.cache', 'swift.trans_id'):
                if name in env:
                    newenv[name] = env[name]

            newenv['swift.authorize'] = lambda req: None
            newenv['swift.authorize_override'] = True
            newenv['REMOTE_USER'] = '.wsgi.swifturl'
            key = [None]

            def _start_response(status, response_headers, exc_info=None):
                for h, v in response_headers:
                    self.logger.debug("Respone %s" %response_headers )
                    if h.lower() == 'x-account-meta-temp-aes-key':
                        key[0] = v

            self.app(newenv, _start_response)
            key = key[0]
            if key and memcache:
                memcache.set('temp-aes-key/%s' % account, key, timeout=60)
        return key

    def _get_hmac(self, env, expires, key, request_method=None):
        """
	Returns the hexdigest string of the HMAC-SHA1 (RFC 2104) for
	the request.

	:param env: The WSGI environment for the request.
	:param expires: Unix timestamp as an int for when the URL
	expires.
	:param key: Key str, from the X-Account-Meta-Temp-URL-Key of
	the account.
	:param request_method: Optional override of the request in
	the WSGI env. For example, if a HEAD
	does not match, you may wish to
	override with GET to still allow the
	HEAD.
	:returns: hexdigest str of the HMAC-SHA1 for the request.
	"""
        if not request_method:
            request_method = env['REQUEST_METHOD']


        #return hmac.new(key, '%s\n%s\n%s' % (request_method, expires,
        #    env['PATH_INFO']), sha1).hexdigest()

        parts = env['PATH_INFO'].split('/')
        # Must be five parts, ['', 'v1', 'a', 'c', 'o'], must be a v1
        # request, have account, container, and object values, and the
        # object value can't just have '/'s.
        path_info = '/%s/%s/%s/%s' %(parts[1], parts[2], parts[3], parts[4])
        self.logger.debug("Path Info: %s" %path_info)
        return hmac.new(key, '%s\n%s\n%s' % (request_method, expires,
            path_info), sha1).hexdigest()

    def _invalid(self, env, start_response):
        """
	Performs the necessary steps to indicate a WSGI 401
	Unauthorized response to the request.

	:param env: The WSGI environment for the request.
	:param start_response: The WSGI start_response hook.
	:returns: 401 response as per WSGI.
	"""
        self._log_request(env, HTTP_UNAUTHORIZED)
        body = '401 Unauthorized: URL is invalid\n'
        start_response('401 Unauthorized',
            [('Content-Type', 'text/plain'),
             ('Content-Length', str(len(body)))])
        if env['REQUEST_METHOD'] == 'HEAD':
            return []

        return [body]

    def _log_request(self, env, response_status_int):
        """
		Used when a request might not be logged by the underlying
        WSGI application, but we'd still like to record what
		happened. An early 401 Unauthorized is a good example of
		this.
		:param env: The WSGI environment for the request.
        :param response_status_int: The HTTP status we'll be replying
                                     to the request with.
        """
        the_request = quote(unquote(env.get('PATH_INFO') or '/'))
        if env.get('QUERY_STRING'):
            the_request = the_request + '?' + env['QUERY_STRING']
        client = env.get('HTTP_X_CLUSTER_CLIENT_IP')
        if not client and 'HTTP_X_FORWARDED_FOR' in env:
            # remote host for other lbs
            client = env['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
        if not client:
            client = env.get('REMOTE_ADDR')


        self.logger.debug('INVALID REQUST ')
        self.logger.debug(' '.join(quote(str(x)) for x in (
            client or '-',
            env.get('REMOTE_ADDR') or '-',
            strftime('%d/%b/%Y/%H/%M/%S', gmtime()),
            env.get('REQUEST_METHOD') or 'GET',
            the_request,
            env.get('SERVER_PROTOCOL') or '1.0',
            response_status_int,
            env.get('HTTP_REFERER') or '-',
            (env.get('HTTP_USER_AGENT') or '-') + ' TempURL',
            env.get('HTTP_X_SIGNATURE') or '-',
            env.get('HTTP_X_SIGNATURE_EXPIRES') or '-',
            '-',
            '-',
            '-',
            env.get('swift.trans_id') or '-',
            '-',
            '-',
        )))

def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def auth_filter(app):
        return CiscoToken(app, conf)
    return auth_filter
