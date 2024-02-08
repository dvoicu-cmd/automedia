from context import lib
from lib.manage_service.service_configurator import ServiceConfigurator
from lib.manage_service.manage_service import ManageService


def test_load():
    sc = ServiceConfigurator()
    print(sc.read())


def test_write():
    sc = ServiceConfigurator()
    sc.write("/etc/systemd/system", "/bin/python3", "/Users/dvoicu/python/src")

    ms = ManageService()
    ms.print_map()



test_write()
test_load()