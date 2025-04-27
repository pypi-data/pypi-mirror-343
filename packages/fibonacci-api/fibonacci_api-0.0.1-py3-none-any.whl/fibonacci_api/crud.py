"""CRUD operations."""

from functools import cache
from pydantic import PositiveInt
from fibonacci_api.types import SequenceNumber

from fibonacci_api import _block


class ValueOnBlockList(Exception):
    pass


@cache
def calculate_fibonacci(n: SequenceNumber) -> SequenceNumber:
    """Calculate the `n`th Fibonacci sequence number.

    This function is naively cached.

    Raises:
        ValueError
    """
    match n:
        case 0:
            return 0
        case 1:
            return 1
        case n if n >= 2:
            return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
        case _:
            raise ValueError


async def get_fibonacci(n: SequenceNumber) -> SequenceNumber:
    if n in _block.SEQUENCE_NUMBER_BLOCK_LIST:
        raise ValueOnBlockList("%s", f"{n} on block list")
    return calculate_fibonacci(n)


def get_page(item: int, page: int, limit: PositiveInt):
    """Return the paginated `range object`."""
    return range(page * limit, min(item, (page + 1) * limit))


async def get_fibonacci_range(
    sequence_number: SequenceNumber,
    page: SequenceNumber = 0,
    limit: PositiveInt = 100,
) -> dict[int, SequenceNumber]:
    return {
        i: await get_fibonacci(i)
        for i in get_page(sequence_number, page, limit)
        if i not in _block.SEQUENCE_NUMBER_BLOCK_LIST
    }


def update_block_list(sequence_number: SequenceNumber) -> set[SequenceNumber]:
    _block.SEQUENCE_NUMBER_BLOCK_LIST |= set([sequence_number])
    return _block.SEQUENCE_NUMBER_BLOCK_LIST


def get_block_list() -> set[SequenceNumber]:
    return _block.SEQUENCE_NUMBER_BLOCK_LIST


def delete_from_block_list(
    sequence_number: SequenceNumber,
) -> set[SequenceNumber]:
    try:
        _block.SEQUENCE_NUMBER_BLOCK_LIST.remove(sequence_number)
    except KeyError:
        # Number was not part of the list.
        pass
    return _block.SEQUENCE_NUMBER_BLOCK_LIST


def delete_all_from_block_list():
    a: set[SequenceNumber] = set()
    _block.SEQUENCE_NUMBER_BLOCK_LIST = a
