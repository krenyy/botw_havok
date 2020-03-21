# botw_havok

A library for converting Breath of the Wild Havok packfiles to JSON and back.

The main purpose of this library is deserializing Havok packfiles into a universal JSON file that can be converted to both Wii U and Switch packfiles.

HKX -> JSON conversion:
```py
from botw_havok import Havok

hk = Havok.from_file('A-1-0.hksc')
hk.deserialize()
hk.to_json('A-1-0.json', pretty_print=True)
```

JSON -> HKX conversion:
```py
from botw_havok import Havok

hk = Havok.from_json('A-1-0.json')
hk.to_switch() # or hk.to_wiiu()
hk.serialize()
hk.to_file('A-1-0.hksc')
```

The library also comes with two commands: `hk_to_json` and `json_to_hk`

You can learn how to use them by appending `--help` flag

---

At the moment, only Havok Physics files (.hksc, .hkrb, .hktmrb) work. Most of them should deserialize and serialize flawlessly and should be nearly identical to the originals (except the pointer section ordering which should be irrelevant).

The library is currently highly experimental, so expect bugs!

It's also really messy. Forgive me.
