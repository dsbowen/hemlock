from hemlock.models.question import Question

def query(ids, model_type=Question):
    if type(ids) == int:
        return model_type.query.get(ids)
    if type(ids) == list:
        return model_type.query.filter(model_type.id.in_(ids)).all()
    if type(ids) == dict:
        to_return = {}
        for key in ids.keys():
            to_return[key] = model_type.query.get(ids[key])
        return to_return