"""Basic smoke tests to verify the Python environment is wired up."""

from retail_dummyjson_pipeline.api_client import DUMMYJSON_BASE_URL, DummyJsonClient


def test_base_url() -> None:
    assert DUMMYJSON_BASE_URL == "https://dummyjson.com"


def test_client_instantiation() -> None:
    client = DummyJsonClient()
    assert client.base_url == "https://dummyjson.com"
