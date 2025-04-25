# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) Stephane Wirtel
# Copyright (C) 2011 Nicolas Vanhoren
# Copyright (C) 2011 OpenERP s.a. (<http://openerp.com>)
# Copyright (C) 2018 Odoo s.a. (<http://odoo.com>).
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
import random

import requests

from ._connector import Connector


class JsonRpcException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class JsonRpcConnector(Connector):
    """
    A type of connector that uses the JsonRPC protocol.
    """

    PROTOCOL = "jsonrpc"

    def __init__(self, hostname: str, port=8069, version="2.0"):
        """
        Initialize by specifying the hostname and the port.
        :param hostname: The hostname of the computer holding the instance of Odoo.
        :param port: The port used by the Odoo instance for JsonRPC (default to 8069).
        """
        super(JsonRpcConnector, self).__init__()
        self.url: str = "http://%s:%d/jsonrpc" % (hostname, port)
        self.version = version

    def send(self, service_name: str, method: str, *args):
        return self._json_rpc(
            "call", {"service": service_name, "method": method, "args": args}
        )

    def _json_rpc(self, fct_name, params):
        data = {
            "jsonrpc": self.version,
            "method": fct_name,
            "params": params,
            "id": random.randint(0, 1000000000),
        }

        try:
            result_req = requests.post(
                self.url,
                data=json.dumps(data),
                headers={
                    "Content-Type": "application/json",
                },
                # timeout=10 # ← sensible default
            )
            result_req.raise_for_status()
        except requests.RequestException as err:  # network / HTTP errors
            raise JsonRpcException({"code": -32000, "message": str(err)}) from err

        result = result_req.json()

        if result.get("error", None):
            raise JsonRpcException(result["error"])

        return result.get("result", False)
