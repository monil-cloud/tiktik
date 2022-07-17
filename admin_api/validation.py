from tiktik.settings import db
def request_data(data, params):
    params = params
    for check in params:
        pass


def user_data_check(field, value):
    find_field = db.UserDetail.find_one({field: value})
    if find_field is not None:
        return 1
    else:
        return 0

