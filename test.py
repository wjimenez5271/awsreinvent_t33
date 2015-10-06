
users = Table('users')

data = { "uid" : "6502418470",
         "sex" : "M",
         "age" : 18,
         "point_count": 0,
         "last_qid": None}



print users.put_item(data=data)