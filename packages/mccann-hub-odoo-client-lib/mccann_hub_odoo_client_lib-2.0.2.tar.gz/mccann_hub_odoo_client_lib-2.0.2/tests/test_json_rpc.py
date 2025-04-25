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

import json
import unittest
from unittest.mock import MagicMock, patch

from mccann_hub.odoolib.connector import JsonRpcConnector, JsonRpcException


class TestJsonRpcConnector(unittest.TestCase):
    def setUp(self):
        self.hostname = "localhost"
        self.port = 8069
        self.version = "2.0"
        self.connector = JsonRpcConnector(self.hostname, self.port, self.version)

    def test_initialization(self):
        self.assertEqual(
            self.connector.url, f"http://{self.hostname}:{self.port}/jsonrpc"
        )
        self.assertEqual(self.connector.version, self.version)
        self.assertEqual(
            self.connector._logger.name, "mccann_hub.odoolib.connector.jsonrpc"
        )

    @patch("mccann_hub.odoolib.connector.json_rpc.requests.post")
    def test_send_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "mock_response"}
        mock_post.return_value = mock_response

        response = self.connector.send("common", "some_method", "arg1", "arg2")

        _, called_kwargs = mock_post.call_args
        sent_data = json.loads(
            called_kwargs["data"]
        )  # Convert JSON string back to dictionary

        # Verify all expected fields except 'id'
        self.assertEqual(sent_data["jsonrpc"], self.version)
        self.assertEqual(sent_data["method"], "call")
        self.assertEqual(
            sent_data["params"],
            {"service": "common", "method": "some_method", "args": ["arg1", "arg2"]},
        )

        # Ensure 'id' exists and is an integer
        self.assertIn("id", sent_data)
        self.assertIsInstance(sent_data["id"], int)

        self.assertEqual(response, "mock_response")

    @patch("mccann_hub.odoolib.connector.json_rpc.requests.post")
    def test_send_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "mock_error"}
        mock_post.return_value = mock_response

        with self.assertRaises(JsonRpcException) as context:
            self.connector.send("common", "some_method", "arg1", "arg2")

        self.assertEqual(str(context.exception), "'mock_error'")


if __name__ == "__main__":
    unittest.main()
