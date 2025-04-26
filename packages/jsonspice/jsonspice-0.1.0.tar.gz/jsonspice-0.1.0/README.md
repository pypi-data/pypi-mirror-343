# json-spice
Python utility to allow JSON kernels in SpiceyPy

A work in progress!!

### Example

```python
import jsonspice  # import first to monkeypatch spiceypy
import spiceypy

spiceypy.furnsh('de-403-masses.tpc')  # normal kernel

spiceypy.furnsh('test.json')  # also works with JSON kernels

spiceypy.furnsh({"BODY8_GM": 6836534.064})  # also works with dicts
spiceypy.furnsh({"time": '@1972-JAN-1'})  # SPICE @ syntax for time (see .fk files)
spiceypy.furnsh({"+abc": [4,5,6]})  # SPICE += syntax to append
```

### See also

* [NAIF](https://naif.jpl.nasa.gov/naif/) -- NASA's Navigation and Ancillary Information Facility
* [SpiceyPy](https://github.com/AndrewAnnex/SpiceyPy) -- SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit
* J. Williams, [JSON + SPICE](https://degenerateconic.com/json-spice.html), Feb 5, 2018 (degenerateconic.com)