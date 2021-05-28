import os

import pytest

ctb_bolt_url_varname = "COMBATTB_BOLT_URL"
skip_if_no_bolt = pytest.mark.skipif(
    os.environ.get(ctb_bolt_url_varname, None) is None,
    reason=f"No {ctb_bolt_url_varname} environment variable present",
)


def get_bolt_url():
    return os.environ[ctb_bolt_url_varname]
