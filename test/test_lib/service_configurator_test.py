from lib.manage_service.service_configurator import ServiceConfigurator


def test_load():
    sc = ServiceConfigurator()
    print(sc.read())


def test_write():
    sc = ServiceConfigurator()
    sc.write("/etc/systemd/system", "/bin/python3", "/Users/dvoicu/python/src")


test_write()
test_load()