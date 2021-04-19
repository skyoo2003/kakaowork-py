import pytest
from click.testing import CliRunner


@pytest.fixture(autouse=True)
def urllib3_never_request(monkeypatch):
    monkeypatch.delattr("urllib3.connectionpool.HTTPConnectionPool.urlopen")


@pytest.fixture(scope="function")
def cli_runner():
    return CliRunner()


@pytest.fixture(scope="function")
def cli_runner_isolated():
    cli_runner = CliRunner()
    with cli_runner.isolated_filesystem():
        yield cli_runner
