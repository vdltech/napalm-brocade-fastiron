"""Test fixtures."""

from builtins import super

import pytest
from napalm.base.test import conftest as parent_conftest

from napalm.base.test.double import BaseTestDouble
from napalm_fastiron import FastIron


@pytest.fixture(scope="class")
def set_device_parameters(request):
    """Set up the class."""

    def fin():
        request.cls.device.close()

    request.addfinalizer(fin)

    request.cls.driver = FastIron.FastIronDriver
    request.cls.patched_driver = PatchedFastIronDriver
    request.cls.vendor = "FastIron"
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedFastIronDriver(FastIron.FastIronDriver):
    """Patched FastIron Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        super().__init__(hostname, username, password, timeout, **optional_args)
        self.patched_attrs = ["device"]
        self.device = FakeFastIronDevice()

    def close(self):
        pass

    def is_alive(self):
        return {"is_alive": True}  # In testing everything works..

    def open(self):
        pass


class FakeFastIronDevice(BaseTestDouble):
    """FastIron device test double."""

    def send_command(self, command, **kwargs):
        filename = "{}.text".format(self.sanitize_text(command))
        full_path = self.find_file(filename)
        result = self.read_txt_file(full_path)
        return str(result)

    def send_command_timing(self, command, **kwargs):
        return self.send_command(command, **kwargs)
