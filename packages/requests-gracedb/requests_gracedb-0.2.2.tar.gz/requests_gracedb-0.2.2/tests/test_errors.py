#
# Copyright (C) 2019-2025  Leo P. Singer <leo.singer@ligo.org>
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
"""Tests for :mod:`requests_gracedb.errors`."""

import pytest
from requests.exceptions import HTTPError

from requests_gracedb import Session


def test_errors(socket_enabled, httpserver):
    """Test that HTTP 400 responses result in exceptions."""
    message = "Tea time!"
    status = 418
    httpserver.expect_request("/").respond_with_data(message, status)

    url = httpserver.url_for("/")
    client = Session(url)
    with pytest.raises(HTTPError) as excinfo:
        client.get(url)
    exception = excinfo.value
    assert exception.response.status_code == status
    assert exception.response.reason == "I'M A TEAPOT"
    assert exception.response.text == message
