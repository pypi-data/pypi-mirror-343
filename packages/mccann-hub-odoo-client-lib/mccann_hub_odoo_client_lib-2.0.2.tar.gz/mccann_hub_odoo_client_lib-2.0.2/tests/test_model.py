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

from mccann_hub.odoolib.model import Model


class TestModel(unittest.TestCase):
    def setUp(self):
        self.mock_connection = MagicMock()
        self.mock_connection.database = "test_db"
        self.mock_connection.user_id = 1
        self.mock_connection.password = "pass"
        self.mock_connection.get_service.return_value.execute_kw = MagicMock()
        self.model = Model(self.mock_connection, "res.partner")

    def test_initialization(self):
        self.assertEqual(
            self.model._logger.name, "mccann_hub.odoolib.model.res.partner"
        )

    def test_proxy_method_call(self):
        self.mock_connection.get_service.return_value.execute_kw.return_value = [
            {"id": 1, "name": "John"}
        ]
        result = self.model.read([1])
        self.assertEqual(result, [{"id": 1, "name": "John"}])

    def test_proxy_method_call_list_ids(self):
        self.mock_connection.get_service.return_value.execute_kw.return_value = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"},
        ]
        result = self.model.read([1, 2])
        self.assertEqual(result, [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}])

    def test_proxy_method_call_id_not_found(self):
        self.mock_connection.get_service.return_value.execute_kw.return_value = []
        result = self.model.read([999])
        self.assertFalse(result)

    def test_search_read(self):
        self.model.search = MagicMock(return_value=[1])
        self.model.read = MagicMock(return_value=[{"id": 1, "name": "X"}])
        result = self.model.search_read([("is_company", "=", True)], ["name"])
        self.assertEqual(result, [{"id": 1, "name": "X"}])

    def test_search_read_no_result(self):
        self.model.search = MagicMock(return_value=[])
        result = self.model.search_read([("is_company", "=", False)])
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
