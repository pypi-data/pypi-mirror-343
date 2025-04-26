import asyncio

import pytest

from egse.async_control import AsyncControlClient
from egse.async_control import AsyncControlServer
from egse.async_control import CONTROL_SERVER_DEVICE_COMMANDING_PORT
from egse.async_control import CONTROL_SERVER_SERVICE_COMMANDING_PORT
from egse.async_control import is_control_server_active


@pytest.mark.asyncio
async def test_control_server(caplog):

    # First start the control server as a background task.
    server = AsyncControlServer()
    server_task = asyncio.create_task(server.serve())

    # Now create a control client that will connect to the above server.
    client = AsyncControlClient(f"tcp://localhost:{CONTROL_SERVER_DEVICE_COMMANDING_PORT}")
    client.connect()

    caplog.clear()

    # Sleep some time, so we can see the control server in action, e.g. status reports, housekeeping, etc
    await asyncio.sleep(5.0)

    assert "Sending status updates" in caplog.text  # this should there be 5 times actually

    response = await client.do({"command": "info"})
    print(f"{response = }")
    assert isinstance(response, dict)
    assert response['success'] is True
    assert "response" in response
    assert "name" in response["response"]
    assert "hostname" in response["response"]
    assert "commanding port" in response["response"]
    assert "timestamp" in response

    assert await is_control_server_active(endpoint=f"tcp://localhost:{CONTROL_SERVER_SERVICE_COMMANDING_PORT}")

    response = await client.do({"command": "terminate"})
    print(f"{response = }")
    assert isinstance(response, dict)
    assert response['success'] is True
    assert response['status'] == 'terminating'
    assert "timestamp" in response

    await server_task
