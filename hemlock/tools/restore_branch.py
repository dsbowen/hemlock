

from hemlock.tools.query import query
from hemlock.models.branch import Branch

def restore_branch(prev_id, table=Branch):
    curr_id = query(prev_id,table).get_next_branch_id()
    return query(curr_id, Branch)