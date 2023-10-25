# The Recursive Nest

# Build a JSON nest
# ----------
# Given a JSON list of items, group the items following a list of given keys as input.
# Return the nest sorted alphabetically.
# Write unit tests to confirm the correctness of your solution.


initial_list = [
    {"country": "US", "city": "Boston", "currency": "USD", "amount": 100},
    {"country": "FR", "city": "Lyon", "currency": "EUR", "amount": 11.4},
    {"country": "FR", "city": "Paris", "currency": "EUR", "amount": 20},
    {"country": "ES", "city": "Madrid", "currency": "EUR", "amount": 8.9},
    {"country": "UK", "city": "London", "currency": "GBP", "amount": 12.2},
    {"country": "UK", "city": "London", "currency": "FBP", "amount": 10.9},
]


# Single key ["currency"] should return:

single_key_dict = {
    "USD": [{"country": "US", "city": "Boston", "amount": 100}],
    "EUR": [
        {"country": "FR", "city": "Paris", "amount": 20},
        {"country": "FR", "city": "Lyon", "amount": 11.4},
        {"country": "ES", "city": "Madrid", "amount": 8.9},
    ],
    "GBP": [{"country": "UK", "city": "London", "amount": 12.2}],
    "FBP": [{"country": "UK", "city": "London", "amount": 10.9}],
}


# Multiple keys ["currency", "country", "city"] should return:

multiple_keys_dict = {
    "EUR": {
        "ES": {"Madrid": [{"amount": 8.9}]},
        "FR": {"Lyon": [{"amount": 11.4}], "Paris": [{"amount": 20}]},
    },
    "FBP": {"UK": {"London": [{"amount": 10.9}]}},
    "GBP": {"UK": {"London": [{"amount": 12.2}]}},
    "USD": {"US": {"Boston": [{"amount": 100}]}},
}


def single_key_sorting(initial_list: list, key: str):
    sorted_dict = {}
    for obj in initial_list:
        if key in obj:
            if obj[key] not in sorted_dict:
                sorted_dict[obj[key]] = []
            current_value = obj[key]
            del obj[key]
            sorted_dict[current_value].append(obj)
        else:
            return None
    return sorted_dict


def key_sorting_dict(sorted_dict: dict, key: str):
    sorted_result = {}
    for dict_key in sorted_dict:
        intermediate_result = {}
        for obj in sorted_dict[dict_key]:
            if key in obj:
                if obj[key] not in intermediate_result:
                    intermediate_result[obj[key]] = []
                current_value = obj[key]
                del obj[key]
                intermediate_result[current_value].append(obj)
            elif isinstance(sorted_dict[dict_key][obj], list):
                intermediate_result = {}
                sorted_result[dict_key] = sorted_dict[dict_key]
                for inner_dict in sorted_result[dict_key][obj]:
                    if inner_dict[key] not in intermediate_result:
                        intermediate_result[inner_dict[key]] = []
                    current_value = inner_dict[key]
                    del inner_dict[key]
                    intermediate_result[current_value].append(inner_dict)
                sorted_result[dict_key][obj] = intermediate_result
                intermediate_result = {}
            else:
                return None
        if intermediate_result:
            sorted_result[dict_key] = intermediate_result
    return sorted_result


def json_sorting(initial_list: list, key_grouping: list):
    sorted_dict = {}
    for key in key_grouping:
        if sorted_dict:
            sorted_dict = key_sorting_dict(sorted_dict, key)
        else:
            sorted_dict = single_key_sorting(initial_list, key)
    return sorted_dict


final_dict = json_sorting(initial_list, ["currency", "country", "city"])
print(final_dict)
