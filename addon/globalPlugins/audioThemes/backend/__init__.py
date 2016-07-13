import sys, os
import ctypes


sys.path.append(os.path.join(os.path.dirname(__file__), 'unspoken', 'deps'))

file_directory = os.path.split(os.path.abspath(__file__))[0]
libaudioverse_directory = os.path.join(file_directory, 'unspoken', 'deps', 'libaudioverse')

dll_hack = [ctypes.cdll.LoadLibrary(os.path.join(libaudioverse_directory, 'libsndfile-1.dll'))]
dll_hack.append(ctypes.cdll.LoadLibrary(os.path.join(libaudioverse_directory, 'libaudioverse.dll')))

import libaudioverse
libaudioverse.initialize()
