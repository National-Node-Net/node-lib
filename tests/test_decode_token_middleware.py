# SPDX-License-Identifier: Apache-2.0
# Originally developed by Telicent Ltd.; subsequently adapted, enhanced, and maintained by the National Digital Twin Programme.


# Copyright (c) Telicent Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modifications made by the National Digital Twin Programme (NDTP)
# © Crown Copyright 2026. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the UK's Department for Business, Innovation, Science and Trade (BIST) as the governing entity.


import logging
import unittest
from unittest import mock

from ia_map_lib.exceptions import ConfigurationException
from ia_map_lib.middleware.decode_token import AccessMiddleware


class DecodeTokenTestCase(unittest.TestCase):

    def test_urls_must_be_set(self):
        self.assertRaises(ConfigurationException, AccessMiddleware, **{'app': None, 'jwt_header': None})

        mw = AccessMiddleware(app=None, jwt_header=None, jwks_url='https://example.com',
                              logger=logging.LoggerAdapter(logging.getLogger(), extra={}))
        self.assertEqual(mw.jwks_url, 'https://example.com')

        mw = AccessMiddleware(app=None, jwt_header=None, public_key_url='https://example.com/',
                              logger=logging.LoggerAdapter(logging.getLogger(), extra={}))
        self.assertEqual(mw.public_key_url, 'https://example.com')

    @mock.patch('ia_map_lib.middleware.decode_token.jwt')
    def test_validate_jwks_token(self, mock_jwt):
        mock_jwt.get_unverified_header.return_value = {'alg': 'abc'}
        mock_jwt.PyJWKClient.return_value.get_signing_key_from_jwt.return_value = mock.Mock()

        mw = AccessMiddleware(app=None, jwt_header=None, jwks_url='https://example.com/',
                              logger=logging.LoggerAdapter(logging.getLogger(), extra={}))
        mw.validate_token('123456')

        mock_jwt.get_unverified_header.assert_called_with('123456')
        mock_jwt.PyJWKClient.assert_called_with('https://example.com/')
        mock_jwt.decode.assert_called_with(
            '123456', mock_jwt.PyJWKClient.return_value.get_signing_key_from_jwt().key, algorithms=['abc']
        )

    @mock.patch('ia_map_lib.middleware.decode_token.requests')
    @mock.patch('ia_map_lib.middleware.decode_token.jwt')
    def test_validate_public_key_token(self, mock_jwt, mock_requests):
        mock_jwt.get_unverified_header.return_value = {'kid': 'abc', 'alg': 'def'}
        mock_requests.get.return_value = mock.Mock()

        mw = AccessMiddleware(app=None, jwt_header=None, public_key_url='https://example.com/',
                              logger=logging.LoggerAdapter(logging.getLogger(), extra={}))
        mw.validate_token('123456')

        mock_jwt.get_unverified_header.assert_called_with('123456')
        mock_requests.get.assert_called_with('https://example.com/abc')
        mock_jwt.decode.assert_called_with(
            '123456', mock_requests.get().text, algorithms=['def']
        )
