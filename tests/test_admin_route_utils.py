# Note: see test__admin_routes for addtional tests of these utilities
import os
from itertools import product

import pytest

from hemlock.admin_route_utils import in_gitpod_ide


@pytest.mark.parametrize(
    "host_in_env, vs_code_remote", product((True, False), (True, False))
)
def test_in_gitpod_ide(host_in_env, vs_code_remote):
    if host_in_env:
        os.environ["GITPOD_HOST"] = "host"

    os.environ["VS_CODE_REMOTE"] = str(vs_code_remote)

    in_ide = in_gitpod_ide()

    if "GITPOD_HOST" in os.environ:
        os.environ.pop("GITPOD_HOST")

    if host_in_env and not vs_code_remote:
        assert in_ide
    else:
        assert not in_ide
