from daak.process import Run
import pytest


@pytest.mark.asyncio
async def test_simple():
    await Run("ls -al").runpurecloud
