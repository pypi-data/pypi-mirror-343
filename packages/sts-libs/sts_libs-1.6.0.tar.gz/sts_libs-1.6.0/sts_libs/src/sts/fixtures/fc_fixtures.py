"""FC test fixtures."""

import pytest

from sts.fc import FcDevice


@pytest.fixture(scope='class')
def get_fc_device() -> FcDevice:
    """Pytest fixture to get the first Fibre Channel (FC) device.

    Returns:
        The first FC device

    Example:
        ```Python
        def test_fc_device(get_fc_device: FcDevice):
            assert get_fc_device.path.exists()
        ```
    """
    devices = FcDevice.get_by_attribute('transport', 'fc:')
    # Break down complex assertion
    online_devices = [dev for dev in devices if dev.state == 'running']
    if not online_devices:
        pytest.skip("No online FC devices found with transport 'fc:'")
    return online_devices[0]
