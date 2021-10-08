from itertools import product

from hemlock import User, Page, create_test_app
from hemlock.utils.random import assign_user, make_assigner


def test_assign_user():
    def seed():
        assign_user(assigner)
        return Page()

    conditions = {"factor0": (0, 1), "factor1": ("low", "medium", "high")}
    assigner = make_assigner(conditions)
    # we expect the users to be evenly assigned to all possible cells
    expected_assignments = list(product(*conditions.values()))
    create_test_app()
    for _ in range(len(expected_assignments)):
        user = User.make_test_user(seed)
        metadata = user.get_meta_data()
        expected_assignments.remove((metadata["factor0"], metadata["factor1"]))
    assert not expected_assignments
