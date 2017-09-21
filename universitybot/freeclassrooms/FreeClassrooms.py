import abc


class FreeClassrooms(metaclass=abc.ABCMeta):
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    https://sourcemaking.com/design_patterns/strategy/python/1
    """

    @staticmethod
    @abc.abstractmethod
    def get_free_classrooms(date, start_time, end_time):
        pass
