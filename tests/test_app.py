import os

import pytest

from hemlock.app import Config


class TestConfig:
    @pytest.mark.parametrize("postgres", (True, False))
    def test_sqlalchemy_database_uri(self, postgres):
        if postgres:
            os.environ["DATABASE_URL"] = "postgres://db"

        uri = Config().SQLALCHEMY_DATABASE_URI

        if postgres:
            os.environ.pop("DATABASE_URL")
            # test that URL uses postgresql scheme for 
            # Heroku + sqlalchemy 1.4 compatibility
            assert uri == "postgresql://db"
        else:
            assert uri == "sqlite://"
            