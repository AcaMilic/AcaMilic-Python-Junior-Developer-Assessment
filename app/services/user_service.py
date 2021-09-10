import logging
from app.models.models import Contact


def array_as_dict(data_array):
    result = []
    for item in data_array:
        json_data = {c.name: getattr(item, c.name) for c in item.__table__.columns}
        result.append(json_data)
    return result



class UserService(object):

    @staticmethod
    def get_all_users():
        """Getting all games."""
        try:
            users = Contact.query.all()
            result = array_as_dict(users)
            return result
        except Exception as e:
            logging.error("Can't get users: " + str(e))
            return None


