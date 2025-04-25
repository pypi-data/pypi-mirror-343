# mypy: disable-error-code="return"

from os import environ

from pytest import fixture, skip

from ebikeconnect import EBikeConnectClient


@fixture(scope="function")
def client() -> EBikeConnectClient:
    return EBikeConnectClient("cookie")


@fixture(scope="session")
def authenticated_client() -> EBikeConnectClient:
    try:
        client = EBikeConnectClient.login(environ["EBIKE_CONNECT_USERNAME"], environ["EBIKE_CONNECT_PASSWORD"])
        client.PAGE_SIZE = 4  # Set a lower PAGE_SIZE in order to more easily test paging.
        return client
    except KeyError:
        skip("Requires authentication.")
