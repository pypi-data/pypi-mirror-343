Changelog
=========

0.2.2 (2025-04-25)
------------------

-   Unit test changes only. No functional changes in this release.

-   Ignore any preexisting bearer tokens when running the unit tests.

0.2.1 (2025-04-16)
------------------

-   Documentation and code style changes only. No functional changes in this
    release.

-   Switch to a "src" package layout for easier Debian packaging. As a side
    effect, the unit test suite is no longer part of the installed package.

0.2.0 (2025-04-11)
------------------

-   Drop support for Python 3.7 and 3.8, which have reached end-of-life.

-   Add support for Python 3.12 and 3.13.

-   Rename the ``cert_reload`` and ``cert_reload_timeout`` keyword arguments
    to ``auth_reload`` and ``auth_reload_timeout`` respectively.

-   Add support for SciTokens.

0.1.4 (2022-11-28)
------------------

-   Drop support for Python 2.6-3.6, which have reached end-of-life.

-   Add support for Python 3.9-3.11.

-   Modernize Python packaging to `configure Setuptools using pyproject.toml
    <https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`_.

0.1.3 (2020-02-20)
------------------

-   When searching for certificates in the default path, check that the files
    both exist and are readable.

-   When reloading certificates, immediately close connections with old
    certificates rather than simply leaving them for garbage collection.

0.1.2 (2020-02-10)
------------------

-   Fix a urllib3 ValueError that occurs with older versions of urllib3.
    See, for example, https://bugzilla.redhat.com/show_bug.cgi?id=1785696.

0.1.1 (2020-02-04)
------------------

-   Remove unused ``ligo`` namespace package.

0.1.0 (2020-02-03)
------------------

-   Fix a unit test failure in test_cert_reload due to a test X.509 certificate
    having an expiration date that was in the past. The workaround was to set
    the certificate's "not valid before" date to the distant past (2008-01-01)
    and its "not valid after" date to the distant future (3020-01-01). Maybe
    our great-great-grandchildren will be wiser.

-   Address all feedback from Pierre Chanial's code review:
    https://git.ligo.org/emfollow/requests-gracedb/issues/3

-   Rename package from ligo-requests to requests-gracedb to remove
    institution-specific branding.

0.0.1 (2019-12-12)
------------------

-   Initial release.
