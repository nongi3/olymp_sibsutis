class Users(db.Entity):
    name = Required(str)
    handle = Required(str)
    vkId = Required(str)
    all_points = Required(int)
    cf_points = Required(int)
    extra_points = Required(int)
    spent_points = Required(int)
