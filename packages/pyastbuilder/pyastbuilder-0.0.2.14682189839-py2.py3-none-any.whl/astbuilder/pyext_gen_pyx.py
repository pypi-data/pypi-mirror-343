'''
Created on Mar 22, 2021

@author: mballance
'''
import itertools

from astbuilder.ast_class import AstClass
from astbuilder.ast_data import AstData
from astbuilder.cpp_gen_ns import CppGenNS
from astbuilder.outstream import OutStream
from astbuilder.pyext_accessor_gen import PyExtAccessorGen
from astbuilder.pyext_gen_ptrdefs import PyExtGenPtrDef
from astbuilder.pyext_type_name_gen import PyExtTypeNameGen
from astbuilder.type_pointer import TypePointer
from astbuilder.type_userdef import TypeUserDef
from astbuilder.visitor import Visitor
from astbuilder.pyext_gen_params import PyExtGenParams
from astbuilder.pyext_gen_utils import PyExtGenUtils


class PyExtGenPyx(Visitor):
    
    def __init__(self,
                 outdir,
                 name, 
                 namespace,
                 target_pkg,
                 decl_pxd,
                 pxd,
                 pyx,
                 pyi):
        self.outdir = outdir
        self.name = name
        self.namespace = namespace
        self.target_pkg = target_pkg
        self.decl_pxd = decl_pxd
        self.pxd = pxd
        self.pyx = pyx
        self.pyi = pyi
        
    def gen(self, ast):
        self.ast = ast
        
        self.pyx.println("# cython: language_level=3")
        self.pxd.println("# cython: language_level=3")
        self.decl_pxd.println("# cython: language_level=3")
        
        self.gen_defs(self.decl_pxd)
        PyExtGenPtrDef(self.decl_pxd).gen(ast)
        self.gen_defs(self.pxd)
#        self.gen_defs(self.pyx)

        self.pyx.println("import ctypes")
        self.pyx.println("import os")
        self.pyx.println("from typing import List, Iterable")
        self.pyx.println("from libc.stdint cimport intptr_t")
        self.pyx.println("from cython.operator cimport dereference") #  as deref

        pkg_elems = self.target_pkg.split(".")
        if len(pkg_elems) > 1:
            self.pxd.println("from %s cimport %s_decl" % (pkg_elems[0], pkg_elems[1]))
            self.pyx.println("from %s cimport %s_decl" % (pkg_elems[0], pkg_elems[1]))
        else:
            self.pxd.println("cimport %s_decl" % self.name)
            self.pyx.println("cimport %s_decl" % self.name)
        
        self.pyx.println("from enum import IntEnum")
        self.pyi.println("from enum import IntEnum, auto")
        self.pyi.println("from typing import Dict, List, Tuple")

        self.pyx.println()
        PyExtGenUtils(self.pyx, self.pyi).gen()
        
        for e in ast.enums:
            if self.namespace is not None:
                self.decl_pxd.println("cdef extern from \"%s\" namespace \"%s\":" % (
                    CppGenNS.incpath(self.namespace, "%s.h"%e.name), self.namespace))
            else:
                self.decl_pxd.println("cdef extern from \"%s.h\":" % e.name)

            self.decl_pxd.inc_indent()
            self.decl_pxd.println("cdef enum %s:" % e.name)
            self.decl_pxd.inc_indent()

            self.pyx.println("class %s(IntEnum):" % e.name)
            self.pyx.inc_indent()
            
            self.pyi.println("class %s(IntEnum):" % e.name)
            self.pyi.inc_indent()
                        
            for i,v in enumerate(e.values):
                if self.namespace is not None:
                    self.decl_pxd.println("%s_%s \"%s\"" % (
                        e.name, v[0], self.namespace + "::" + e.name + "::" + v[0]))
                else:
                    self.decl_pxd.println("%s_%s \"%s\"" % (
                        e.name, v[0], e.name + "::" + v[0]))
                self.pyx.println("%s = %s_decl.%s.%s_%s" % (
                    v[0], self.name, e.name, e.name, v[0]))
                self.pyi.println("%s = auto()" % v[0])
            self.pyi.println()
                
            self.decl_pxd.dec_indent()                
            self.decl_pxd.dec_indent()                
            self.pyx.dec_indent()
            self.pyi.dec_indent()

        for e in ast.structs:
            if self.namespace is not None:
                self.decl_pxd.println("cdef extern from \"%s\" namespace \"%s\":" % (
                    CppGenNS.incpath(self.namespace, "%s.h"%e.name), self.namespace))
            else:
                self.decl_pxd.println("cdef extern from \"%s.h\":" % e.name)
            self.decl_pxd.inc_indent()
            self.decl_pxd.println("cdef cppclass %s:" % e.name)
            self.decl_pxd.inc_indent()
            for d in e.data:
                self.decl_pxd.println(
                    PyExtTypeNameGen(ns=self.name,compressed=True,is_ref=False,is_const=False).gen(d.t) + " %s" % d.name)
            if len(e.data) == 0:
                self.decl_pxd.println("pass")
            self.decl_pxd.dec_indent()
            self.decl_pxd.dec_indent()

            pass

        for e in ast.flags:
            if self.namespace is not None:
                self.decl_pxd.println("cdef extern from \"%s\" namespace \"%s\":" % (
                    CppGenNS.incpath(self.namespace, "%s.h"%e.name), self.namespace))
            else:
                self.decl_pxd.println("cdef extern from \"%s.h\":" % e.name)

            self.decl_pxd.inc_indent()
            self.decl_pxd.println("cdef enum %s:" % e.name)
            self.decl_pxd.inc_indent()

            self.pyx.println("class %s(IntEnum):" % e.name)
            self.pyx.inc_indent()

            self.pyi.println("class %s(IntEnum):" % e.name)
            self.pyi.inc_indent()
                        
            for i,v in enumerate(e.values):
                if self.namespace is not None:
                    self.decl_pxd.println("%s_%s \"%s\"" % (
                        e.name, v, self.namespace + "::" + e.name + "::" + v))
                else:
                    self.decl_pxd.println("%s_%s \"%s\"" % (
                        e.name, v, e.name + "::" + v))
                self.pyx.println("%s = %s_decl.%s.%s_%s" % (
                    v, self.name, e.name, e.name, v))
                self.pyi.println("%s = auto()" % v)
            self.pyi.println()
                
            self.decl_pxd.dec_indent()                
            self.decl_pxd.dec_indent()                
            self.pyx.dec_indent()
            self.pyi.dec_indent()

        self.gen_factory_decl()
        self.gen_factory()
        
        ast.accept(self)
        
    
    def gen_defs(self, out):
        out.println("from enum import IntEnum")
        out.println("from libcpp.cast cimport dynamic_cast")
        out.println("from libcpp.cast cimport reinterpret_cast")
        out.println("from libcpp.cast cimport static_cast")
        out.println("from libcpp.string cimport string as      std_string")
        out.println("from libcpp.map cimport map as            std_map")
        out.println("from libcpp.unordered_map cimport unordered_map as  std_unordered_map")
        out.println("from libcpp.memory cimport unique_ptr, shared_ptr")
        out.println("from libcpp.vector cimport vector as std_vector")
        out.println("from libcpp.utility cimport pair as  std_pair")
        out.println("from libcpp cimport bool as          bool")
        out.println("cimport cpython.ref as cpy_ref")
        out.println("from cython.operator cimport dereference") #  as deref
        out.println()

        out.println("cdef extern from \"zsp/ast/impl/UP.h\" namespace \"zsp::ast\":")
        out.inc_indent()
        out.println("cpdef cppclass UP[T](unique_ptr[T]):")
        out.inc_indent()
        out.println("UP()")
        out.println("UP(T *, bool)")
        out.println("T *get()")
        out.dec_indent()
        out.dec_indent()
              
        out.println()

        out.println("ctypedef char                 int8_t")
        out.println("ctypedef unsigned char        uint8_t")
        out.println("ctypedef short                int16_t")
        out.println("ctypedef unsigned short       uint16_t")
        out.println("ctypedef int                  int32_t")
        out.println("ctypedef unsigned int         uint32_t")
        out.println("ctypedef long long            int64_t")
        out.println("ctypedef unsigned long long   uint64_t")
        out.println()
        

    def gen_factory_decl(self):
        self.decl_pxd.println("ctypedef IFactory *IFactoryP")
        if self.namespace is not None:
            self.decl_pxd.println("cdef extern from \"%s\" namespace \"%s\":" % (
                CppGenNS.incpath(self.namespace, "IFactory.h"), self.namespace))
        else:
            self.decl_pxd.println("cdef extern from \"IFactory.h\":")
        self.decl_pxd.inc_indent()
        
        self.decl_pxd.println("cdef cppclass IFactory:")
        self.decl_pxd.inc_indent()
        for c in self.ast.classes:
            name = c.name[0].upper() + c.name[1:]
            self.decl_pxd.println("I%s *mk%s(" % (c.name, name))
            self.decl_pxd.inc_indent(2)
            have_params = PyExtGenParams.gen_ctor_params(
                self.name, c, self.decl_pxd, is_pydecl=False, is_pytype=False, ins_self=False)
            if have_params:
                self.decl_pxd.write(")\n")
            else:
                self.decl_pxd.println(")")
            self.decl_pxd.dec_indent(2)

        self.decl_pxd.dec_indent()
        self.decl_pxd.dec_indent()
        
    def gen_factory(self):
        self.pyx.println("cdef Factory _inst = None")
        self.pxd.println("cdef class Factory(object):")
        self.pyx.println("cdef class Factory(object):")
        self.pyi.println("class Factory(object):")
        self.pxd.inc_indent()
        self.pyx.inc_indent()
        self.pyi.inc_indent()
        self.pxd.println("cdef %s_decl.IFactory *_hndl" % (self.name,))

        for c in self.ast.classes:
            name = c.name[0].upper() + c.name[1:]
            self.pxd.write("%scpdef %s mk%s(" % (self.pxd.ind, c.name, name))
            PyExtGenParams.gen_ctor_params(
                self.name, c, self.pxd, is_pydecl=False, is_pytype=True, ins_self=True)
            self.pxd.write(")\n")
            self.pyi.write("%sdef mk%s(" % (self.pyi.ind, name))
            PyExtGenParams.gen_ctor_params_pyi(self.name, c, self.pyi)
            self.pyi.write(") -> '%s': ...\n" % c.name)

            self.pyx.print("cpdef %s mk%s(" % (c.name, name))
            self.pyx.inc_indent(2) 
            PyExtGenParams.gen_ctor_params(
                self.name, c, self.pyx, is_pydecl=False, is_pytype=True, ins_self=True)
            self.pyx.dec_indent(2) 
            self.pyx.write("):\n")
            self.pyx.inc_indent()
            PyExtGenParams.gen_ctor_param_temps(c, self.pyx)
            self.pyx.println("return %s.mk(self._hndl.mk%s(" % (c.name, name))
            self.pyx.inc_indent(2)
            PyExtGenParams.gen_ctor_pvals(self.name, c, self.pyx)
            self.pyx.dec_indent(2)
            self.pyx.write("), True)\n")
            self.pyx.dec_indent()

        self.pyx.println("@staticmethod")
        self.pxd.println("@staticmethod")
        self.pxd.println("cdef mk(%s_decl.IFactory *hndl)" % (self.name,))
        self.pyx.println("cdef mk(%s_decl.IFactory *hndl):" % (self.name,))
        self.pyx.inc_indent()
        self.pyx.println("ret = Factory()")
        self.pyx.println("ret._hndl = hndl")
        self.pyx.println("return ret")
        self.pyx.dec_indent()

        self.pyx.println("@staticmethod")
        self.pyx.println("def inst():")
        self.pyx.inc_indent()
        self.pyx.println("cdef Factory factory")
        self.pyx.println("global _inst")
        self.pyx.println("if _inst is None:")
        self.pyx.inc_indent()
        self.pyx.println("ext_dir = os.path.dirname(os.path.abspath(__file__))")
        self.pyx.println("build_dir = os.path.abspath(os.path.join(ext_dir, \"../../build\"))")
        self.pyx.println("libname = \"lib%s.so\"" % self.name)
        self.pyx.println("core_lib = None")
        self.pyx.println("for libdir in (\"lib\", \"lib64\"):")
        self.pyx.inc_indent()
        self.pyx.println("if os.path.isfile(os.path.join(build_dir, libdir, libname)):")
        self.pyx.inc_indent()
        self.pyx.println("core_lib = os.path.join(build_dir, libdir, libname)")
        self.pyx.println("break")
        self.pyx.dec_indent()
        self.pyx.dec_indent()
        self.pyx.println("if core_lib is None:")
        self.pyx.inc_indent()
        self.pyx.println("core_lib = os.path.join(ext_dir, \"lib%s.so\")" % self.name)
        self.pyx.dec_indent()
        self.pyx.println("if not os.path.isfile(core_lib):")
        self.pyx.inc_indent()
        self.pyx.println("raise Exception(\"Extension library core \\\"%s\\\" doesn't exist\" % core_lib)")
        self.pyx.dec_indent()
        self.pyx.println("so = ctypes.cdll.LoadLibrary(core_lib)")
        self.pyx.println("func = so.%s_getFactory" % self.name)
        self.pyx.println("func.restype = ctypes.c_void_p")
        self.pyx.println("")
        self.pyx.println("hndl = <%s_decl.IFactoryP>(<intptr_t>(func()))" % self.name)
        self.pyx.println("factory = Factory()")
        self.pyx.println("factory._hndl = hndl")
#        self.pyx.println("factory.init(dm_core.Factory.init())")
        self.pyx.println("_inst = factory")
        self.pyx.dec_indent()

        self.pyx.println("return _inst")
        self.pyx.dec_indent()

        self.pyi.println("@staticmethod")
        self.pyi.println("def inst() -> 'Factory': ...")
        self.pyi.println()
        
        self.pxd.dec_indent()
        self.pyx.dec_indent()
        self.pyi.dec_indent()

    def visitAstClass(self, c : AstClass):
        
        # Generate the prototype that goes in the .decl_pxd
        if self.namespace is not None:
            self.decl_pxd.println("cdef extern from \"%s\" namespace \"%s\":" % (
                CppGenNS.incpath(self.namespace, "I%s.h"%c.name), self.namespace))
        else:
            self.decl_pxd.println("cdef extern from \"I%s.h\":" % c.name)
            
        self.decl_pxd.inc_indent()
        
        if c.super is not None:
            self.decl_pxd.println("cpdef cppclass I%s(%s):" % (
                c.name, 
                PyExtTypeNameGen(ns=self.name,is_pytype=False,is_pydecl=False).gen(c.super)))
        else:
            self.decl_pxd.println("cpdef cppclass I%s:" % c.name)
            
        self.decl_pxd.inc_indent()
        
        # Generate the wrapper that goes in the .pyx
        if c.super is not None:
            self.pyx.println("cdef class %s(%s):" % (
                c.name, PyExtTypeNameGen(ns=self.name,is_pytype=True).gen(c.super)))
            self.pxd.println("cdef class %s(%s):" % (
                c.name, PyExtTypeNameGen(self.name, is_pytype=True).gen(c.super)))
            self.pyi.println("class %s(%s):" % (
                c.name, PyExtTypeNameGen(self.name, is_pytype=True).gen(c.super)))
            if c.doc is not None:
                self.pyi.inc_indent()
                self.pyi.println("\"\"\"")
                for line in c.doc.split('\n'):
                    self.pyi.println(line)
                self.pyi.println("\"\"\"")
                self.pyi.dec_indent()
        else:
            self.pyx.println("cdef class %s(object):" % c.name)
            self.pxd.println("cdef class %s(object):" % c.name)
            self.pyi.println("class %s(object):" % c.name)
            
                        
        self.pyx.inc_indent()
        self.pxd.inc_indent()
        self.pyi.inc_indent()

        self.pyi.println("pass")
        
        if c.super is None:
            self.pxd.println("cdef %s_decl.I%s    *_hndl" % (self.name, c.name))
            self.pxd.println("cdef bool           _owned")
            
        self.pyx.println()
        self.pxd.println()
        self.pyi.println()
            
        if c.super is None:
            self.pyx.println("def __dealloc__(self):")
            self.pyx.inc_indent()
            self.pyx.println("if self._owned and self._hndl != NULL:")
            self.pyx.inc_indent()
            self.pyx.println("del self._hndl")
            self.pyx.println("self._hndl = NULL")
            self.pyx.dec_indent()
            self.pyx.dec_indent()
            self.pyx.println()
            
            self.pyx.println("cpdef void accept(self, VisitorBase v):")
            self.pyx.inc_indent()
            self.pyx.println("self._hndl.accept(v._hndl)")
            self.pyx.dec_indent()
            self.pyx.println()
            
            self.pxd.println("cpdef void accept(self, VisitorBase v)")

            self.pxd.println("cpdef int id(self)")
            self.pyx.println("cpdef int id(self):")
            self.pyx.inc_indent()
            self.pyx.println("return reinterpret_cast[intptr_t](self._hndl)")
            self.pyx.dec_indent()
#            self.pxd.println("def int __hash__(self)")
            self.pyx.println("def __hash__(self):")
            self.pyx.inc_indent()
            self.pyx.println("return reinterpret_cast[intptr_t](self._hndl)")
            self.pyx.dec_indent()
            self.pyx.println()
#            self.pxd.println("def bool __eq__(self, %s o)" % c.name)
            self.pyx.println("def __eq__(self, o):")
            self.pyx.inc_indent()
            self.pyx.println("oh = <%s>(o)" % c.name)
            self.pyx.println("return self._hndl == oh._hndl")
            self.pyx.dec_indent()
            self.pyx.println()


        self.pyx.println("cdef %s_decl.I%s *as%s(self):" % (self.name, c.name, c.name))
        self.pyx.inc_indent()
        self.pyx.println("return dynamic_cast[%s_decl.I%sP](self._hndl)" % (self.name, c.name))
        self.pyx.dec_indent()

        self.pxd.println("cdef %s_decl.I%s *as%s(self)" % (self.name, c.name, c.name))

        self.pyx.println("@staticmethod")
        self.pyx.println("cdef %s mk(%s_decl.I%s *hndl, bool owned):" % (c.name, self.name, c.name))
        self.pyx.inc_indent()
        self.pyx.println("'''Creates a Python wrapper around native class'''")
        self.pyx.println("ret = %s()" % c.name)
        self.pyx.println("ret._hndl = hndl")
        self.pyx.println("ret._owned = owned")
        self.pyx.println("return ret")
        self.pyx.dec_indent()
        self.pyx.println()
        
        self.pxd.println("@staticmethod")
        self.pxd.println("cdef %s mk(%s_decl.I%s *hndl, bool owned)" % (c.name, self.name, c.name))
        
        # TODO: Handle ctor parameters        
#         self.pyx.println("@staticmethod")
#         if len(c.data) == 0:
#             self.pyx.println("def create():")
#         else:
#             self.pyx.println("def create(")
#             self.pyx.inc_indent()
#             self.gen_ctor_params(c, True, self.pyx)
#             self.pyx.dec_indent()
#             self.pyx.write("):\n")
#         self.pyx.inc_indent()
#         self.pyx.println("'''Creates a Python wrapper around a new native class'''")
#         self.pyx.println("ret = %s()" % c.name)
#         if len(params) == 0:
#             self.pyx.println("ret._hndl = new %s_decl.%s()" % (self.name, c.name))
#         else:
#             self.pyx.write("%sret._hndl = new %s_decl.%s(" % (self.pyx.ind, self.name, c.name))
#             for i,p in enumerate(params):
#                 if i>0:
#                     self.pyx.write(", ")
#                 # TODO: ref '_hndl' if it is a user-defined type
#                 if isinstance(p.t, TypePointer):
#                     self.pyx.write("<%s_decl.%s *>%s._hndl" % (self.name, 
#                         PyExtTypeNameGen(is_pyx=True).gen(p.t), p.name))
#                 else:
#                     self.pyx.write("%s" % p.name)
#             self.pyx.write(")\n")
#                 
#         self.pyx.println("ret._owned = True")
#         self.pyx.println("return ret")
#         self.pyx.dec_indent()
#         self.pyx.println()

        for d in c.data:
            PyExtAccessorGen(self.name, c.name, self.decl_pxd, self.pxd, self.pyx, self.pyi).gen(d)

        if len(c.data) == 0:
            self.decl_pxd.println("pass")
            
        if c.super is None:
            self.decl_pxd.println("void accept(VisitorBase *v)")
            
        self.decl_pxd.dec_indent()
        self.pyx.dec_indent()
        self.pxd.dec_indent()
        
        self.decl_pxd.dec_indent()        
        self.pyx.dec_indent()        
        self.pxd.dec_indent()
        self.pyi.dec_indent()
        
        self.decl_pxd.println()
        self.pyx.println()
        self.pxd.println()

    def visitAstData(self, d:AstData):
        print("visitAstData")
        
    def gen_ctor_params(self, 
                        c, 
                        is_pyx,
                        out):
        """Returns True if this level (or a previous level) added content"""
        ret = False
        if c.super is not None:
            # Recurse first
            ret |= self.gen_ctor_params(c.super.target, is_pyx, out)
            
        params = list(filter(lambda d : d.is_ctor, c.data))
        for i,p in enumerate(params):
            if ret and i == 0:
                out.write(",\n")
            out.write(out.ind)
            out.write(PyExtTypeNameGen(ns=self.name,compressed=True,is_pyx=is_pyx, is_ret=True).gen(p.t) + " ")
            out.write(p.name + (",\n" if i+1 < len(params) else ""))
            ret = True
        
        return ret        
    
    def collect_ctor_params(self, c):
        if c.super is not None:
            params = self.collect_ctor_params(c.super.target)
        else:
            params = []
            
        params.extend(list(filter(lambda d : d.is_ctor, c.data)))
        
        return params
