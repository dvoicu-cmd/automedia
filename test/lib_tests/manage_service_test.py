from context import lib
from lib.manage_service.manage_service import ManageService

def test_create_paths_config():
    ms = ManageService()
    ms.create_paths_config("/etc/systemd", "/usr/bin/python3", "/Users/dvoicu/Desktop/Local\ Editing\ Projects/bottomtextmedia/automedia_backend/test/lib_tests")

def test_create_service():
    ms = ManageService()
    ms.create("the", ["*-*-* 18:00:00", "*-*-* 18:10:00"])

def test_delete_service():
    ms = ManageService()
    ms.delete("the")

ms = ManageService()
# test_create_service()
ms.lock()

