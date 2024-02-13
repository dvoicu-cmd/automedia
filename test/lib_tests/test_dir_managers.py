from context import lib
from lib import *
import pdb


pdm = PublisherDirManager()
tmp = pdm.create_tmp_dir()
name = tmp.name
pdb.set_trace()
print("HEHE")
print(name)
pdm.cleanup(tmp)
pdb.set_trace()
print(tmp)
