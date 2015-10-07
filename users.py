import uuid
import db


class EndUser(object):
    def __init__(self, uid, point_count=0, last_question=None, demographics=[]):
        self.uid = uid
        self.point_count = point_count
        self.last_question = last_question
        self.demographics = demographics

    def write(self):
        data ={'uid':self.uid,
                'point_count': self.point_count,
                'last_question': self.last_question,
                'demographics': self.demographics}
        db.put(data, table_name='users', overwrite=True)


def get_user(uid):
    r = db.get('users', uid=uid)
    return EndUser(uid,
                point_count=r['point_count'],
                last_question=r['last_question'],
                demographics=r['demographics'])

