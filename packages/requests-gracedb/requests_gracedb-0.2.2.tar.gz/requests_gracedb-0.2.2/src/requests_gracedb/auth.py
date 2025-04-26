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
from os import R_OK, access, environ, getuid
from os.path import expanduser, join
from urllib.parse import urlparse
from warnings import warn

from igwn_auth_utils.scitokens import default_bearer_token_file
from safe_netrc import netrc

from .cert_reload import CertReloadingHTTPAdapter
from .scitoken import SciTokenAuth, SciTokenReloadingAuth


def _find_cert():
    """Try to find a user's X509 certificate and key.

    Checks environment variables first, then expected location for default
    proxy.

    Notes
    -----
    This function is adapted from the original ``_find_x509_credentials()``
    method in https://git.ligo.org/lscsoft/gracedb-client/blob/gracedb-2.5.0/ligo/gracedb/
    rest.py, which is copyright (C) Brian Moe, Branson Stephens (2015).

    """  # noqa: E501
    result = tuple(environ.get(key) for key in ("X509_USER_CERT", "X509_USER_KEY"))
    if all(result):
        return result

    result = environ.get("X509_USER_PROXY")
    if result:
        return result

    result = join("/tmp", f"x509up_u{getuid()}")
    if access(result, R_OK):
        return result

    result = tuple(
        expanduser(join("~", ".globus", filename))
        for filename in ("usercert.pem", "userkey.pem")
    )
    if all(access(path, R_OK) for path in result):
        return result


def _find_username_password(url):
    host = urlparse(url).hostname

    try:
        result = netrc().authenticators(host)
    except IOError:
        result = None

    if result is not None:
        username, _, password = result
        result = (username, password)

    return result


def _find_token():
    path = default_bearer_token_file()
    if access(path, R_OK):
        return path


class SessionAuthMixin:
    """A mixin for :class:`requests.Session` to add support for all GraceDB
    authentication mechanisms.

    Parameters
    ----------
    url : str
        GraceDB Client URL.
    token : str
        Filename for SciTokens bearer token.
    cert : str, tuple
        Client-side X.509 certificate. May be either a single filename
        if the certificate and private key are concatenated together, or
        a tuple of the filenames for the certificate and private key.
    username : str
        Username for basic auth.
    password : str
        Password for basic auth.
    force_noauth : bool, default=False
        If true, then do not use any authentication at all.
    fail_if_noauth : bool, default=False
        If true, then raise an exception if authentication credentials are
        not provided.
    auth_reload : bool, default=False
        If true, then automatically reload the authentication before it
        expires.
    auth_reload_timeout : int, default=300
        Reload the authentication this many seconds before it expires.
    cert_reload :
        Deprecated synonym for auth_reload.
    cert_reload_timeout :
        Deprecated synonym for auth_reload_timeout.

    Notes
    -----
    When a new Session instance is created, the following sources of
    authentication are tried, in order:

    1.  If the :obj:`force_noauth` keyword argument is true, then perform no
        authentication at all.

    2.  If the :obj:`token` keyword argument is provided, then use SciTokens
        bearer token authentication.

    3.  If the :obj:`cert` keyword argument is provided, then use X.509 client
        certificate authentication.

    4.  If the :obj:`username` and :obj:`password` keyword arguments are
        provided, then use basic auth.

    5.  Look for a SciTokens bearer token in:

        a.  the environment variable :envvar:`BEARER_TOKEN_FILE`
        b.  the file :file:`$XDG_RUNTIME_DIR/bt_u{UID}`, where :samp:`{UID}`
            is your numeric user ID, if the file exists and is readable

    6.  Look for a default X.509 client certificate in:

        a.  the environment variables :envvar:`X509_USER_CERT` and
            :envvar:`X509_USER_KEY`
        b.  the environment variable :envvar:`X509_USER_PROXY`
        c.  the file :file:`/tmp/x509up_u{UID}`, where :samp:`{UID}` is your
            numeric user ID, if the file exists and is readable
        d.  the files :file:`~/.globus/usercert.pem` and
            :file:`~/.globus/userkey.pem`, if they exist and are readable

    7.  Read the netrc file [1]_ located at :file:`~/.netrc`, or at the path
        stored in the environment variable :envvar:`NETRC`, and look for a
        username and password matching the hostname in the URL.

    8.  If the :obj:`fail_if_noauth` keyword argument is true, and no
        authentication source was found, then raise a :class:`ValueError`.

    References
    ----------
    .. [1] The .netrc file.
           https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html

    """  # noqa: E501

    def __init__(
        self,
        url=None,
        token=None,
        cert=None,
        username=None,
        password=None,
        force_noauth=False,
        fail_if_noauth=False,
        auth_reload=False,
        auth_reload_timeout=300,
        cert_reload=None,
        cert_reload_timeout=None,
        **kwargs,
    ):
        super(SessionAuthMixin, self).__init__(**kwargs)

        if cert_reload is not None:
            warn(
                "The cert_reload argument is deprecated. Please use the auth_reload argument instead.",
                DeprecationWarning,
            )
            auth_reload = cert_reload
        if cert_reload_timeout is not None:
            warn(
                "The cert_reload_timeout argument is deprecated. Please use the auth_reload_timeout argument instead.",
                DeprecationWarning,
            )
            auth_reload_timeout = cert_reload_timeout

        # Argument validation
        if fail_if_noauth and force_noauth:
            raise ValueError("Must not set both force_noauth and fail_if_noauth.")
        if (username is None) ^ (password is None):
            raise ValueError("Must provide username and password, or neither.")

        if force_noauth:
            pass
        elif token is not None:
            pass
        elif cert is not None:
            self.cert = cert
        elif username is not None:
            self.auth = (username, password)
        elif (token := _find_token()) is not None:
            pass
        elif (default_cert := _find_cert()) is not None:
            self.cert = default_cert
        elif (default_basic_auth := _find_username_password(url)) is not None:
            self.auth = default_basic_auth
        elif fail_if_noauth:
            raise ValueError("No authentication credentials found.")

        # Support for reloading client certificates
        if self.cert is not None and auth_reload:
            self.mount(
                "https://",
                CertReloadingHTTPAdapter(cert_reload_timeout=auth_reload_timeout),
            )

        if token is not None:
            if auth_reload:
                self.auth = SciTokenReloadingAuth(
                    token, reload_timeout=auth_reload_timeout
                )
            else:
                self.auth = SciTokenAuth(token)
