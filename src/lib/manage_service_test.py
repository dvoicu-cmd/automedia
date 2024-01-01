from manage_service.manage_service import ManageService

def test_create_paths_config():
    ms = ManageService()
    ms.create_paths_config("/etc/systemd/system", "/usr/bin/python3", "/root/automedia_backend/src/lib")

def test_create_service():
    ms = ManageService()
    ms.create("the", ["*-*-* *:*0/3:00"])

test_create_service()
