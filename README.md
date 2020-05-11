# botw_havok

### A library for manipulating Breath of the Wild Havok packfiles.

```py
"""
Removing a RigidBody
"""

from botw_havok import Havok

hk = Havok.from_file('/mnt/hdd/A-1-0.shksc')  # can also be Yaz0 compressed
hk.deserialize()
del hk.files[1].data.contents[0].namedVariants[0].variant.systems[0].rigidBodies[-1]
hk.serialize()
hk.to_file('/mnt/hdd/A-1-0_edited.hksc')
```

```py
"""
Converting between formats
"""

from botw_havok import Havok

hk0 = Havok.from_file('/mnt/hdd/0-0.shktmrb')
hk0.deserialize()
hk0.to_json('/mnt/hdd/0-0.json')

hk1 = Havok.from_json('/mnt/hdd/0-0.json')
hk1.to_wiiu()  # or hk1.to_switch()
hk1.serialize()
hk1.to_file('/mnt/hdd/0-0_nx.hktmrb')
```

```py
"""
Comparing contents
"""

from botw_havok import Havok

hk0 = Havok.from_file('/mnt/hdd/E-4-1_u.shksc')
hk1 = Havok.from_file('/mnt/hdd/E-4-1_nx.shksc')

hk0.deserialize()
hk1.deserialize()

hk0.files[1].data.contents == hk1.files[1].data.contents
```

---

<br/>

This library comes with these commands:
* `hk_to_json`: Havok packfile -> JSON
* `json_to_hk`: JSON -> Havok packfile
* `hk_compare`: Compare two or more packfiles
* `hkrb_extract`: Extract shapes from Static Compound files by HashId
* `hksc_to_hkrb`: Convert all Static Compound shapes into a single HKRB

<br/>

---

<br/>

* At the moment, only Havok Physics files (*.hksc, *.hkrb, *.hktmrb) can be read.

* Most of the smaller ones deserialize and serialize flawlessly and the resulting packfiles are nearly identical to the originals.

* The larger files (particularly StaticCompound ones) are usually smaller than the originals after serialization. That's caused by the originals having duplicate Havok objects that are removed and referenced instead.
