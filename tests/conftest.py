import pytest


@pytest.fixture(autouse=True)
def urllib3_never_request(monkeypatch):
    monkeypatch.delattr("urllib3.connectionpool.HTTPConnectionPool.urlopen")
