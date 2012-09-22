#!/usr/bin/env python

#===- insert-asserts.py ----- Code Refactoring example -------*- python -*--===#
#
# Very simple example of libclang usage. Process all function in module and
# insert assert that all poiters argument must be not 0.
#
# Ofcouse it not working for all situations but it is only example.
#
# Setup environment before use:
#   export LD_LIBRARY_PATH=<path to libclang.so>
#   export PYTHONPATH=<path to python binding>
#
#===------------------------------------------------------------------------===#

# export LD_LIBRARY_PATH=/Users/snk/usr/soft/llvm/build/lib/
# export PYTHONPATH=/Users/snk/usr/soft/llvm/tools/clang/bindings/python

# TODO: fix windows path names
#
# LIBCLANG_DIR="/Users/snk/usr/soft/llvm/build/lib/"
# LIBCLANG_PY_DIR="/Users/snk/usr/soft/llvm/tools/clang/bindings/python"
# import os,sys
# sys.path.insert(0,LIBCLANG_PY_DIR)
#
# if( os.environ.has_key('LD_LIBRARY_PATH') ):
#    os.environ['LD_LIBRARY_PATH'] += ":" + LIBCLANG_DIR
# else:
#    os.environ['LD_LIBRARY_PATH'] = LIBCLANG_DIR

import clang.cindex
from clang.cindex import Index,CursorKind,TypeKind
from optparse import OptionParser, OptionGroup

rewrite_pool = {}

def append_rewrite_location( file_name, start, end, text_to_insert ):
    """ add text for inserton and location for future processing all at once"""
    global rewrite_pool

    if( rewrite_pool.has_key(file_name) ):
        rewrite_pool[file_name].append([start, end, text_to_insert])
    else:
        rewrite_pool[file_name] = [[start, end, text_to_insert]]

def do_rewrite():
    """ rewrite needed files by text from pool """ 
    global rewrite_pool

    for file_name in rewrite_pool:
      # Some workaround for bypass function defination in system header files
      # maybe better way is filter by path or allow only one file
      if( not (file_name.endswith(".c") or file_name.endswith(".cpp") or file_name.endswith(".cc"))):
        continue

      rewrite_pool[file_name].sort( key = lambda x: x[0])    # sort by insert position

      # I hope nobody doesn't have 1Gb source file :)
      f = file(file_name,"r")
      d = f.read()
      f.close()

      offset = 0
      for p in rewrite_pool[file_name]:
         start = p[0] + offset
         indent = p[1]
         text = "".join( map(lambda s: "\n"+" "*indent+s, p[2]) )
         d = d[:start] + text + d[start:]
         offset += len(text)

      t = file_name.split(".")
      t[-2] += "_v2"
      file_name = ".".join(t)

      print "save: "+file_name

      f = file(file_name,"w")
      f.write(d)
      f.close()

def get_required_children(node, node_kind, amount = None):
    """ support function: get one child of desired type """
    try:
       l = filter( lambda n: n.kind == node_kind, node.get_children())
       if( l and amount ):
          l = l[:amount]
       return l
    except:
       return None

def process_function(func):
    """ Insert asserts in function """
    assert(func.kind == CursorKind.FUNCTION_DECL)
    print "process: " + func.displayname

    args = get_required_children(func,CursorKind.PARM_DECL)
    body = get_required_children(func,CursorKind.COMPOUND_STMT, amount = 1)[0]

    accerts = []

    for arg in args:
       if( arg.type.kind == TypeKind.POINTER ):
          accerts.append("assert(%s != 0);" % arg.displayname)


    if( len(accerts) > 0 ):
       indent = list(body.get_children())[0].location.column

       append_rewrite_location(
          body.extent.start.file.name,  # because we need file name not obj
          body.extent.start.offset + 1, # because insert after '{'
          indent - 1,                   # because counting from 1
          accerts)

def main():
    global opts
    parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")
    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args()

    if len(args) == 0:
        parser.error('invalid number arguments')

    index = Index.create()
    tu = index.parse(None, args)

    if not tu:
        parser.error("unable to load input")

    funcs = filter( lambda node: node.kind == CursorKind.FUNCTION_DECL and node.is_definition(), tu.cursor.get_children() )
    for f in funcs:
       process_function(f)

    do_rewrite()

if __name__ == '__main__':
    main()

