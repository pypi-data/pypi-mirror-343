import spiceypy
from spiceypy import tparse, pdpool, pcpool, dtpool, gcpool, gdpool, dvpool
from typing import Iterable, Union
try:
    # this will allow loading JSON files with comments
    import json5 as json
except ImportError:
    # if not present, fallback to regular json (won't allow comments)
    import json

class spiceypy_cache:
    # just to cache the original furnsh function
    furnsh = spiceypy.spiceypy.furnsh

def monkey_patch_spiceypy():
    """
    Monkey patch the `furnsh` function in spiceypy to support JSON kernels.
    """
    spiceypy.spiceypy.furnsh = furnsh_json_kernel
    spiceypy.furnsh = furnsh_json_kernel

def furnsh_json_kernel(kernel_path: Union[str, dict, Iterable[str]]) -> None:
    """
    Load a JSON kernel into SPICE.

    See: `furnsh_dict` for details.

    Parameters
    ----------
    kernel_path : str | list of strings | dict
        The path(s) to the JSON kernel file(s) or a dictionary containing the kernel data.
    """

    if isinstance(kernel_path, dict):
        # if a dictionary is passed, use it directly
        furnsh_dict(kernel_path)
    elif spiceypy.stypes.is_iterable(kernel_path):
        # if an iterable is passed, assume it is a list of paths
        for p in kernel_path:
            furnsh_json_kernel(p)
    elif isinstance(kernel_path, str):
        if not kernel_path.lower().endswith('.json'):
            # in this case, just use a normal furnsh
            spiceypy_cache.furnsh(kernel_path)
        else:
            # use the custom routine:
            with open(kernel_path, 'r') as f:
                data = json.load(f)
            furnsh_dict(data)
    else:
        raise TypeError("kernel_path must be a string or a dictionary.")

def furnsh_dict(data: dict) -> None:
    """
    Load a JSON kernel data into SPICE.

    Note: there are two modifications to support JSON SPICE kernels:

    1. if the variable name starts with '+', then the SPICE '+=' syntax
       is used to add to an existing variable if it exists.
    2. if a string value starts with '@', it is treated as a UTC string
       and converted to a double precision number representing "UTC seconds past J2000".

    Reference: https://degenerateconic.com/json-spice.html

    Parameters
    ----------
    d : dict
        The JSON kernel data as a dictionary.
    """

    for item, value in data.items():

        if isinstance(value, (list, tuple)):  # a list of values
            n = len(value)
            if n == 0:
                raise Exception("Empty arrays are not supported in JSON SPICE kernels.")

            # first if any are strings, check for @ syntax and convert to int
            value = [tparse_wrapper(x) for x in value]  # apply tparse to all elements

            # what is the type of this list?
            if all(isinstance(x, str) for x in value):
                # a list of strings
                t = str
            elif all(isinstance(x, (int, bool, float)) for x in value):
                # a list of integers, floats, bools
                t = float
                value = [float(x) for x in value]
            else:
                raise Exception("Unsupported array type in JSON SPICE kernel.")

        elif isinstance(value, str):
            n = 1
            value = tparse_wrapper(value)
            t = type(value)
            value = [value]

        elif isinstance(value, (int, float, bool)):
            n = 1
            t = float
            value = [float(value)]

        elif isinstance(value, dict):
            raise Exception("Nested dictionaries are not supported in JSON SPICE kernels.")

        # check for += and add to existing variable if it exists
        if item.startswith('+'):

            item = item[1:]
            try:
                n_existing, typeout = dtpool(item)
                found = n_existing > 0 and typeout != 'X'
            except:
                found = False

            if found:
                if typeout == 'C':  # character
                    if t == str:
                        values = [str(s) for s in gcpool(item, 0, n)]
                    else:
                        raise Exception("Cannot add to existing character variable with a non-string value.")
                elif typeout == 'N':  # numeric
                    if t == float:
                        values = [float(x) for x in gdpool(item, 0, n)]
                    else:
                        raise Exception("Cannot add to existing numeric variable with a non-float value.")
                if found:
                    values.extend(value)  # append new values to existing ones
                    value = values
                    dvpool(item)  # delete the existing variable from the pool
                else:
                    raise Exception(f"Variable '{item}' not found in SPICE pool for += operation.")

        # add the variable
        if t == float:
            pdpool ( item, value )
        elif t == str:
            pcpool ( item, value )

def tparse_wrapper(x):
    """wrapper for `tparse` to either return the result or the original string if parsing fails."""
    if isinstance(x, str) and x.startswith('@'):
        # convert to UTC seconds past J2000
        val, msg = tparse(x[1:])
        if msg:
            return x  # as is
        else:
            return val
    else:
        return x
