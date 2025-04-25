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

"""
Odoo Client Library

Home page: http://pypi.python.org/pypi/odoo-client-lib
Code repository: https://github.com/odoo/odoo-client-lib
"""
from .connection import Connection
from .connector import (JsonRpcConnector, JsonRpcsConnector, XmlRpcConnector,
                        XmlRpcsConnector)


def get_connector(hostname: str, protocol="xmlrpc", port=8069):
    """
    A shortcut method to easily create a connector to a remote server using XMLRPC.

    :param hostname: The hostname to the remote server.
    :param protocol: The name of the protocol, must be "xmlrpc", "xmlrpcs", "jsonrpc" or "jsonrpcs".
    :param port: The number of the port. Defaults to 8069.
    """
    match protocol:
        case "xmlrpc":
            return XmlRpcConnector(hostname, port)
        case "xmlrpcs":
            return XmlRpcsConnector(hostname, port)
        case "jsonrpc":
            return JsonRpcConnector(hostname, port)
        case "jsonrpcs":
            return JsonRpcsConnector(hostname, port)
        case _:
            raise ValueError("You must choose xmlrpc, xmlrpcs, jsonrpc or jsonrpcs")

def get_connection(
    hostname: str,
    protocol="xmlrpc",
    port=8069,
    database=None,
    login=None,
    password=None,
    user_id=None,
):
    """
    A shortcut method to easily create a connection to a remote Odoo server.

    :param hostname: The hostname to the remote server.
    :param protocol: The name of the protocol, must be "xmlrpc", "xmlrpcs", "jsonrpc" or "jsonrpcs".
    :param port: The number of the port. Defaults to 8069.
    :param connector: A valid Connector instance to send messages to the remote server.
    :param database: The name of the database to work on.
    :param login: The login of the user.
    :param password: The password of the user.
    :param user_id: The user id is a number identifying the user. This is only useful if you
    already know it, in most cases you don't need to specify it.
    """
    return Connection(
        get_connector(hostname, protocol, port), database, login, password, user_id
    )
