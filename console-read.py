import ast
import json

file = open('console-feed.json').read()
feed = ast.literal_eval(file)


def parse_request(request_str):
    find_str = "request"

    location = request_str.find(find_str)
    return ast.literal_eval(request_str[location + len(find_str) + 1:])


items = [x['message'][x['message'].index("\"") + 1: -1] for x in feed if x['source'] == 'console-api']

items = items[7:]

url_end = "battle-gen7randombattle-655630618"

for item in items:
    # loc = item.find(u'003C')
    # loc = item.find(u'003C', loc+1)
    loc = item.find(url_end)

    if loc != -1:
        temp_str = item[loc + len(url_end):]
        find_request = "request"
        loc = temp_str.find(find_request)

        if loc != -1:
            print(parse_request(temp_str))

        print(temp_str)
    else:
        print(item)



