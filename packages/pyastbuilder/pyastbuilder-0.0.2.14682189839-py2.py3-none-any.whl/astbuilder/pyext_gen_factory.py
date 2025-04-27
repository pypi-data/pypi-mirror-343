'''
Created on Mar 23, 2021

@author: mballance
'''
from astbuilder.ast_enum import AstEnum
from astbuilder.ast_flags import AstFlags
from astbuilder.cpp_gen_ns import CppGenNS
from astbuilder.visitor import Visitor


class PyExtGenFactory(Visitor):
    
    def __init__(self,
                 name,
                 namespace,
                 target_pkg,
                 decl_pxd,
                 pxd,
                 pyx,
                 pyi,
                 cpp,
                 hpp):
        self.name = name
        self.namespace = namespace
        self.target_pkg = target_pkg
        self.decl_pxd = decl_pxd
        self.pxd = pxd
        self.pyx = pyx
        self.pyi = pyi
        self.cpp = cpp
        self.hpp = hpp

    def gen(self, ast):
        # Generate a C++ class with 
        # - Holds a handle to a cdef proxy class
        # - py_prefixed visitor methods to be called from Python
        # - un-prefixed visitor methods to be called from C++
        #
        # Generate an import class that mirrors the base visitor
        # Generate an import class in decl_pxd that mirrors this class
        #
        # Generate a cdef class in pyx with just 
        
#        self.gen_factory_imp(ast)
        self.gen_factory(ast)
#        self.gen_py_base_factory(ast)
        
        pass
    
    def gen_factory_imp(self, ast):
        """Generate the decl_pxd view of the base visitor"""

        # Define the AST VisitorBase class
        if self.namespace is not None:
            self.decl_pxd.println("cdef extern from '%s' namespace '%s':" % (
                CppGenNS.incpath(self.namespace, "impl/VisitorBase.h"), self.namespace))
        else:
            self.decl_pxd.println("cdef extern from '%s.h':" % "VisitorBase")
            
        self.decl_pxd.inc_indent()
        self.decl_pxd.println("cpdef cppclass %s:" % "VisitorBase")
        self.decl_pxd.inc_indent()
        for c in ast.classes:
            self.decl_pxd.println("void visit%s(I%sP i)" % (c.name, c.name))
        self.decl_pxd.dec_indent()
        self.decl_pxd.dec_indent()
        
        if self.namespace is not None:
            self.decl_pxd.println("cdef extern from 'PyBaseVisitor.h' namespace '%s':" % self.namespace)
        else:
            self.decl_pxd.println("cdef extern from '%s.h':" % "PyBaseVisitor")
            
        self.decl_pxd.inc_indent()
        self.decl_pxd.println("cpdef cppclass %s(%s):" % ("PyBaseVisitor", "VisitorBase"))
        self.decl_pxd.inc_indent()
        self.decl_pxd.println("PyBaseVisitor(cpy_ref.PyObject *)")
        for c in ast.classes:
            self.decl_pxd.println("void py_visit%s(I%s *i)" % (c.name, c.name))
        self.decl_pxd.dec_indent()
        self.decl_pxd.dec_indent()
        
    def gen_factory(self, ast):
        """Generates cdef class that user can extend"""
        
        self.pxd.println("cdef class ObjFactory(VisitorBase):")
        self.pxd.inc_indent()
        self.pxd.println("cdef bool _obj_owned")
        self.pxd.println("cdef object _obj")
        
        self.pyx.println("cdef class ObjFactory(VisitorBase):")
        self.pyx.inc_indent()
        
        self.pyx.println("def __init__(self):")
        self.pyx.inc_indent()
        self.pyx.println("super().__init__()")
        self.pyx.println("self._obj = None")
        self.pyx.println("self._obj_owned = False")
        self.pyx.dec_indent()

        # self.pyx.println("cpdef mk(self, obj, owned):")
        # self.pyx.inc_indent()
        # self.pyx.println("self._obj = None")
        # self.pyx.println("self._obj_owned = owned")
        # for i,c in enumerate(ast.rootClasses()):
        #     if i == 0:
        #         self.pyx.println("if isinstance(obj, %s):" % c.name)
        #     else:
        #         self.pyx.println("elif isinstance(obj, %s):" % c.name)
        #     self.pyx.inc_indent()
        #     self.pyx.println("self._hndl.py_accept%s((<%s>obj)._hndl)" % (c.name, c.name))
        #     self.pyx.dec_indent()
            
        # self.pyx.println("else:")
        # self.pyx.inc_indent()
        # self.pyx.println("#ralse Exception('Failed to find appropriate root file')")
        # self.pyx.println("pass")
        # self.pyx.dec_indent()
        # self.pyx.println("return self._obj")
        # self.pyx.dec_indent()

        
        for c in ast.classes:
            self.pxd.println("cpdef void visit%s(self, %s i)" % (c.name, c.name))
            
            self.pyx.println("cpdef void visit%s(self, %s i):" % (c.name, c.name))
            self.pyx.inc_indent()
            self.pyx.println("self._obj = i")
            self.pyx.dec_indent()
        self.pyx.dec_indent()
        self.pxd.dec_indent()
        
    def gen_py_base_visitor(self, ast):
        self.hpp.println("#pragma once")

        self.hpp.println("#include \"%s\"" % CppGenNS.incpath(self.namespace, "impl/VisitorBase.h"))

        print("TARGET_PKG: %s" % self.target_pkg)        
        self.hpp.println("#include <Python.h>")
        self.cpp.println("#include \"PyBaseVisitor.h\"")
        if self.target_pkg.find('.') != -1:
            self.cpp.println("#include \"%s_api.h\"" % self.target_pkg[self.target_pkg.find('.')+1:])
        else:
            self.cpp.println("#include \"%s_api.h\"" % self.target_pkg)
        

        CppGenNS.enter(self.namespace, self.hpp)        
        CppGenNS.enter(self.namespace, self.cpp)
       
        # Constructor 
        self.hpp.println("class PyBaseVisitor : public VisitorBase {")
        self.hpp.println("public:")
        self.hpp.inc_indent()
        self.hpp.println("PyBaseVisitor(PyObject *proxy);")
        
        self.cpp.println("PyBaseVisitor::PyBaseVisitor(PyObject *proxy) : m_proxy(proxy) {")
        self.cpp.inc_indent()
        self.cpp.println("import_%s();" % self.target_pkg.replace('.','__'))
        self.cpp.println("Py_XINCREF(m_proxy);")
        self.cpp.dec_indent()
        self.cpp.println("}")
        
        # Destructor 
        self.hpp.println("virtual ~PyBaseVisitor();")
        self.hpp.dec_indent()
        
        self.cpp.println("PyBaseVisitor::~PyBaseVisitor() {")
        self.cpp.inc_indent()
        self.cpp.println("Py_XDECREF(m_proxy);")
        self.cpp.dec_indent()
        self.cpp.println("}")
        
        self.hpp.println("private:")
        self.hpp.inc_indent()
        self.hpp.println("PyObject *m_proxy;")
        
        self.decl_pxd.inc_indent()
        self.hpp.println("public:")
        self.decl_pxd.inc_indent()
        for c in ast.classes:

            # C++-callable visitor method            
            self.hpp.println("virtual void visit%s(I%s *i) override;" % (c.name, c.name))
            self.cpp.println("void PyBaseVisitor::visit%s(I%s *i) {" % (c.name, c.name))
            self.cpp.inc_indent()
            self.cpp.println("%s_call_visit%s(m_proxy, i);" % (self.name, c.name))
            self.cpp.dec_indent()
            self.cpp.println("}")

            # Python-callable visitor method            
            self.hpp.println("void py_visit%s(I%s *i);" % (c.name, c.name))
            self.cpp.println("void PyBaseVisitor::py_visit%s(I%s *i) {" % (c.name, c.name))
            self.cpp.inc_indent()
            self.cpp.println("VisitorBase::visit%s(i);" % c.name)
            self.cpp.dec_indent()
            self.cpp.println("}")
            
            self.pyx.println("cdef public api %s_call_visit%s(object self, %s_decl.I%s *i) with gil:" % 
                             (self.name, c.name, self.name, c.name))
            self.pyx.inc_indent()
            self.pyx.println("self.visit%s(%s.mk(i, False))" % (c.name, c.name))
            self.pyx.dec_indent()
            
        self.decl_pxd.dec_indent()
        self.decl_pxd.dec_indent()

        self.hpp.dec_indent()
        self.hpp.println("};")

        CppGenNS.leave(self.namespace, self.hpp)
        CppGenNS.leave(self.namespace, self.cpp)
        
    def visitAstEnum(self, e:AstEnum):
        pass
        
        

