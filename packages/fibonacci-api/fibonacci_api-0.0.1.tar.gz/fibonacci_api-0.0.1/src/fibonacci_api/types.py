"""Types."""

from typing import Annotated
from pydantic import Field

# Fibonacci sequence numbers are Int and x <= 0
SequenceNumber = Annotated[int, Field(ge=0)]
