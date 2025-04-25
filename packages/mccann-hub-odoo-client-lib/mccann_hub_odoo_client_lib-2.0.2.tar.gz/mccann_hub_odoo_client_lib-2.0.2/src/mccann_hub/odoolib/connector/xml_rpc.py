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

from typing import Optional
from xmlrpc.client import ServerProxy, Transport

from ._connector import Connector


class XmlRpcConnector(Connector):
    """
    A type of connector that uses the XMLRPC protocol.
    """

    PROTOCOL = "xmlrpc"

    def __init__(
        self,
        hostname: str,
        port=8069,
        version: Optional[str] = "2",
        transport: Optional[Transport] = None,
    ):
        """
        Initialize by specifying the hostname and the port.
        :param hostname: The hostname of the computer holding the instance of Odoo.
        :param port: The port used by the Odoo instance for XMLRPC (default to 8069).
        """
        super(XmlRpcConnector, self).__init__()
        self.url = (
            "http://%s:%d/xmlrpc" % (hostname, port)
            if version is None
            else "http://%s:%d/xmlrpc/%s" % (hostname, port, version)
        )
        self._transport = transport

    def send(self, service_name: str, method: str, *args):
        """
        Send a request to the specified service and method with the given arguments.

        :param service_name: The name of the service to call (e.g., 'common', 'object', etc.)
        :param method: The method name to call on the service
        :param args: Additional arguments to pass to the method
        :return: The result of the method call
        :raises: xmlrpc.client.Fault if the remote call fails
        """
        url = "%s/%s" % (self.url, service_name)
        service = ServerProxy(url, transport=self._transport)
        return getattr(service, method)(*args)
