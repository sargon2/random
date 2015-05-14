#!/usr/bin/env python
import ctypes

lib = ctypes.cdll.LoadLibrary("./lib.so")
print lib.num()
