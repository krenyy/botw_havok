from . import Havok

# testhk = "/home/kreny/Desktop/hktestfiles/rigidbody/elevator_u.hkrb"
# testhk = "/home/kreny/Desktop/hktestfiles/teramesh/6-27_empty_u.hktmrb"
# testhk = "/home/kreny/Desktop/hktestfiles/staticcompound/Dungeon000.hksc"
testhk = "/home/kreny/Desktop/hktestfiles/staticcompound/A-1-0_nx.hksc"
# testhk = "/home/kreny/Desktop/hktestfiles/navmesh/0-0_u.hknm2"
# testhk = "/home/kreny/Desktop/model-box-long-name.bin"

hk = Havok()
hk.read(testhk)

# hk.write("/home/kreny/Desktop/test.hkfile")

import pdb

pdb.set_trace()
