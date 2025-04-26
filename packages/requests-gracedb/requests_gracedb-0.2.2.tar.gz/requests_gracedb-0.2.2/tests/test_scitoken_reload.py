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

from datetime import datetime, timedelta, timezone

import jwt
import pytest

from requests_gracedb import Session


@pytest.mark.parametrize("auth_reload", [False, True])
def test_token_reload(tmp_path, freezer, socket_enabled, httpserver, auth_reload):
    httpserver.expect_request("/").respond_with_json({})
    url = httpserver.url_for("/")

    token = tmp_path / "token.json"
    start_time = datetime(3020, 1, 1, tzinfo=timezone.utc)

    def write_jwt(exp):
        data = jwt.encode({"exp": exp.timestamp()}, key="", algorithm="none")
        token.write_text(data)
        return data

    jwt1 = write_jwt(start_time + timedelta(seconds=100))
    freezer.move_to(start_time)
    client = Session(token=token, auth_reload=auth_reload, auth_reload_timeout=10)
    response = client.get(url, stream=True)
    conn1 = response.connection
    assert response.request.headers["Authorization"] == f"Bearer {jwt1}"
    assert conn1 is not None

    jwt2 = write_jwt(start_time + timedelta(seconds=200))
    assert jwt1 != jwt2
    freezer.move_to(start_time + timedelta(seconds=50))
    response = client.get(url)
    assert response.request.headers["Authorization"] == f"Bearer {jwt1}"
    assert response.connection is conn1

    freezer.move_to(start_time + timedelta(seconds=91))
    response = client.get(url)
    assert (
        response.request.headers["Authorization"]
        == f"Bearer {jwt2 if auth_reload else jwt1}"
    )
    # JWT replacement does not require replacing connections.
    assert response.connection is conn1
