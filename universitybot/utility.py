"""
Utility functions
"""


# split list l in smaller list of length n
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]


# returns a tuple from a tuple list which has as value at a given position
def find_tuple_in_tuplelist(tuplelist, value, position):
    return [item for item in tuplelist if item[position] == value]


# given a list of strings of user data names, it deletes them from given user data
def delete_userdata(user_data, data_list):
    for data in data_list:
        if data in user_data:
            del user_data[data]
