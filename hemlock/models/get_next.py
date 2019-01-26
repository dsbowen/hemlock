###############################################################################
# get_next function
# by Dillon Bowen
# last modified 01/26/2019
###############################################################################

# Get the next branch of the survey
# inputs: next navigation function, arguments, participant
# returns branch from the next navigation function
# assigns participant for embedded data questions
def get_next(next, args, part):
    if next:
        if args:
            branch = next(args)
        else:
            branch = next()
        for e in branch.embedded:
            e.part = part
        return branch
    return None