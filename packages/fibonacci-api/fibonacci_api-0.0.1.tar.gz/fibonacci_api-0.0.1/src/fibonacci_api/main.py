"""A simple Fibonacci-API.

The Fibonacci sequence is a sequence in which each element is the sum of the two
elements that precede it. The Fibonacci sequence is numbered from 0. such as:
[0:0, 1:1, 2:1, 3:2, ...]

[Ref](https://en.wikipedia.org/wiki/Fibonacci_sequence)
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, PositiveInt
from fastapi import APIRouter
from enum import Enum

from fibonacci_api import crud
from fibonacci_api.types import SequenceNumber


class Versions(Enum):
    v1 = "/api/v1"


assert __doc__ is not None
_summary, _description = __doc__.split("\n", 1)[:]
app = FastAPI(title="Fibonacci-api", summary=_summary, description=_description)

API_VERSION_1 = "/api/v1"
router_v1 = APIRouter(prefix=Versions.v1.value, tags=[Versions.v1])


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@app.get("/")
def read_root():
    return {
        "version": app.version,
        "title": app.title,
        "summary": app.summary,
        "api-versions": {"v1": Versions.v1.value},
        "description": app.description,
    }


@router_v1.get("/fibonacci/{sequence_number}")
async def get_item(sequence_number: SequenceNumber):
    """Return the `n`th Fibonacci number."""
    try:
        return await crud.get_fibonacci(sequence_number)
    except crud.ValueOnBlockList:
        raise HTTPException(status_code=409, detail="Item on block list.")


@router_v1.get("/fibonacci_range/{sequence_number}")
async def get_range(
    sequence_number: SequenceNumber,
    limit: PositiveInt = 100,
    page: SequenceNumber = 0,
) -> dict[int, SequenceNumber]:
    """Return the Fibonacci sequence until the `n`th number.

    Returns empty response if pagination/limit is configured out of range.
    """
    return await crud.get_fibonacci_range(sequence_number, page, limit)


@router_v1.patch(
    "/fibonacci/block/{sequence_number}", status_code=201, tags=["blocklist"]
)
def add_to_block_list(sequence_number: SequenceNumber) -> set[SequenceNumber]:
    """Add a number to the block list."""
    return crud.update_block_list(sequence_number)


@router_v1.get("/fibonacci/block/", tags=["blocklist"])
def get_block_list() -> set[SequenceNumber]:
    """Show the block list."""
    return crud.get_block_list()


@router_v1.delete("/fibonacci/block/{sequence_number}", tags=["blocklist"])
def remove_from_block_list(
    sequence_number: SequenceNumber,
) -> set[SequenceNumber]:
    """Drop single item from drop list."""
    return crud.delete_from_block_list(sequence_number)


@router_v1.delete("/fibonacci/block/", status_code=204, tags=["blocklist"])
def remove_all_from_block_list() -> None:
    """Drop all from block list."""
    return crud.delete_all_from_block_list()


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """Endpoint to perform a healthcheck on.

    This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status

    Reference: https://gist.github.com/Jarmos-san/0b655a3f75b698833188922b714562e5
    """
    return HealthCheck(status="OK")


app.include_router(router_v1)
