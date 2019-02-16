

from hemlock import query
from hemlock.models.branch import Branch

def restore_branch(prev_id):
    curr_id = query(prev_id,Branch).get_next_branch_id()
    return query(curr_id, Branch)