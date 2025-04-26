#
# Copyright (C) 2025  Leo P. Singer <leo.singer@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from time import time

import jwt
from requests.auth import AuthBase


class SciTokenAuth(AuthBase):
    def __init__(self, path):
        self.path = path
        self.refresh()

    def refresh(self):
        with open(self.path) as f:
            result = f.read()
        self.token = result.strip()

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class SciTokenReloadingAuth(SciTokenAuth):
    def __init__(self, path, reload_timeout=0):
        self.reload_timeout = reload_timeout
        super().__init__(path)

    def refresh(self):
        super().refresh()
        self.expires_at = (
            jwt.decode(self.token, options={"verify_signature": False})["exp"]
            - self.reload_timeout
        )

    def expired(self):
        return time() >= self.expires_at

    def __call__(self, request):
        if self.expired():
            self.refresh()
        return super().__call__(request)
