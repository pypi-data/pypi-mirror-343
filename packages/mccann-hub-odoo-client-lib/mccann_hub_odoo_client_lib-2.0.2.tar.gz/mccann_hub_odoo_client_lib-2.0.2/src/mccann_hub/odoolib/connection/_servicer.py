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

import logging
from typing import Optional

from ..connector._connector import Connector
from ..service import Service
from .authentication_error import AuthenticationError


class Servicer(object):

    def __init__(
        self,
        connector: Connector,
        database: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        user_id: Optional[int] = None,
    ):
        self._logger = logging.getLogger(
            f"{str.join('.', __name__.split('.')[:-1])}.{connector.PROTOCOL}"
        )
        self.connector = connector
        self.set_login_info(database, login, password, user_id)

    def set_login_info(
        self,
        database: Optional[str],
        login: Optional[str],
        password: Optional[str],
        user_id: Optional[int] = None,
    ):
        """
        Set login information after the initialisation of this object.

        :param connector: A valid Connector instance to send messages to the remote server.
        :param database: The name of the database to work on.
        :param login: The login of the user.
        :param password: The password of the user.
        :param user_id: The user id is a number identifying the user. This is only useful if you
        already know it, in most cases you don't need to specify it.
        """
        self.database, self.login, self.password = database, login, password

        self.user_id = user_id

    def _check_logged_in(self, force=True) -> bool:
        """
        Checks if this Connection was already validated previously.

        :param force: Force to re-check even if this Connection was already validated previously.
        Default to True.
        """
        if self.user_id and not force:
            return True

        if not self.database or not self.login or self.password is None:
            raise AuthenticationError("Credentials not provided")

        return False

    def check_login(self, force=True):
        """
        Checks that the login information is valid. Throws an AuthenticationError if the
        authentication fails.

        :param force: Force to re-check even if this Connection was already validated previously.
        Default to True.
        """
        if self._check_logged_in(force):
            return

        # TODO use authenticate instead of login
        self.user_id = self.get_service("common").login(
            self.database, self.login, self.password
        )
        if not self.user_id:
            raise AuthenticationError("Authentication failure")
        self._logger.debug("Authenticated (sync) with user id %s", self.user_id)

    async def async_check_login(self, force=True):
        """
        Checks that the login information is valid. Throws an AuthenticationError if the
        authentication fails.

        :param force: Force to re-check even if this Connection was already validated previously.
        Default to True.
        """
        if self._check_logged_in(force):
            return

        # TODO use authenticate instead of login
        self.user_id = await self.get_service("common").login.async_(
            self.database, self.login, self.password
        )
        if not self.user_id:
            raise AuthenticationError("Authentication failure")
        self._logger.debug("Authenticated (async) with user id %s", self.user_id)

    def get_service(self, service_name: str) -> Service:
        """
        Returns a Service instance to allow easy manipulation of one of the services offered by the remote server.
        Please note this Connection instance does not need to have valid authentication information since authentication
        is only necessary for the "object" service that handles models.

        :param service_name: The name of the service.
        """
        return self.connector.get_service(service_name)
