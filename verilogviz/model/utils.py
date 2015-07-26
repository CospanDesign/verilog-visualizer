import sys
import os

class ModuleError(Exception):
    """
    - Module File not found
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

    raise ModuleError("File: %s not found, looked in %s" % (filename, str(user_paths)))
#XXX: This should probably return none, and not an empty string upon failure
#XXX:   perhaps even raise an error


def remove_comments(buf="", debug=False):
    """Remove comments from a buffer.

    Args:
      buf = Buffer to remove the comments from

    Returns:
      A buffer with no verilog comments in it

    Raises:
      Nothing
    """
    #first pass remove the '//' comments
    lines = buf.splitlines()
    if debug:
        print "buf:\n" + buf
    bufx = ""
    for line in lines:
        line = line.partition("//")[0]
        bufx = bufx + line + "\n"
    if debug:
        print "bufx:\n" + bufx

    if debug:
        print "working on /* */ comments\n\n\n"
    #get rid of /*, */ comments
    buf_part = bufx.partition("/*")
    pre_comment = ""
    post_comment = ""
    bufy = bufx
    while (len(buf_part[1]) != 0):
        pre_comment = buf_part[0]
        post_comment = buf_part[2].partition("*/")[2]
        #print "pre_comment: " + pre_comment
        #print "post comment: " + post_comment
        bufy = pre_comment + post_comment
        buf_part = bufy.partition("/*")
        pre_comment = ""
        post_comment = ""

    if debug:
        print "buf:\n" + bufy

    return bufy




def is_module_in_file(filename, module_name, debug = False):
    fbuf = ""

    try:
        filein = open(filename)
        fbuf = filein.read()
        filein.close()
    except IOError as err:
        if debug:
          print "the file is not a full path, searching RTL"

        try:
            filepath = find_rtl_file_location(filename)
            filein = open(filepath)
            fbuf = filein.read()
            filein.close()
        except IOError as err_int:
            if debug:
                print "%s is not in %s" % (module_name, filename)
            return False

    if debug:
        print "Openning file: %s" % filename

    fbuf = remove_comments(fbuf)
    done = False
    module_string = fbuf.partition("module")[2]

    while (not done):
        #remove the parameter and ports list from this possible module
        module_string = module_string.partition("(")[0]
        module_string = module_string.strip("#")
        module_string = module_string.strip()

        if debug:
            print "Searching through: %s" % module_string

        if len(module_string) == 0:
            if debug:
                print "length of module string == 0"
            done = True

        if module_string.endswith("("):
            if debug:
                print "module_string endswith \"(\""
            module_string = module_string.strip("(")

        if debug:
            print "Looking at: %s" % module_string

        if module_string == module_name:
            #Success!
            if debug:
                print "Found %s in %s" % (module_string, filename)
            return True

        elif len(module_string.partition("module")[2]) > 0:
            if debug:
                print "Found another module in the file"
            module_string = module_string.partition("module")[2]

        else:
            done = True

    return False

def _find_module_filename (directory, module_name, debug = False):
    filename = ""

    verilog_files = []
    #get all the verilog files
    for root, dirs, files in os.walk(directory):
        filelist = [os.path.join(root, fi) for fi in files if fi.endswith(".v")]
        for  f in filelist:
            verilog_files.append(f)

    for f in verilog_files:
        if debug:
            print "serching through %s" % f

        if is_module_in_file(f, module_name):
            return f

    raise ModuleError("Searched in standard hdl/rtl location for file \
                    containing the module %s" % module_name)

def find_module_filename (module_name, user_paths = [], debug = False):
    filename = ""
    paths = [os.getcwd()]
    paths.extend(user_paths)

    if debug: print "Search directory: %s" % str(paths)
    for p in paths:
        p = str(p)
        try:
            return _find_module_filename(p, module_name, debug = debug)
        except ModuleError as mnf:
            continue

    raise ModuleError ("Module %s not found: %s" % (module_name, str(paths)))


def _get_file_recursively(directory):
    file_dir_list = glob.glob(directory + "/*")
    file_list = []
    for f in file_dir_list:
        if (os.path.isdir(f)):
            if(f.split("/")[-1] != "sim"):
                file_list += _get_file_recursively(f)
        elif (os.path.isfile(f)):
            if f.endswith(".v"):
                file_list.append(f)

    return file_list


