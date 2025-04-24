"""This file is used to test the functions of FC."""

#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import logging

import pytest

from sts.fc import FcDevice
from sts.utils.cmdline import run
from sts.utils.errors import DeviceNotFoundError
from sts.utils.modules import ModuleInfo
from sts.utils.packages import ensure_installed


class TestFcDevice:
    """Test class for FC functionality."""

    @pytest.fixture(autouse=True)
    def _device(self, get_fc_device: FcDevice) -> None:
        """Automatically instantiate an instance of FcDevice shared in each test method.

        Args:
            get_fc_device: A fixture that provides an instance of FcDevice.

        Returns:
            None: This method does not return a value but instead assigns the provided FcDevice instance to
            the `device` attribute of the test class instance, making it accessible for other test methods
            within the class.
        """
        self.device = get_fc_device

    def test_show_driver_info(self) -> None:
        """Test showing driver information for the device."""
        if self.device.driver:
            mod_info = ModuleInfo.from_name(self.device.driver)
            logging.info(mod_info)
        else:
            pytest.skip(f'Could not find the driver used by {self.device}')

    def test_lspci_fc_host(self) -> None:
        """Test displaying PCI bus information for FC host."""
        if self.device.pci_id:
            assert ensure_installed('pciutils')
            result = run(f'lspci -s {self.device.pci_id} -vvv')
            logging.info(result.stdout)
        else:
            pytest.skip(f'Could not find the pci slot where {self.device} resides.')

    def test_delete_disk_then_rescan_host(self) -> None:
        """Test deleting a disk and then rescanning the host."""
        logging.info(f'Running check_sector_zero for {self.device.path}')
        assert self.device.check_sector_zero(), f'I/O error in sector 0 of disk {self.device.path}'
        logging.info(f'Running delete_disk for {self.device.path}')
        assert self.device.delete_disk(), f'Failed to delete disk {self.device.path}'
        logging.info('Running rescan_host')
        assert self.device.rescan_host(), f'Rescan host{self.device.host_id} failed.'

        logging.info('Running wait_udev')
        self.device.wait_udev()

        try:
            logging.info(f'Running validate_device_exists for {self.device.path}')
            self.device.validate_device_exists()
        except DeviceNotFoundError:
            pytest.fail(f'The deleted disk {self.device.path} was not added back')
        logging.info(f'Running check_sector_zero again for {self.device.path}')
        assert self.device.check_sector_zero(), f'I/O error in sector 0 of disk {self.device.path} after rescan'
