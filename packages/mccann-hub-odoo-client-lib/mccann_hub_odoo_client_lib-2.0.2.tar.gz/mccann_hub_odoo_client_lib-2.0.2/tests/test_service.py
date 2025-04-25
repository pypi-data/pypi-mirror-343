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

from mccann_hub.odoolib.service import Service


class TestService(unittest.TestCase):
    def setUp(self):
        self.mock_sender = MagicMock()
        self.service_name = "common"
        self.service = Service(self.mock_sender, self.service_name)

    def test_initialization(self):
        self.assertEqual(self.service._logger.name, "mccann_hub.odoolib.service.common")

    def test_sync_method_call(self):
        self.mock_sender.send.return_value = "success"

        result = self.service.some_method("arg1", 42)

        self.mock_sender.send.assert_called_once_with(
            "common", "some_method", "arg1", 42
        )
        self.assertEqual(result, "success")

    def test_sync_method_caching_and_multiple_calls(self):
        self.mock_sender.send.side_effect = ["res1", "res2"]

        result1 = self.service.foo(1)
        result2 = self.service.foo(2)

        self.assertEqual(result1, "res1")
        self.assertEqual(result2, "res2")
        self.assertEqual(self.mock_sender.send.call_count, 2)

    def test_method_name_reflection(self):
        proxy = self.service.do_something
        self.assertTrue(callable(proxy))
        self.assertTrue(hasattr(proxy, "async_"))


if __name__ == "__main__":
    unittest.main()
