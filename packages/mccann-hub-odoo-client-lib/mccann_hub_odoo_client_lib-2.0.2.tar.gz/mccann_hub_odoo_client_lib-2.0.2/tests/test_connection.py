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
from unittest.mock import MagicMock

from mccann_hub.odoolib.connection import Connection
from mccann_hub.odoolib.connector._connector import Connector
from mccann_hub.odoolib.model import Model


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.mock_connector = MagicMock(spec=Connector)
        self.connection = Connection(
            connector=self.mock_connector,
            database="test_db",
            login="admin",
            password="password",
        )

    def test_initialization(self):
        self.assertEqual(self.connection.database, "test_db")
        self.assertEqual(self.connection.login, "admin")
        self.assertEqual(self.connection.password, "password")
        self.assertIsNone(self.connection.user_context)

    def test_get_user_context(self):
        mock_model = MagicMock()
        mock_model.context_get.return_value = {"lang": "en_US"}
        self.connection.get_model = MagicMock(return_value=mock_model)

        context = self.connection.get_user_context()
        self.assertEqual(context, {"lang": "en_US"})
        self.assertEqual(self.connection.user_context, {"lang": "en_US"})
        self.connection.get_model.assert_called_once_with("res.users")
        mock_model.context_get.assert_called_once()

    def test_get_model(self):
        model_instance = self.connection.get_model("res.partner")
        self.assertIsInstance(model_instance, Model)
        self.assertEqual(model_instance.model_name, "res.partner")
        self.assertEqual(model_instance.connection, self.connection)


if __name__ == "__main__":
    unittest.main()
