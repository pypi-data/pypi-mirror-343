'''
Created on May 28, 2022

@author: mballance
'''
from astbuilder.pyext_type_name_gen import PyExtTypeNameGen
from astbuilder.pyext_type_name_gen_pyi import PyExtTypeNameGenPyi
from astbuilder.type_userdef import TypeUserDef
from astbuilder.type_pointer import TypePointer
from astbuilder.ast_enum import AstEnum
from astbuilder.ast_flags import AstFlags

class PyExtGenParams(object):
    
    @classmethod
    def gen_ctor_param_temps(cls, c, out):
        if c.super is not None:
            # Recurse first
            cls.gen_ctor_param_temps(c.super.target, out)
            
        params = list(filter(lambda d : d.is_ctor, c.data))
        for p in params:
            if isinstance(p.t, TypeUserDef) and isinstance(p.t.target, (AstEnum,AstFlags)):
                out.println("cdef int %s_i = int(%s)" % (p.name, p.name))
    
    @classmethod
    def gen_ctor_params(cls, 
        ns, 
        c, 
        out, 
        is_pydecl,  # Are we in a .pxd?
        is_pytype,  # Are we referring to a Python type (vs import)
        ins_self):
        """Returns True if this level (or a previous level) added content"""
        ret = False
            
        if c.super is not None:
            # Recurse first
            ret |= cls.gen_ctor_params(ns, c.super.target, out, is_pydecl, is_pytype, ins_self)
            
        if ins_self and not ret:
            out.write("self")
            ret = True
            
        params = list(filter(lambda d : d.is_ctor, c.data))
        for i,p in enumerate(params):
            if i == 0:
                if ret:
                    out.write(",\n")
                elif ins_self:
                    out.write(",\n")
            out.write(out.ind)
            out.write(PyExtTypeNameGen(
                ns=ns,
                compressed=True,
                is_pytype=is_pytype,
                is_pydecl=is_pydecl,
                is_ret=True).gen(p.t) + " ")
            out.write(p.name + (",\n" if i+1 < len(params) else ""))
            ret = True
        
        return ret    
    
    @classmethod
    def gen_ctor_params_pyi(cls, 
        ns, 
        c, 
        out): 
        """Returns True if this level (or a previous level) added content"""
        ret = False
            
        if c.super is not None:
            # Recurse first
            ret |= cls.gen_ctor_params_pyi(ns, c.super.target, out)
        else:
            out.write("self")

        ret = True

        out.inc_indent()
        params = list(filter(lambda d : d.is_ctor, c.data))
        for i,p in enumerate(params):
            if i == 0:
                out.write(",\n")
            out.write(out.ind)
            out.write(p.name + " : ")
            out.write(PyExtTypeNameGenPyi(ns=ns).gen(p.t))
            out.write((",\n" if i+1 < len(params) else ""))
            ret = True
        out.dec_indent()            

        return ret
    
    @classmethod
    def gen_ctor_pvals(cls, name, c, out):
        ret = False
        if c.super is not None:
            # Recurse first
            ret |= cls.gen_ctor_pvals(name, c.super.target, out)
            
        params = list(filter(lambda d : d.is_ctor, c.data))
        for i,p in enumerate(params):
            if ret and i == 0:
                out.write(",\n")
            out.write(out.ind)
            print("Param type: %s" % str(p.t))
            if isinstance(p.t, TypeUserDef):
                if p.t.target is None:
                    print("Failed to resolve type %s" % p.t.name)
                if isinstance(p.t.target, (AstEnum,AstFlags)):
                    if i+1<len(params):
                        t=",\n"
                    else:
                        t=""
                    
                    out.write("<%s_decl.%s>(%s_i)%s" % (
                        name,
                        p.t.target.name,
                        p.name,
                        t))
                else:
                    if i+1<len(params):
                        t=",\n"
                    else:
                        t=""
                    
                    out.write("dynamic_cast[%s_decl.I%sP](%s_i._hndl)%s" % (
                        name,
                        p.t.target.name,
                        p.name,
                        t))
            elif isinstance(p.t, TypePointer):
                target = p.t.t.name
                out.write("%s.as%s()" % (p.name,target) + (",\n" if i+1 < len(params) else ""))
            else:
                out.write(p.name + (",\n" if i+1 < len(params) else ""))
            ret = True
        
        return ret
