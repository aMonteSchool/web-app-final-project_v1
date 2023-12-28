def to_list_of_dicts(context):
    result = []
    for row in context.table.rows:
        result.append(dict(row.items()))
    return result
