
class Utility:
    """
    Utility functions
    """
    # split list l in smaller list of length n
    @staticmethod
    def chunks(l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i+n]

    # returns a tuple from a tuple list which has as value at a given position
    @staticmethod
    def find_tuple_in_tuplelist(tuplelist, value, position):
        return [item for item in tuplelist if item[position] == value]
