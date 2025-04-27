from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from fibonacci_api.main import app, Versions
from fibonacci_api import crud

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == app.title
    assert content["summary"] == app.summary
    assert content["description"] == app.description


def test_get_fibonacci_number():
    fibonacci_val = 1
    response = client.get(Versions.v1.value + f"/fibonacci/{fibonacci_val}")
    assert response.status_code == 200
    assert int(response.content.decode("utf-8")) == crud.calculate_fibonacci(
        fibonacci_val
    )


@given(st.integers(min_value=0))
def test_add_to_block_list(sequence_number: int):
    response = client.patch(
        Versions.v1.value + f"/fibonacci/block/{sequence_number}"
    )
    assert response.status_code == 201
    assert sequence_number in response.json()
