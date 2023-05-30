

# for filtering
def query_chaining_filter(query, model, request, attributs):
    for attr in attributs:
        filter = request.args.get(attr)
        if filter:
            query = query.filter(getattr(model, attr) == (filter))
    return query
        # >, <, >=, <= can't be handled yet
        # for attr in ATTRIBUTES_RANGE:
        #     filter = request.args.get(attr)
        #     print('here -> ', request.args)
        #     if filter:
        #         for operator in OPERATORS:
        #             if operator in filter:
        #                 parts = filter.split(operator, 1)
        #                 field = parts[0].strip()
        #                 print(parts)
        #                 value = strToDatetime(value) if field == 'item_time' else int(parts[1].strip())
        #                 print(value)

        #                 if operator == '>=':
        #                     query = query.filter(getattr(ItemsModel, field) >= value)
        #                 elif operator == '<=':
        #                     query = query.filter(getattr(ItemsModel, field) <= value)
        #                 elif operator == '>':
        #                     query = query.filter(getattr(ItemsModel, field) > value)
        #                 elif operator == '<':
        #                     query = query.filter(getattr(ItemsModel, field) < value)
        #                 break                    

# for sorting
def query_chaining_sort(query, model, request, attributs):
    sort_param = request.args.get('sort')
    if sort_param:
        for attr in attributs:
            if sort_param == attr:
                query = query.order_by(getattr(model, attr))
    return query.order_by(model.item_time)


# for limiting
def query_chaining_limit(query, request):
    limit = request.args.get('limit')
    if limit:
        query = query.limit(int(limit))
    return query
# for pagination
def query_chaining_page(query, request):
    page = request.args.get('page', type=int)  # Get the page parameter from the query string
    page_size = request.args.get('page_size', type=int)  # Get the page_size parameter from the query string
    if page and page_size:
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)   
    return query