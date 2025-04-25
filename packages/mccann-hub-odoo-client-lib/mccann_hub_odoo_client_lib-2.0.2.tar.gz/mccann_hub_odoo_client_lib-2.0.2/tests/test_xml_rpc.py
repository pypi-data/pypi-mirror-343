# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2025 Jimmy McCann
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##############################################################################

import unittest
from unittest.mock import MagicMock, patch

from mccann_hub.odoolib import XmlRpcConnector


class TestXmlRpcConnector(unittest.TestCase):
    def setUp(self):
        self.hostname = "localhost"
        self.port = 8069
        self.version = "2"
        self.connector = XmlRpcConnector(self.hostname)

    def test_initialization(self):
        self.assertEqual(
            self.connector.url,
            f"http://{self.hostname}:{self.port}/xmlrpc/{self.version}",
        )
        self.assertEqual(
            self.connector._logger.name, "mccann_hub.odoolib.connector.xmlrpc"
        )
        self.assertIsNone(self.connector._transport)

    @patch("mccann_hub.odoolib.connector.xml_rpc.ServerProxy")
    def test_send(self, mock_server_proxy):
        mock_service = MagicMock()
        mock_method = MagicMock(return_value="mock_response")
        mock_service.some_method = mock_method
        mock_server_proxy.return_value = mock_service

        response = self.connector.send("common", "some_method", "arg1", "arg2")

        mock_server_proxy.assert_called_once_with(
            f"http://{self.hostname}:{self.port}/xmlrpc/{self.version}/common",
            transport=None,
        )
        mock_method.assert_called_once_with("arg1", "arg2")
        self.assertEqual(response, "mock_response")


if __name__ == "__main__":
    unittest.main()
