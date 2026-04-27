import ctypes
import os

class SoupEntry(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("name", ctypes.c_char * 64),
        ("rating", ctypes.c_uint8),
        ("date", ctypes.c_char * 16),
        ("notes", ctypes.c_char * 256),
    ]

class SoupBridge:
    def __init__(self, lib_path="/home/agent-engineer/Auto/build/libsouplog.so"):
        self.lib = ctypes.CDLL(lib_path)
        self.lib.print_soup_entry.argtypes = [ctypes.POINTER(SoupEntry)]
        self.lib.print_soup_entry.restype = None

    def log_telemetry(self, entry_id, name, rating, date, notes):
        entry = SoupEntry()
        entry.id = entry_id
        entry.name = name.encode('utf-8')[:63]
        entry.rating = rating
        entry.date = date.encode('utf-8')[:15]
        entry.notes = notes.encode('utf-8')[:255]
        
        self.lib.print_soup_entry(ctypes.byref(entry))

# Singleton instance
try:
    bridge = SoupBridge()
except Exception as e:
    print(f"Warning: Could not load SoupLog library: {e}")
    bridge = None
