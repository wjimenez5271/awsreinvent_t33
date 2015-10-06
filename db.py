from boto.dynamodb2.table import Table


def put(data, table_name, overwrite=False):
    assert type(data) == dict
    assert type(table_name) == str
    table = Table(table_name)
    return table.put_item(data, overwrite=overwrite)


def get(table_name, **kwargs):
    assert type(table_name) == str
    table = Table(table_name)
    return table.put_item(**kwargs)

