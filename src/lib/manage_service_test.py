from manage_service.manage_service import ManageService

def test_create_paths_config():
    ms = ManageService()
    ms.create_paths_config("/etc/systemd/system", "/usr/bin/python3", "/root/automedia_backend/src/lib")

def test_create_service():
    ms = ManageService()
    ms.create("the", ["*-*-* 18:00:00", "*-*-* 18:10:00"])

def test_delete_service():
    ms = ManageService()
    ms.delete("the")

# test_create_service()
test_delete_service()
