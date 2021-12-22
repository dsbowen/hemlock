import pytest
from sqlalchemy_mutable.utils import partial

from hemlock import User, Page
from hemlock.app import db
from hemlock.utils.random import Assigner

from ..utils import app


@pytest.fixture(
    scope="module",
    params=(
        {"factor0": (0, 1)},
        {"factor0": (0, 1), "factor1": ("low", "med", "high")},
    ),
)
def assigner(request):
    return Assigner(request.param)


class TestAssigner:
    def seed(self, assigner):
        assigner.assign_user()
        return [Page(), Page()]

    def test_assign_user(self, app, assigner):
        expected_assignments = set(assigner.possible_assignments)
        for _ in range(len(expected_assignments)):
            user = User.make_test_user(partial(self.seed, assigner))
            metadata = user.get_meta_data()
            expected_assignments.remove(
                tuple(metadata[name] for name in assigner.factor_names)
            )
        assert not expected_assignments

    def test_get_cum_assigned(self, app, assigner):
        df = assigner.get_cum_assigned()
        if len(assigner.factor_names) == 1:
            expected_values = set(value[0] for value in assigner.possible_assignments)
        else:
            assert set(df.index.names) == set(assigner.factor_names)
            expected_values = set(assigner.possible_assignments)
        assert expected_values == set(df.index.values)

        # test that the count is 0 when there are no users
        assert (df["count"] == 0).all()

        # test that the count is 0 when there are in progress users but no one has
        # finished (so the factor names aren't in the dataframe)
        User.make_test_user(partial(self.seed, assigner))
        assert (assigner.get_cum_assigned()["count"] == 0).all()

        # test that the count is 1 when exactly 1 user has finished in all conditions
        for _ in range(len(expected_values)):
            User.make_test_user(partial(self.seed, assigner)).test()
        assert (assigner.get_cum_assigned()["count"] == 1).all()
