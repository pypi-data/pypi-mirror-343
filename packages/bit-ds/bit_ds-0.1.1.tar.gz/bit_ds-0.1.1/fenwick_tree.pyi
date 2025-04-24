class BIT:
    """
    A class representing a Binary Indexed Tree (Fenwick Tree).
    The tree is 1 indexed and the input array is 0 indexed.

    :param input: input array to build the tree
    """
    def __init__(self, input: list) -> None: ...
    @classmethod
    def update(cls, position: int, val: int) -> None:
        """
        Updates the Fenwick Tree with a given value at a specified position.
        position is 0 indexed.

        :param position: index of the element to be updated
        :param val: value to be added to the specified position
        """
    @classmethod
    def override_update(cls, position: int, val: int) -> None:
        """
        Overrides a value in the Fenwick Tree with a given value at a specified position.
        position is 0 indexed.

        :param position: index of the element to be updated
        :param val: value to be set at the specified position
        """
    @classmethod
    def tree(cls) -> list:
        """
        Returns the BIT as a list.
        """
    @classmethod
    def size(cls) -> int:
        """
        Returns the size of the BIT.
        """
    @classmethod
    def sum(cls, position: int) -> int:
        """
        Returns the sum of the elements from the origin to the specified position.
        position is 0 indexed.

        :param position: index of the element to query
        """
    @classmethod
    def range_sum(cls, start: int, end: int) -> int:
        """
        Returns the sum of the elements in the specified range.
        start and end are 0 indexed.

        :param start: index of the starting element
        :param end: index of the ending element
        """
    @staticmethod
    def new_file(path: str) -> BIT:
        """
        Creates a new BIT class instance from a file.

        :param path: path to the file containing the input array
        """
    @classmethod
    def sum_indices(cls, index: int) -> list[int]:
        """
        Returns the indices of the elements that contribute to the sum at a given index.

        :param index: index of the element to query to from origin
        """
    @classmethod
    def range_sum_indices(cls, start: int, end: int) -> list[int]:
        """
        Returns the indices of the elements that contribute to the sum in the specified range.

        :param start: index of the starting element
        :param end: index of the ending element
        """

class NdBIT:
    """
    A class representing a N-Dimensional BIT (Fenwick Tree).
    The tree is 1 indexed and the input array is 0 indexed.

    :param input: input array to build the tree
    :param dim: number of dimensions of the input array
    """
    def __init__(self, input: list, dim: int) -> None: ...
    @classmethod
    def update(cls, position: list[int], val: int) -> None:
        """
        Updates the Fenwick Tree with a given value at a specified position.
        position is 0 indexed.

        :param position: list of indices representing the position in the N-dimensional array
        :param val: value to be added to the specified position
        """
    def override_update(self, position: list[int], val: int) -> None:
        """
        Overrides a value in the BIT with a given value at a specified position.
        position is 0 indexed.

        :param position: list of indices representing the position in the N-dimensional array
        :param val: value to be set at the specified position
        """

    @classmethod
    def tree(cls) -> list:
        """
        Returns the BIT tree.
        """

    @classmethod
    def size(cls) -> int:
        """
        Returns the size of the BIT
        """

    @classmethod
    def dim(cls) -> int:
        """
        Returns the number of dimensions of the Fenwick Tree
        """

    @classmethod
    def sum(cls, position: list[int]) -> int:
        """
        Returns the sum of the elements from the origin to the specified position.
        position is 0 indexed.

        :param position: list of indices representing the position in the N-dimensional array
        """

    @classmethod
    def range_sum(cls, start: list[int], end: list[int]) -> int:
        """
        Returns the sum of the elements in the specified range.
        start and end are 0 indexed.

        :param start: list of indices representing the start position in the N-dimensional array
        :param end: list of indices representing the end position in the N-dimensional array
        """

