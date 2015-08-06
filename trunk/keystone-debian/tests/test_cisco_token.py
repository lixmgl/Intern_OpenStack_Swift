#!/usr/bin/env python

import json

import nose
import webob
import hmac
import unittest

from hashlib import sha1
from time import gmtime, strftime, time
from contextlib import contextmanager

from webob import Request, Response

from keystone import test

try:
    # NOTE(chmou): We don't want to force to have swift installed for
    # unit test so we skip it we have an ImportError.
    from keystone.middleware import cisco_token
    skip = False
except ImportError:
    skip = True
    
class FakeMemcache(object):

    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, timeout=0):
        self.store[key] = value
        return True

    def incr(self, key, timeout=0):
        self.store[key] = self.store.setdefault(key, 0) + 1
        return self.store[key]

    @contextmanager
    def soft_lock(self, key, timeout=0, retries=5):
        yield True

    def delete(self, key):
        try:
            del self.store[key]
        except Exception:
            pass
        return True



class FakeApp(object):

    def __init__(self, status_headers_body_iter=None):
        self.calls = 0
        self.status_headers_body_iter = status_headers_body_iter
        if not self.status_headers_body_iter:
            self.status_headers_body_iter = iter([('404 Not Found', {
                'x-test-header-one-a': 'value1',
                'x-test-header-two-a': 'value2',
                'x-test-header-two-b': 'value3'}, '')])
        self.request = None

    def __call__(self, env, start_response):
        self.calls += 1
        self.request = Request.blank('', environ=env)
        if 'swift.authorize' in env:
            resp = env['swift.authorize'](self.request)
            if resp:
                return resp(env, start_response)
        status, headers, body = self.status_headers_body_iter.next()
        return Response(status=status, headers=headers,
                        body=body)(env, start_response)


class CiscoTokenMiddlewareTest(unittest.TestCase):
    def setUp(self, expected_env=None):
        # We probably going to end-up with the same strategy than
        # test_swift_auth when this is decided.
        if skip:
            raise nose.SkipTest('no swift detected')

        self.app = FakeApp()
        #self.auth = tempauth.filter_factory({})(self.app)
        self.signedurl = cisco_token.filter_factory({})(self.app)

    def _make_request(self, path, **kwargs):
        req = Request.blank(path, **kwargs)
        req.environ['swift.cache'] = FakeMemcache()
        return req

    def test_passthrough(self):
        resp = self._make_request('/v1/a/c/o').get_response(self.signedurl)
        self.assertEquals(resp.status_int, 404)
        self.assertTrue('URL is invalid' not in resp.body)
    """
    def test_get_valid_with_querystring(self):
        method = 'GET'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        sig = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path,
            environ={'QUERY_STRING':
                       'signature=%s&signature_expires=%s' % (sig, expires)})
        req.environ['swift.cache'].set('temp-aes-key/a', key)
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 404)
        self.assertEquals(resp.headers['content-disposition'],
                          'attachment; filename=o')
    """
    def test_get_valid_with_header(self):
        method = 'GET'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        claim = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path)

        req.headers['X-Signature-Expires'] = expires
        req.headers['X-Signature'] = claim
          
        req.environ['swift.cache'].set('temp-aes-key/a', key)
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 404)
        self.assertEquals(resp.headers['content-disposition'],
                          'attachment; filename=o')


    def test_put_not_allowed_by_get(self):
        method = 'PUT'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        claim = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path)
        req.headers['X-Signature-Expires'] = expires
        req.headers['X-Signature'] = claim
        req.environ['swift.cache'].set('temp-aes-key/a', key)
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 401)
        self.assertTrue('URL is invalid' in resp.body)

    def test_put_valid(self):
        method = 'PUT'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        claim = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path)
        req.method = 'PUT'
        req.headers['X-Signature-Expires'] = expires
        req.headers['X-Signature'] = claim
        req.environ['swift.cache'].set('temp-aes-key/a', key)
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 404)

    def test_put_not_allowed_by_get(self):
        method = 'GET'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        claim = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path)
        req.method = 'PUT'
        req.headers['X-Signature-Expires'] = expires
        req.headers['X-Signature'] = claim
        req.environ['swift.cache'].set('temp-aes-key/a', key)
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 401)
        self.assertTrue('URL is invalid' in resp.body)

    def test_X_Auth_Token_path_request(self):
        method = 'GET'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        claim = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path)
        req.method = 'GET'
        req.headers['X-Auth-Token'] = 'cd76df5f2e6b4ef285b0b9ff6840ab74'
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 404)

    def test_invalid_key(self):
        method = 'GET'
        expires = int(time() + 86400)
        path = '/v1/a/c/o'
        key = 'abc'
        hmac_body = '%s\n%s\n%s' % (method, expires, path)
        claim = hmac.new(key, hmac_body, sha1).hexdigest()
        req = self._make_request(path)

        req.headers['X-Signature-Expires'] = expires
        req.headers['X-Signature'] = claim
          
        req.environ['swift.cache'].set('temp-aes-key/a', key + 'hack')
        resp = req.get_response(self.signedurl)
        self.assertEquals(resp.status_int, 401)
        self.assertTrue('URL is invalid' in resp.body)

if __name__ == '__main__':
    unittest.main()      
      
