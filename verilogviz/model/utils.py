import sys
import os


class ModuleNotFound(Exception):
   """ModuleNotFound

   Errors associated with searching for a module file location
   usually occurs when the module is not found in the local directory
   or in the rtl files in ibuilder
   """
   pass

def find_rtl_file_location(filename="", user_paths = [], debug=False):
    """Finds a RTL file in the cbuilder rtl directory.

    Args:
        filename: the name of a verilog file to search for
        user_paths: list of paths to search for cbuilder projects

    Returns:
        If found, The absolute path of the verilog module file,
        Otherwise an empty string

    Raises:
      Nothing
    """
    for path in user_paths:
        path = str(path)
        for root, dirs, names in os.walk(path):
            if filename in names:
                return os.path.join(root, filename)

    raise ModuleNotFound("File: %s not found, looked in %s and the default location %s" % (filename, str(user_paths), local_dirs))
#XXX: This should probably return none, and not an empty string upon failure
#XXX:   perhaps even raise an error



