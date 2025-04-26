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
"""Tests for :mod:`requests_gracedb.cert_reload`."""

from datetime import datetime, timezone
from ssl import PROTOCOL_TLS_SERVER, SSLContext

import pytest
import pytest_httpserver
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.x509 import (
    CertificateBuilder,
    DNSName,
    Name,
    NameAttribute,
    SubjectAlternativeName,
    random_serial_number,
)
from cryptography.x509.oid import NameOID

from requests_gracedb import Session


@pytest.fixture
def backend():
    """Return an instance of the default cryptography backend."""
    return default_backend()


@pytest.fixture
def client_key(backend):
    """Generate client RSA key."""
    return generate_private_key(65537, 2048, backend)


@pytest.fixture
def server_key(backend):
    """Generate server RSA key."""
    return generate_private_key(65537, 2048, backend)


@pytest.fixture
def client_cert(client_key, backend):
    """Generate client certificate."""
    subject = issuer = Name(
        [
            NameAttribute(NameOID.COMMON_NAME, "example.org"),
            NameAttribute(NameOID.ORGANIZATION_NAME, "Alice A. Client"),
        ]
    )
    return (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .serial_number(random_serial_number())
        .public_key(client_key.public_key())
        .not_valid_before(datetime(3019, 1, 1, tzinfo=timezone.utc))
        .not_valid_after(datetime(3019, 1, 10, tzinfo=timezone.utc))
        .add_extension(SubjectAlternativeName([DNSName("localhost")]), critical=False)
        .sign(client_key, SHA256(), backend)
    )


@pytest.fixture
def server_cert(server_key, backend):
    """Generate server certificate."""
    subject = issuer = Name(
        [
            NameAttribute(NameOID.COMMON_NAME, "localhost"),
            NameAttribute(NameOID.ORGANIZATION_NAME, "Bob B. Server"),
        ]
    )
    return (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .serial_number(random_serial_number())
        .public_key(server_key.public_key())
        .not_valid_before(datetime(2008, 1, 1, tzinfo=timezone.utc))
        .not_valid_after(datetime(3020, 1, 1, tzinfo=timezone.utc))
        .add_extension(SubjectAlternativeName([DNSName("localhost")]), critical=False)
        .sign(server_key, SHA256(), backend)
    )


@pytest.fixture
def client_key_file(client_key, tmpdir):
    """Generate client key file."""
    filename = str(tmpdir / "client_key.pem")
    with open(filename, "wb") as f:
        f.write(
            client_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
        )
    return filename


@pytest.fixture
def server_key_file(server_key, tmpdir):
    """Generate server key file."""
    filename = str(tmpdir / "server_key.pem")
    with open(filename, "wb") as f:
        f.write(
            server_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
        )
    return filename


@pytest.fixture
def client_cert_file(client_cert, tmpdir):
    """Generate client certificate file."""
    filename = str(tmpdir / "client_cert.pem")
    with open(filename, "wb") as f:
        f.write(client_cert.public_bytes(Encoding.PEM))
    return filename


@pytest.fixture
def server_cert_file(server_cert, tmpdir):
    """Generate server certificate file."""
    filename = str(tmpdir / "server_cert.pem")
    with open(filename, "wb") as f:
        f.write(server_cert.public_bytes(Encoding.PEM))
    return filename


@pytest.fixture
def server(socket_enabled, server_cert_file, server_key_file):
    """Run test https server."""
    context = SSLContext(PROTOCOL_TLS_SERVER)
    context.load_cert_chain(server_cert_file, server_key_file)
    with pytest_httpserver.HTTPServer(ssl_context=context) as server:
        server.expect_request("/").respond_with_json({"foo": "bar"})
        yield server


@pytest.fixture
def client(server, client_cert_file, client_key_file, server_cert_file):
    """Create test client."""
    url = server.url_for("/")
    cert = (client_cert_file, client_key_file)
    with Session(url, cert=cert, auth_reload=True) as client:
        client.verify = server_cert_file
        yield client


def test_cert_reload(client, server, freezer):
    """Test reloading client X.509 certificates."""
    url = server.url_for("/")

    # Test 1: significantly before expiration time, still valid
    freezer.move_to(datetime(3019, 1, 2, tzinfo=timezone.utc))
    response = client.get(url, stream=True)
    conn1 = response.raw.connection
    assert response.json() == {"foo": "bar"}
    assert conn1 is not None

    # Test 2: > cert_reload_timeout seconds before expiration time, still valid
    freezer.move_to(datetime(3019, 1, 9, 23, 54, 59, tzinfo=timezone.utc))
    response = client.get(url, stream=True)
    conn2 = response.raw.connection
    assert response.json() == {"foo": "bar"}
    assert conn1 is conn2

    # Test 3: < cert_reload_timeout seconds before expiration time, invalid
    freezer.move_to(datetime(3019, 1, 10, tzinfo=timezone.utc))
    response = client.get(url)
    conn3 = response.raw.connection
    assert response.json() == {"foo": "bar"}
    assert conn1 is not conn3
