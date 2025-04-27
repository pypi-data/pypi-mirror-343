
from astbuilder.type_pointer import PointerKind
from astbuilder.type_scalar import TypeScalar, TypeKind

from .type_pointer import TypePointer
from .visitor import Visitor
from astbuilder.ast_enum import AstEnum
from astbuilder.ast_flags import AstFlags
from astbuilder.ast_struct import AstStruct

# pydecl - captures whether we are in a context where a C++ type must be namespace-qualified
# pytype - When true, we want to refer to the 'Python' version of a class type
#          When false, we want to refer to the wrapped C++ version of a class type
#
# pydecl, pytype
# True    True    - In a .pxd file referring to a Python type (empty for Enum)
# False   True    - In a .pyx file referring to a Python type (empty for Enum)
# True    False   - We're in a declaration scope (unclear .pxd or _decl.pxd) using the non-Python type
#                   - Do not qualify with a namespace
#                   - Reference as I<type>
#                   - Use I<type>P for pointer types
# False   False   - We're in the _decl.pxd using a non-Python type

class PyExtCallParamGen(Visitor):
    
    def __init__(self, ns) :
        self.out = ""
        self.ns = ns
        self.param = None
        self.depth = 0
        
    def gen(self, param, t):
        self.out = ""
        self.param = param
        t.accept(self)
        return self.out

    def visitAstEnum(self, e : AstEnum):
        print("is_pydecl=%s is_pytype=%s" % (self.is_pydecl, self.is_pytype))
        # Enums are a strange case
        # - When referenced in _decl.pxd as a parameter (pdecl=True,ptype=False), we have a simple name
        # - When referenced in .pxd/.pyx as a parameter (pdecl=True,ptype=True), we omit the type
        # is_pytype - this refers to a user-facing Python type
        # is_pydecl - 
        if self.is_pydecl and self.is_pytype:
            # In a .pxd file referring to a Python type (empty for Enum)
            pass
        elif not self.is_pydecl and self.is_pytype:
            # In a .pyx file referring to a Python type (empty for Enum)
            # Note: Unsure we do this
#            self.out += self.ns + "."
#            self.out += e.name
            pass
        elif self.is_pydecl and not self.is_pytype:
            # We're in a declaration scope (unclear .pxd or _decl.pxd) using the non-Python type
            self.out += e.name
            pass
        elif not self.is_pydecl and not self.is_pytype:
            # We're in the _decl.pxd using a non-Python type
            self.out += e.name
    
    def visitAstFlags(self, f : AstFlags):
        if not self.is_pytype:
            self.out += f.name
    
    def visitTypeList(self, t):
        if self.depth == 0:
            self.depth += 1
            if self.is_const:
                self.out += "const "
            
            self.out += "std_vector["
            self.out += PyExtTypeNameGen(
                ns=self.ns,
                compressed=self.compressed,
                is_pytype=self.is_pytype,
                is_pydecl=self.is_pydecl).gen(t.t)
            self.out += "]"
        
            if self.is_ret:
                self.out += " &"
            self.depth -= 1
        else:
            self.out += PyExtTypeNameGen(ns=self.ns).gen(t)

    def visitTypeMap(self, t):
        if self.depth == 0:
            self.depth += 1
            if self.is_const:
                self.out += "const "
            
            self.out += "std_map["
            self.out += PyExtTypeNameGen(
                ns=self.ns,
                compressed=self.compressed,
                is_pydecl=self.is_pydecl,
                is_pytype=self.is_pytype).gen(t.kt)
            self.out += ","
            self.out += PyExtTypeNameGen(
                ns=self.ns,
                compressed=self.compressed,
                is_pydecl=self.is_pydecl,
                is_pytype=self.is_pytype).gen(t.vt)
            self.out += "]"
        
            if self.is_ret:
                self.out += " &"
            self.depth -= 1
        else:
            self.out += PyExtTypeNameGen(ns=self.ns).gen(t)
        
    def visitTypePointer(self, t : TypePointer):
        if self.depth == 0:
            self.depth += 1
            if self.is_pytype:
                # Just display the name
                Visitor.visitTypePointer(self, t)
            else:
                if not self.compressed:
                    if t.pt == PointerKind.Shared:
                        self.out += "shared_ptr["
                    elif t.pt == PointerKind.Unique and not self.is_ret:
                        self.out += "%sUP[" % (
                            (("%s_decl." % self.ns) if self.is_pydecl else "")
                        )
                Visitor.visitTypePointer(self, t)
        
                if t.pt == PointerKind.Shared or t.pt == PointerKind.Unique:
                    if not self.compressed:
                        if self.is_ret:
                            if t.pt == PointerKind.Shared:
                                self.out += "]"
                            else:
                                self.out += "P"
                        else:
                            self.out += "]"
                    else:
                        if self.is_ret:
                            if t.pt == PointerKind.Shared:
                                self.out += "SP"
                            else:
                                self.out += "P"
                        else:
                            self.out += "SP" if t.pt == PointerKind.Shared else "UP"
                else:
                    self.out += "P"
            self.depth -= 1
        else:
            self.out += PyExtTypeNameGen(
                ns=self.ns,
                is_pytype=self.is_pytype,
                is_pydecl=self.is_pydecl).gen(t)

    def visitTypeScalar(self, t : TypeScalar):
        if t.t == TypeKind.String:
            self.out += "%s.encode()" % self.param
        else:
            self.out += self.param
    
    def visitAstStruct(self, s : AstStruct):
        if self.is_const:
            self.out += "const "
        self.out += s.name
        if self.is_ref:
            self.out += " &"

    def visitTypeUserDef(self, t):
        print("PyCallParamGen: TypeUserDef")

        if isinstance(t.target, (AstEnum,AstFlags)):
            t.target.accept(self)
        elif isinstance(t.target, (AstStruct,)):
            if self.is_pydecl and self.is_pytype:
                self.out += "%s" % t.name
            elif not self.is_pydecl and self.is_pytype:
                self.out += "%s" % t.name
            elif self.is_pydecl and not self.is_pytype:
                self.out += "%s.%s" % (self.ns, t.name)
            elif not self.is_pydecl and not self.is_pytype:
                self.out += "%s" % t.name
        else:
            if self.is_const:
               self.out += "const "

            if self.is_pydecl and self.is_pytype:
                self.out += "%s" % t.name
            elif not self.is_pydecl and self.is_pytype:
                self.out += "%s" % t.name
            elif self.is_pydecl and not self.is_pytype:
                self.out += "%s_decl.I%s" % (self.ns, t.name)
            elif not self.is_pydecl and not self.is_pytype:
                self.out += "I%s" % t.name

            if self.is_ptr:
                if not self.is_pytype:
                    self.out += "P "
                else:
                    self.out += " "
            if self.is_ref:
                self.out += " &"
        
        