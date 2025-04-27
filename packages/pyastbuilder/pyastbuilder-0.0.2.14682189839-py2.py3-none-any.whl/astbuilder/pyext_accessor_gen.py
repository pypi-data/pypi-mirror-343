from astbuilder.pyext_type_name_gen import PyExtTypeNameGen
from astbuilder.pyext_type_name_gen_pyi import PyExtTypeNameGenPyi
from astbuilder.type_pointer import PointerKind
from astbuilder.type_scalar import TypeKind
from astbuilder.visitor import Visitor
from .ast_enum import AstEnum
from .ast_flags import AstFlags
from .pyext_list_accessor_gen import PyExtListAccessorGen
from .pyext_map_accessor_gen import PyExtMapAccessorGen


class PyExtAccessorGen(Visitor):
    # Integer and pointer
    # - const read accessor
    # - non-const write-value accessor
    #
    # String
    # - const-ref read accessor
    # - non-const write accessor
    #
    # List, Map
    # - const-ref read accessor
    # - non-const write accessor
    #
    #
    
    def __init__(self, name, clsname, decl_pxd, pxd, pyx, pyi):
        super().__init__()
        self.name = name
        self.clsname = clsname
        self.pxd = pxd
        self.decl_pxd = decl_pxd
        self.pyx = pyx
        self.pyi = pyi
        self.field = None
        self.decl_pxd_ptr_tgen = PyExtTypeNameGen(
                ns=self.name,
                compressed=True,
                is_pydecl=False,
                is_pytype=False,
                is_ref=False,
                is_const=False)
        self.decl_pxd_cref_tgen = PyExtTypeNameGen(
                ns=self.name,
                compressed=True,
                is_pydecl=False,
                is_pytype=False,
                is_ref=True,
                is_const=True)
        self.pyi_tgen = PyExtTypeNameGenPyi(ns=self.name)
        self.list_accessor_gen = PyExtListAccessorGen(
            name, clsname, decl_pxd, pxd, pyx, pyi)
        self.map_accessor_gen = PyExtMapAccessorGen(
            name, clsname, decl_pxd, pxd, pyx, pyi)
        
    def gen(self, field):
        self.field = field
        self.field.t.accept(self)

    def visitTypeList(self, t):
        self.list_accessor_gen.gen(self.field, t)

        name = self.field.name[0].upper() + self.field.name[1:]
        self.decl_pxd.println(self.nonconst_ref_ret(
            t, 
            is_pydecl=False,
            is_pytype=False) + " get" + name + "();")
        self.pyi.println("def get%s(self) -> %s: ..." % (name, self.pyi_tgen.gen(t)))
        self.pyi.println()
        
    
    def visitTypeMap(self, t):
        self.map_accessor_gen.gen(self.field, t)
        
    def visitTypePointer(self, t):
        name = self.field.name[0].upper() + self.field.name[1:]
        tname = t.t.name

        self.pxd.println("cpdef %s get%s(self)" % (tname, name))
        
        self.pyx.println("cpdef %s get%s(self):" % (tname, name))
        self.pyx.inc_indent()
        self.pyx.println("if self.as%s().get%s() == NULL:" % (self.clsname, name))
        self.pyx.inc_indent()
        self.pyx.println("return None")
        self.pyx.dec_indent()
        self.pyx.println("else:")
        self.pyx.inc_indent()
        self.pyx.println("of = ObjFactory()")
        self.pyx.println("self.as%s().get%s().accept(of._hndl)" % (self.clsname, name))
        self.pyx.println("return <%s>(of._obj)" % tname)
        self.pyx.dec_indent()
        self.pyx.dec_indent()

        if t.pt == PointerKind.Raw:
            self.gen_rawptr_accessors(t)
        elif t.pt == PointerKind.Unique:
            self.gen_uptr_accessors(t)
        elif t.pt == PointerKind.Shared:
            self.gen_sptr_accessors(t)
        else:
            raise Exception("Accessor generation not supported for " + str(self.pt))

        self.pyi.println("def get%s(self) -> %s: ..." % (name, tname))
        self.pyi.println()

    def visitAstClass(self, c):
        self.gen_class_accessors(c)

    def visitAstStruct(self, s):
        self.gen_struct_accessors(s)

    def visitAstEnum(self, e : AstEnum):
        self.gen_enum_accessors(e)
    
    def visitAstFlags(self, f : AstFlags):
        self.gen_enum_accessors(f)

    def visitTypeScalar(self, t):
        if t.t == TypeKind.String:
            self.gen_string_accessors(t)
        else:
            self.gen_scalar_accessors(t)

    def visitTypeUserDef(self, t):
        print("--> visitTypeUserDef")
        t.target.accept(self)
        print("<-- visitTypeUserDef")
        pass
    
    def gen_collection_accessors(self, t):
        name = self.field.name[0].upper() + self.field.name[1:]
        # Generate a read-only accessor
#        self.decl_pxd.println(self.const_ref_ret(t) + "get_" + self.field.name + "()")
#        self.decl_pxd.println()

        # Generate a non-const accessor


#         self.pyx.println("cdef %s get_%s():" % (self.nonconst_ref_ret(t), self.field.name))
#         self.pyx.inc_indent()
#         self.pyx.println("return (<%s_decl.%s *>self._hndl).get_%s()" %
#                          (self.name, self.clsname, self.field.name))
#         self.pyx.dec_indent()

    def gen_class_accessors(self, c):
        print("TODO: class accessor")
        pass

    def gen_struct_accessors(self, s):
        # Generate a read-only accessor
        name = self.field.name[0].upper() + self.field.name[1:]
        self.decl_pxd.println("%s get%s()" % (
            self.decl_pxd_cref_tgen.gen(s),
            name))
        self.decl_pxd.println()

        # Generate a setter
        self.decl_pxd.println("void set%s(%s)" % (
            name,
            self.decl_pxd_cref_tgen.gen(s)))

    def gen_enum_accessors(self, t):
        print("--> gen_enum_accessors %s" % self.field.name)
        name = self.field.name[0].upper() + self.field.name[1:]
        
        # Generate a read-only accessor
        print("--> Generate decl_pxd")
        self.decl_pxd.println(
            self.decl_pxd_ptr_tgen.gen(t) + " get" + name + "()")
        self.decl_pxd.println()
        print("<-- Generate decl_pxd")
        
        
        self.pxd.println("cpdef %s get%s(self)" % 
                         (PyExtTypeNameGen(
                            ns=self.name,compressed=True,
                            is_pytype=True,is_pydecl=True,is_ret=True).gen(t), name))
        
        self.pyx.println("cpdef %s get%s(self):" % 
                         (PyExtTypeNameGen(
                            ns=self.name,compressed=True,
                            is_pytype=True,is_pydecl=True,is_ret=True).gen(t), name))
        self.pyx.inc_indent()
        self.pyx.println("return dynamic_cast[%s_decl.I%sP](self._hndl).get%s()" % 
                         (self.name, self.clsname, name))
        self.pyx.dec_indent()

        # Generate a non-const accessor
        self.decl_pxd.println("void set" + name + "(" +
            self.decl_pxd_ptr_tgen.gen(t) + " v)")
        
        self.pyi.println("def set%s(self, v : %s): ..." % (
            name, 
            self.pyi_tgen.gen(t)))
        self.pyi.println()

        print("<-- gen_enum_accessors %s" % self.field.name)

   
    def gen_scalar_accessors(self, t):
        name = self.field.name[0].upper() + self.field.name[1:]
        
        # Generate a read-only accessor
        self.decl_pxd.println(
            self.decl_pxd_ptr_tgen.gen(t) + " get" + name + "()")
        self.decl_pxd.println()
        
        
        self.pxd.println("cpdef %s get%s(self)" % 
                         (PyExtTypeNameGen(ns=self.name,compressed=True,is_ret=True).gen(t), name))
        
        self.pyx.println("cpdef %s get%s(self):" % 
                         (PyExtTypeNameGen(ns=self.name,compressed=True,is_ret=True).gen(t), name))
        self.pyx.inc_indent()
        self.pyx.println("return dynamic_cast[%s_decl.I%sP](self._hndl).get%s()" % 
                         (self.name, self.clsname, name))
        self.pyx.dec_indent()

        # Generate a non-const accessor
        self.decl_pxd.println("void set" + name + "(" +
            self.decl_pxd_ptr_tgen.gen(t) + " v)")

    def gen_rawptr_accessors(self, t):
        # Generate a read-only accessor
        name = self.field.name[0].upper() + self.field.name[1:]
        self.decl_pxd.println(self.decl_pxd_ptr_tgen.gen(t) + 
            " get" + name + "();")
        self.decl_pxd.println()

        # Generate a setter
        self.decl_pxd.println("void set" + name + "(" +
            self.decl_pxd_ptr_tgen.gen(t) + " v)")

    def gen_uptr_accessors(self, t):
        name = self.field.name[0].upper() + self.field.name[1:]
        
        # Generate a read-only accessor
        self.decl_pxd.println(self.decl_pxd_ptr_tgen.gen(t.t) + 
            " *get" + name + "()")
        self.decl_pxd.println()

        # Generate a setter
        self.decl_pxd.println("void set" + name + "(" + self.decl_pxd_ptr_tgen.gen(t.t) + " *v)")

    def gen_sptr_accessors(self, t):
        name = self.field.name[0].upper() + self.field.name[1:]
        
        # Generate a read-only accessor
        self.decl_pxd.println(
            PyExtTypeNameGen(ns=self.name,compressed=True,is_pydecl=True).gen(t) + " get" + name + "()")
        self.decl_pxd.println()

        # Generate a setter
        self.decl_pxd.println("void set" + name + "(" +
            PyExtTypeNameGen(ns=self.name,compressed=True,is_pydecl=True).gen(t) + " v)")

    def gen_string_accessors(self, t):
        name = self.field.name[0].upper() + self.field.name[1:]
        
        # Generate a read-only accessor
        self.decl_pxd.println(
            PyExtTypeNameGen(ns=self.name,compressed=True,is_pydecl=True,is_ref=True,is_const=True).gen(t) + 
            "get%s()" % name)
        self.decl_pxd.println()

        self.pxd.println("cpdef %s get%s(self)" % (
            "str",
#            PyExtTypeNameGen(ns=self.name,compressed=True,is_ref=False,is_const=False).gen(t),
            name))
        self.pyx.println("cpdef %s get%s(self):" % (
            "str",
#            PyExtTypeNameGen(ns=self.name,compressed=True,is_ref=False,is_const=False).gen(t),
            name))
        self.pyx.inc_indent()
        self.pyx.println("return dynamic_cast[%s_decl.I%sP](self._hndl).get%s().decode()" %
                         (self.name, self.clsname, name))
        self.pyx.dec_indent()

        self.pyi.println("def get%s(self) -> str: ..." % name)
        self.pyi.println()

        # Generate a setter
        self.decl_pxd.println("void set%s(%s v)" % (
            name,
            PyExtTypeNameGen(ns=self.name,compressed=True,is_pydecl=True, is_const=True,is_ref=True).gen(t)
        ))

        self.pxd.println("cpdef void set%s(self, %s v)" % (
            name,
            "str"))
        self.pyx.println("cpdef void set%s(self, %s v):" % (
            name,
            "str"))
        self.pyx.inc_indent()
        self.pyx.println("dynamic_cast[%s_decl.I%sP](self._hndl).set%s(v.encode())" % (
                self.name, self.clsname, name))
        self.pyx.dec_indent()

        self.pyi.println("def set%s(self, v : str): ..." % name)
        self.pyi.println()

    def const_ref_ret(self, t, is_pydecl=False, is_pytype=False):
        return PyExtTypeNameGen(ns=self.name,compressed=True,is_pydecl=is_pydecl,
                                is_pytype=is_pytype, is_ret=True,is_const=True).gen(t)
    
    def nonconst_ref_ret(self, t, is_pydecl=False, is_pytype=False):
        return PyExtTypeNameGen(ns=self.name,compressed=True,is_pydecl=is_pydecl, is_pytype=is_pytype,
                                is_ret=True,is_const=False).gen(t)
    
    