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

import mccann_hub.odoolib as odoolib


class TestAsyncSequenceFunctions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pass

    def _conn(self, protocol):
        return odoolib.get_connection(
            hostname="localhost",
            protocol=protocol,
            database="test",
            login="admin",
            password="a",
        )

    def _get_protocols(self):
        """Returns available protocols."""
        return ["xmlrpc", "jsonrpc"]

    async def test_simple_async(self):
        """Tests async read."""
        for protocol in self._get_protocols():
            connection = self._conn(protocol)

            res = await connection.get_model("res.users").read.async_(1)

            self.assertEqual(res["id"], 1)

    async def test_user_context_async(self):
        """Tests async user context retrieval."""
        for protocol in self._get_protocols():
            connection = self._conn(protocol)

            context = await connection.async_get_user_context()
            self.assertIsInstance(context, dict)
            self.assertIn("lang", context)
            self.assertIn("tz", context)

    async def test_search_count_async(self):
        """Tests async search and count."""
        for protocol in self._get_protocols():
            connection = self._conn(protocol)
            country_model = connection.get_model("res.country")

            de_country_ids = await country_model.search.async_(
                [("name", "ilike", "de")]
            )
            de_country_count = await country_model.search_count.async_(
                [("name", "ilike", "de")]
            )

            self.assertEqual(de_country_count, len(de_country_ids))


if __name__ == "__main__":
    unittest.main()
