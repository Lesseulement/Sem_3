def field(items, *args):
    assert len(args) > 0

    if len(args) == 1:
        key = args[0]
        return [item[key] for item in items if key in item and item[key] is not None]

    else:
        result = []
        for item in items:
            filtered_dict = {key: item[key] for key in args if key in item and item[key] is not None}
            if filtered_dict:
                result.append(filtered_dict)
        return result

goods = [
    {'title': 'Ковер', 'price': 2000, 'color': 'green'},
    {'title': 'Диван для отдыха', 'color': 'black'}
]

print(field(goods, 'title'))

print(field(goods, 'title', 'price'))