# Core do simulador, este arquivo converte a AST em codigo intermediario (usando llvmlite)
#Desta forma, cada um dos metodos abaixo fazem a converção de algum "Ramo" em uma estrutura que seja processada pela máquina




from llvmlite import ir
import llvmlite.binding as llvm
import constants as c
import copy
import numpy as np
import llvm_binder


#Inicializando llvm e pegando informações sobre o processamento da máquina que executa o simulador
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

#Algumas constantes para facilitar a codificação
i32 = ir.IntType(64)
i1 = ir.IntType(1)
f32 = ir.FloatType()
i128 = ir.IntType(128)


#Pega a referencia das funções e variavéis declaradas dentro do codigo
#Ref Type, is referece memory location (no copy refrence), this is true real obeject memory

def ir_type(string):
    if "ref" in string:
        if "int" in string:
            return ir.PointerType(i32)
        return ir.PointerType(f32)
    if "int" in string:
        return i32
    #if "sfloat" in string:
     #   return f32
    #if "float" in string:
     #   return f32
    return ir.VoidType()



#Exetern mecanismo usado para chamar funções dentro do codigo (CallFunc) 

def externs(extern, module, *sysArgs):
    returnType = ir_type(extern["ret_type"])

    args = list()
    if "tdecls" in extern:
        for arg in extern["tdecls"]["types"]:
            args.append(ir_type(arg))

    if extern["globid"] == "getarg":
        getArg(module, *sysArgs)

    elif extern["globid"] == "getargf":
        getArgf(module, *sysArgs)
        pass

    else:
        fnty = ir.FunctionType(returnType, args)  
        func = ir.Function(module, fnty, name=extern["globid"])


#Localiza e aloca memoria para os possiveis parametros dentro do codigo 
def getArg(module,  sysArgs):
    sysArgs = [
        int(float(value)) for value in sysArgs
    ]
    array_type = ir.ArrayType(i32, len(sysArgs))
    arr = ir.Constant(array_type, sysArgs)

    fnty = ir.FunctionType(i32, [i32])
    func = ir.Function(module, fnty, name = "getarg")
    entry = func.append_basic_block("entry")
    builder = ir.IRBuilder(entry)

    ptr = builder.alloca(array_type)

    #function arguments (which is the index)
    index = func.args[0]
    ptr_arg = builder.alloca(i32)
    builder.store(index, ptr_arg)
    value = builder.load(ptr_arg)


    for number, arg in enumerate(sysArgs):
        int_1 = ir.Constant(i32, arg)

        
        builder.insert_value(arr, int_1, number)
    builder.store(arr, ptr)


    int_0 = ir.Constant(i32, 0)

    address = builder.gep(ptr, [int_0,value])
    builder.ret(builder.load(address))


def getArgf(module, sysArgs):
    sysArgs = [float(value) for value in sysArgs]
    array_type = ir.ArrayType(f32, len(sysArgs))
    arr = ir.Constant(array_type, sysArgs)

    fnty = ir.FunctionType(f32, [i32])
    func = ir.Function(module, fnty, name = "getargf")
    entry = func.append_basic_block("entry")
    builder = ir.IRBuilder(entry)

    ptr = builder.alloca(array_type)

    #function arguments (which is the index)
    index = func.args[0]
    ptr_arg = builder.alloca(i32)
    builder.store(index, ptr_arg)
    value = builder.load(ptr_arg)


    for number, arg in enumerate(sysArgs):
        float_1 = ir.Constant(f32, arg)
        builder.insert_value(arr, float_1, number)
    builder.store(arr, ptr)

    int_0 = ir.Constant(i32, 0)

    address = builder.gep(ptr, [int_0,value])
    builder.ret(builder.load(address))


#Func todo o codigo escrito no simulador e visto com um programa (função), esse metodo cria a estrutrua basica para executar
#cada uma das funções existentes no codigo.


def funcs(ast, module, known_funcs):
    func_name = ast["globid"]
    symbols = {}
    symbols['cint'] = set()
    symbols[c.cint_args] = {}
    symbols[c.cint_args][func_name] = []

    returnType = ir_type(ast['ret_type'])
    # find arguments
    argument_types = list()
    args = ()
    if "vdecls" in ast:
        funcArgs = vdecls(ast["vdecls"], symbols, func_name)
        argument_types = funcArgs[0]
        args = funcArgs[1]

    fnty = ir.FunctionType(returnType, argument_types)
    func = ir.Function(module, fnty, name=func_name)
    known_funcs[func_name] = (fnty, symbols[c.cint_args][func_name]) # add parameter info
    populate_known_funcs(symbols, known_funcs)


    entry = func.append_basic_block('entry')
    builder = ir.IRBuilder(entry)

    for index, value in enumerate(func.args):
        var_name = args[index]
        var_type = argument_types[index]

        if var_type.is_pointer:
            ptr = value
            symbols[var_name] = ptr
        else:
            ptr = builder.alloca(var_type)
            symbols[var_name] = ptr
            builder.store(value, ptr)

    returned = pure_blk(ast["blk"], builder, symbols)
    if ast[c.ret_type] == 'void':
        builder.ret_void()
        return fnty
    if not returned:
        raise RuntimeError("A função não possui retorno valido!")


def pure_blk(blk, builder, symbols):
    if c.contents not in blk:
        return None
    legacy = copy.copy(symbols)
    returned = False
    for statement in blk[c.contents][c.stmts]:
        returned = stmt(statement, builder, legacy) or returned
        if returned:
            return returned
    return returned


def populate_known_funcs(symbols, known_funcs):
    for name, t in known_funcs.items():
        symbols[name] = t[0]
        symbols[c.cint_args][name] = t[1] 



#processa declaração de variaveis da AST
def vdecls(vdec, symbols, function_name):
    variables = vdec["vars"]
    variableList = list()
    args = list()
    for i in variables:
        if "cint" in i["type"]:
            symbols["cint"].add(i["var"])
            symbols[c.cint_args][function_name].append(True)
        else:
            symbols[c.cint_args][function_name].append(False)
        variableList.append(ir_type(i["type"]))
        args.append(i["var"])
    return [variableList, args]


def blk_stmt(stmt, builder, symbols):
    return pure_blk(stmt[c.contents], builder, symbols)


#Cada função tem dentro de seus blocos stmt, que podem ser vazios ou processar alguma informação, declaração, if, while, callfunc, exp, operações, etc
def stmt(ast, builder, symbols):
    name = ast["name"]

    if name == 'while':
        whileStmt(ast, builder, symbols)

    elif name == 'stmtEqual':
        if ast[c.var] in symbols:
            array(ast, builder, symbols)
        else:
            raise RuntimeError('A variavel :   ' + str(ast[c.var]) + '   não foi definida!')
    elif name == 'stmtOpera':
        arrayOpera(ast, builder, symbols)

    elif name == 'if':
        return ifStmt(ast, builder, symbols)

    elif name == 'ret':
        return returnStmt(ast, builder, symbols)

    elif name == 'vardeclstmt':
        vardeclstmt(ast, builder, symbols)

    elif name == 'expstmt':
        
        # stmt : exp Semicolon
        expression(ast[c.exp], symbols, builder)

    elif name == 'blk':
        return blk_stmt(ast, builder, symbols)

    elif name == c.printStmt:
        printStmt(ast, builder, symbols)

    else:
        raise RuntimeError('Código não foi processado corretamente. Verifique o código fonte:   ' + str(ast))



# Estrutura que processa vetores (Ou o que o simulador entende por vetors)
#
# O sistema inica vetores de forma altomatica, isto é não existe uma "expressão" que inicia um vetor diretamete
# Esse inicio é feito quando o programador chama EX:
# Array[1]+ 1;, ou Array[a]+1; ou a = Array[] (esse retorna o produto dos primos elevados aos index do vetor, que na pratica é um numero natural)  
# A estrutura se manten vida dentro do escopo do metodo

def arrayOpera(ast, builder, symblos):

    i32_0 = ir.Constant(i32, 0)

    if ast[c.op] == "+":
        

        if ast[c.var] in symblos:
            value_op = builder.load(symblos[ast[c.var]])

            if '#array' in symblos:
                      
                array_poiter = builder.gep(symblos['#array'], [i32_0, value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.add(array_i_value, valor_somado, name="add")
                builder.store(new_value_index, array_poiter)
            else:
                array_example =[0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #print(array_example)
                array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
                arr = ir.Constant(array_type, array_example)
                ptr = builder.alloca(array_type) #allocate memory
                builder.store(arr, ptr)
                symblos['#array'] = ptr            
                array_poiter = builder.gep(symblos['#array'],[i32_0,value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.add(array_i_value, valor_somado, name="add")
                builder.store(new_value_index, array_poiter)
        else:

            
            value_op = ir.Constant(i32, ast['var'])
            #builder.store(ast[c.var], value_op)
            

            if '#array' in symblos:
                
                
                array_poiter = builder.gep(symblos['#array'], [i32_0, value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.add(array_i_value, valor_somado, name="add")
                builder.store(new_value_index, array_poiter)
            else:
                array_example =[0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #print(array_example)
                array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
                arr = ir.Constant(array_type, array_example)
                ptr = builder.alloca(array_type) #allocate memory
                builder.store(arr, ptr)
                symblos['#array'] = ptr            
                array_poiter = builder.gep(symblos['#array'],[i32_0,value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.add(array_i_value, valor_somado, name="add")
                builder.store(new_value_index, array_poiter)
    else:

        
        if ast[c.var] in symblos:
            value_op = builder.load(symblos[ast[c.var]])

            if '#array' in symblos:               


                array_poiter = builder.gep(symblos['#array'], [i32_0, value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.sub(array_i_value, valor_somado, name="sub")
                builder.store(new_value_index, array_poiter)
            else:
                array_example =[0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #print(array_example)
                array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
                arr = ir.Constant(array_type, array_example)
                ptr = builder.alloca(array_type) #allocate memory
                builder.store(arr, ptr)
                symblos['#array'] = ptr            
                array_poiter = builder.gep(symblos['#array'],[i32_0,value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.sub(array_i_value, valor_somado, name="sub")
                builder.store(new_value_index, array_poiter)
        else:

            value_op = ir.Constant(i32, ast[c.var])

            if '#array' in symblos:
                                
                array_poiter = builder.gep(symblos['#array'], [i32_0, value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.sub(array_i_value, valor_somado, name="sub")
                builder.store(new_value_index, array_poiter)
            else:
                array_example =[0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                #print(array_example)
                array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
                arr = ir.Constant(array_type, array_example)
                ptr = builder.alloca(array_type) #allocate memory
                builder.store(arr, ptr)
                symblos['#array'] = ptr            
                array_poiter = builder.gep(symblos['#array'],[i32_0,value_op])
                array_i_value = builder.load(array_poiter)
                valor_somado = ir.Constant(i32, ast[c.value])

                new_value_index = builder.sub(array_i_value, valor_somado, name="sub")
                builder.store(new_value_index, array_poiter)


        
# INDEX OUT OF RANGE NEED SOLVER....
def array(ast, builder, symbols):

    if ast[c.array][c.value] == None:
        
        
        symbol_table = {}

        if '#array' in symbols:
            symbol_table['vetor'] = symbols['#array']

        else:

            array_example =[0,0,0,0,0,0,0,0,0,0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            #print(array_example)
            array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
            arr = ir.Constant(array_type, array_example)
            ptr = builder.alloca(array_type) #allocate memory
            builder.store(arr, ptr)

            symbols['#array'] = ptr
            symbol_table['vetor'] = ptr






        i32_100 = ir.Constant(i32, 100)
        i32_0 = ir.Constant(i32, 0)
        i32_1 = ir.Constant(i32, 1)
        
        array_prime = [2,3,5,7,11,13,17,19,23,31,
        37,41,43,47,53,59,61,67,71,73,
        79,83,97,101,103,107,109,113,127,131,
        137,139,149,151,157,163,167,173,179,181,
        191,193,197,199,211,223,227,229,233,239,
        241,251,257,263,269,271,277,281,283,293,
        307,311,313,317,331,337,347,349,353,359,
        367,373,379,383,389,397,401,409,419,421,
        431,433,439,443,449,457,461,463,467,479,
        487,491,499,503,509,521,523,523,541,547]

        array_type = ir.ArrayType(i32, 100)
        arr = ir.Constant(array_type, array_prime)
        ptr = builder.alloca(array_type)
        builder.store(arr, ptr)

        symbol_table["#array_prime"] = ptr



        value_array = builder.alloca(i32)
        builder.store(i32_1, value_array)


        symbol_table["value_array"] = value_array


        for_body_block = builder.append_basic_block("for_body_externo")
        for_after_block = builder.append_basic_block("for_after_externo")

        for_body_block_interno = builder.append_basic_block("for_body")
        for_after_block_interno = builder.append_basic_block("for_after")



        


        #iniciando o for(int i = 0; ...)

        i_ptr = builder.alloca(i32)
        i_value = ir.Constant(i32, 0)
        builder.store(i_value, i_ptr)

        symbol_table["i"]=i_ptr


        #Fazendo i< 28; Quando i =0

        current_i_value = builder.load(symbol_table["i"])

        cond_head = builder.icmp_signed('<', current_i_value, i32_100, name="lt")

        builder.cbranch(cond_head, for_body_block, for_after_block)
        builder.position_at_start(for_body_block)

        current_i_value = builder.load(symbol_table["i"])
        array_i_ponter = builder.gep(symbol_table["vetor"], [i32_0, current_i_value])
        max_j_value = builder.load(array_i_ponter)

        
        

        #operação do for


        # Aqui dentro tem q fazer o segundo for       



        
        
        #iniciando o for(int i = 0; ...)

        j_ptr = builder.alloca(i32)
        j_value = ir.Constant(i32, 0)
        builder.store(j_value, j_ptr)

        symbol_table["j"]=j_ptr

        #Fazendo i< 28; Quando i =0

        current_j_value = builder.load(symbol_table["j"])

        cond_head_interno = builder.icmp_signed('<', current_j_value, max_j_value, name="lt")

        builder.cbranch(cond_head_interno, for_body_block_interno, for_after_block_interno)
        builder.position_at_start(for_body_block_interno)




        value_atual = builder.load(symbol_table["value_array"])
        value_primo_pointer = builder.gep(symbol_table["#array_prime"], [i32_0, current_i_value])
        value_primo_prod = builder.load(value_primo_pointer)


        value_prod = builder.mul(value_atual, value_primo_prod, name="mul")
        builder.store(value_prod, symbol_table["value_array"])


        #Fim do for interno



        current_j_value = builder.load(symbol_table["j"])
        new_j_value = builder.add(current_j_value, i32_1, name="add")
        builder.store(new_j_value, symbol_table["j"])

        cond_body_interno = builder.icmp_signed('<', new_j_value, max_j_value, name="lt")
        builder.cbranch(cond_body_interno, for_body_block_interno, for_after_block_interno)

        builder.position_at_start(for_after_block_interno)

        # Inicio da incremento no valor de i, for_externo








        new_i_value = builder.add(current_i_value, i32_1, name="add")
        builder.store(new_i_value, symbol_table["i"])
        cond_body = builder.icmp_signed('<', new_i_value, i32_100, name="lt")
        builder.cbranch(cond_body, for_body_block, for_after_block)

        builder.position_at_start(for_after_block)

        #Load do valor final e atribuição a variavel q chamou ele

        var_recebe = symbols[ast[c.var]] 
        value_stored = builder.load(symbol_table["value_array"])
        builder.store(value_stored, var_recebe)






    elif ast[c.array][c.value] in symbols:


        var_name = symbols[ast[c.array][c.value]]
        


        if '#array' in symbols:

            ptr = symbols['#array']

            int_0 = ir.Constant(i32, 0)
            value = builder.load(var_name)
            

            # index out of range criar

            address = builder.gep(ptr, [int_0, value])
            valor_stored = builder.load(address)
            var_recebe = symbols[ast[c.var]] 
            builder.store(valor_stored, var_recebe)
        else:
            array_example = array_example =[0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            #print(array_example)
            array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
            arr = ir.Constant(array_type, array_example)
            ptr = builder.alloca(array_type) #allocate memory
            builder.store(arr, ptr)

            symbols['#array'] = ptr
            #print(symbols)
            int_0 = ir.Constant(i32, 0)
            value = builder.load(var_name)
            
            
            # index out of range criar

            address = builder.gep(ptr, [int_0, value])
            valor_stored = builder.load(address)
            
            var_recebe = symbols[ast[c.var]]
            
            builder.store(valor_stored, var_recebe)


        
    else:

        value_int = ast[c.array][c.value]
                
        # index out of range criar

        if '#array' in symbols:
            ptr = symbols['#array']

            int_0 = ir.Constant(i32, 0)
            value = ir.Constant(i32, value_int)
            address = builder.gep(ptr, [int_0, value])
            var_name = symbols[ast[c.var]]
            valor_stored = builder.load(address)
            builder.store(valor_stored, var_name)
        else:
            array_example =[0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
            #array_example = [3,5,8]
            array_type = ir.ArrayType(i32, len(array_example)) #According to documentation, the second argument has to be an Python Integer. It can't be ir.Constant(i32, 3) for example.
            arr = ir.Constant(array_type, array_example)
            ptr = builder.alloca(array_type) #allocate memory
            builder.store(arr, ptr)
            symbols['#array'] = ptr
            
            int_0 = ir.Constant(i32, 0)
            value = value = ir.Constant(i32, value_int)
            address = builder.gep(ptr, [int_0, value])
            valor_stored = builder.load(address)
            var_name = symbols[ast[c.var]]

            builder.store(valor_stored, var_name)





#Funções possibilitando uma possivel versao terminal... (fragmento de codigo seguindo tutoriias na net)
def convert_to_string(builder, ir_object):
    if ir_object.type == f32:
        fn = builder.module.globals.get('floatToString')
        return builder.call(fn, [ir_object])
    else:
        fn = builder.module.globals.get('intToString')
        return builder.call(fn, [ir_object])


def print_pointer_number(ir_pointer, builder):
    print_numbers(builder.load(ir_pointer), builder)


def print_numbers(ir_object, builder):
    if ir_object.type.is_pointer:
        return print_pointer_number(ir_object, builder)

    if ir_object.type == f32:
        fn = builder.module.globals.get('printFloat')
    else:
        fn = builder.module.globals.get('printInt')
        if ir_object.type == i1:
            ir_object = builder.zext(ir_object, i32)
    builder.call(fn, [ir_object])


#printf
def printStmt(ast, builder, symbols):

    #adapted from tutorial https://github.com/cea-sec/miasm/blob/master/miasm2/jitter/llvmconvert.py
    #but I know how it works and can explain it

    s = expression(ast["exp"], symbols, builder)
    if not isinstance(s, str):
        return print_numbers(s, builder)
    else:
        if len(s) == 0:
            return None
        b = s.encode('ascii')
        b = bytearray(b)

        s_bytes = ir.Constant(ir.ArrayType(ir.IntType(8), len(b)), b)

        #finds the global variables
        global_fmt = find_global_constant(builder, s, s_bytes)
        ptr_fmt = builder.bitcast(global_fmt, ir.IntType(8).as_pointer())
    fn = builder.module.globals.get('printString')
    builder.call(fn, [ptr_fmt])

# Todas as variavéis são de escopo logal (a menos que use ref...) embora o codigo possa ser adaptado para uso das variaveis com escopo global
# Não existe vantegem nisso, ao contrario somente perca de desempenho 
def find_global_constant(builder,name, value):
    #adapted https://github.com/cea-sec/miasm/blob/master/miasm2/jitter/llvmconvert.py
    if name in builder.module.globals:
        return builder.module.globals[name]
    else:
        glob = ir.GlobalVariable(builder.module, value.type, name = name)
        glob.global_constant = True
        glob.initializer = value
        return glob



#Bloco do while
def whileStmt(ast, builder, symbols):
    w_body_block = builder.append_basic_block("w_body")
    w_after_block = builder.append_basic_block("w_after")

    # head
    cond_head = expression(ast[c.cond], symbols, builder)
    builder.cbranch(cond_head, w_body_block, w_after_block)
    # body
    builder.position_at_start(w_body_block)
    stmt(ast["stmt"], builder, symbols)
    cond_body = expression(ast[c.cond], symbols, builder)
    builder.cbranch(cond_body, w_body_block, w_after_block)
    # after
    builder.position_at_start(w_after_block)



#Bloco do if
def ifStmt(ast, builder, symbols):

    cond = expression(ast["cond"], symbols, builder)
    #print(cond)
    returned = False
    entry = builder.block
    if "else_stmt" in ast:
        with builder.if_else(cond) as (then, otherwise):
            with then:
                returned_then = stmt(ast["stmt"], builder, symbols)
                #print(returned_then)
            with otherwise:
                returned_else = stmt(ast["else_stmt"], builder, symbols)
        returned = returned_then and returned_else

    else:
        with builder.if_then(cond):            
            stmt(ast["stmt"], builder, symbols)
    if returned:
        endif = builder.block
        builder.function.blocks.remove(endif)

   # print(returned)
    return returned



def returnStmt(ast, builder, symbols):
    if "exp" in ast:
        ret_exp = expression(ast["exp"], symbols, builder)
        if ret_exp.type.is_pointer:
            return builder.ret(
                builder.load(ret_exp)
            )
        builder.ret(ret_exp)
    else:
        builder.ret_void()
    return True


#Processa declaração de variavel
def vardeclstmt(ast, builder, symbols):
    var_declaration = ast[c.vdecl]
    var_type = var_declaration[c.typ]
    var_name = var_declaration[c.var]
    
    if 'ref' in var_type:
        return ref_var_decl_stmt(ast, builder, symbols)

    vtype = to_ir_type(var_type)
    ptr = builder.alloca(vtype)
    symbols[var_name] = ptr

    exp = ast[c.exp]
    cint = False
    if "cint" in ast[c.vdecl][c.typ]:
        cint = True
        symbols["cint"].add(var_name)
    value = expression(exp, symbols, builder, cint = cint)
    if value.type.is_pointer:
        value = builder.load(value)

    if vtype != value.type:
        if vtype == f32:
            value = builder.uitofp(value, f32)
        if vtype == i32:
            if value.type == i1:
                value = builder.zext(value, i32)
            value = builder.fptosi(value, i32)

    try:
        builder.store(value, ptr)

    except TypeError as err:
        raise RuntimeError('Erro de alocação do Tipo de variavel:    ' + str(ast), err)


def ref_var_decl_stmt(ast, builder, symbols):
    var_declaration = ast[c.vdecl]
    var_type = var_declaration[c.typ]   
    var_name = var_declaration[c.var]
    exp = ast[c.exp]
    pointee = expression(exp, symbols, builder)
    symbols[var_name] = pointee


def binary_convert(builder, il):
    if il.type.is_pointer:
        il = builder.load(il)
    if il.type == i32:
        il = builder.uitofp(il, f32)
    if il.type == f32:
        il = builder.fptosi(il, i1)

    return il


def extract_value(exp, builder):
    if exp.type.is_pointer:
        return builder.load(exp)
    return exp


def binop(ast, symbols, builder, target_type, cint = False):
    lhs = expression(ast["lhs"], symbols, builder, cint = cint)  
    rhs = expression(ast["rhs"], symbols, builder, cint = cint)  
    lhs = extract_value(lhs, builder)
    rhs = extract_value(rhs, builder)
    exp_type = target_type
    op = ast["op"]



    # Codigo sequindo tutoriais na net 


    flags = list()
    if "float" == target_type:
        flags= ["fast"]

    try:
        
        if "int" in exp_type:
            if op == 'mul':
                return builder.mul(lhs, rhs, name='mul')
                #result = builder.smul_with_overflow(lhs, rhs, name='mul')
                #return builder.extract_value(result, 0)
                

            elif op == 'div':
                return builder.sdiv(lhs, rhs, name='div')
            elif op == 'add':
                return builder.add(lhs, rhs, name="add")
                
            elif op == 'sub':


                # Adapted from tutorial https://gist.github.com/sklam/eb89eab5b5708f03d0b971136a9806f4
                # Andhttps://ian-bertolacci.github.io/llvm/llvmlite/python/compilers/programming/2016/03/06/LLVMLite_fibonacci.html
                

                cond = builder.icmp_signed('<', lhs, rhs)
                #print (cond)
                with builder.if_else(cond) as (then, otherwise):
                    with then:
                        bb_then = builder.basic_block
                        out_then = builder.sub(lhs, lhs, name = 'out_then')
                        
                    with otherwise:
                        bb_otherwise = builder.basic_block
                        out_otherwise = builder.sub(lhs,rhs, name = 'out_otherwise')
                        
                
                endif = builder.block
                out_phi = builder.phi(i32)
                out_phi.add_incoming(out_then, bb_then)
                out_phi.add_incoming(out_otherwise, bb_otherwise)

                return out_phi
                #return builder.sub(lhs, rhs, name = 'sub')
            elif op == 'eq':
                return builder.icmp_signed('==', lhs, rhs, name="eq")
            elif op == 'lt':
                return builder.icmp_signed('<', lhs, rhs, name="lt")
            elif op == 'gt':
                return builder.icmp_signed('>', lhs, rhs, name="gt")
            elif op == 'df':
                return builder.icmp_signed('!=', lhs, rhs, name = "df")
            elif op == 'el':
                return builder.icmp_signed('<=', lhs, rhs, name="el")
            elif op == 'lg':
                return builder.icmp_signed('>=', lhs, rhs, name = "lg")
        
    except ValueError as err:
        raise RuntimeError('Erro ao pocessar a operação:  ' + str(ast) + '  ' + str(err))
    except AttributeError as err: 
        raise RuntimeError('Erro ao processar a operação:  ' + str(ast)+ '  ' + str(err))



def deference(builder, p):
    if p.type.is_pointer:
        return builder.load(p)
    return p


def expression(ast, symbols, builder, cint = False, neg=False, exception=False):
    name = ast[c.name]
    
    try:

        if name == 'lit':
              #18.446.744.073.709.551.616
            limit = 9223372036854775807
                
            #    print(ast['value'])

            if ast['value'] > limit:
                raise RuntimeError('Valor acima do suportado: valor overflow')
                    
            if exception and ast['value'] <= 9223372036854775808:
                raise RuntimeError('Valor acima do suportado: valor overflow')

            r = ir.Constant(to_ir_type(ast['type']), ast['value'])
            return r



        if name == c.litExp:
            if cint:
                #18.446.744.073.709.551.616
                limit = 9223372036854775807
                
                #print(ast['value'])

                if ast['value'] > limit:
                    raise RuntimeError('Valor acima do suportado: valor overflow')
                    
                if exception and ast['value'] <= 9223372036854775808:
                    raise RuntimeError('Valor acima do suportado: valor overflow')

            r = ir.Constant(to_ir_type(ast['type']), ast['value'])
            return r
        
        if name == c.varExp:
            id = ast[c.var]
            try:
                
                return symbols[id]
            except TypeError as err:
                raise RuntimeError('Erro ao fazer parse: ' + str(ast) + '  ' + str(err))
        if name == c.funcCallExp:
            function_name = ast[c.globid]
            fn = builder.module.globals.get(function_name)
            params = ast[c.params]
            parameters = []
            if function_name != "getarg" and function_name != "getargf":
                parameters = prepare_parameters(function_name, symbols, params, builder)
            else:
                parameters = [
                    deference(
                        builder,
                        expression(param, symbols, builder)
                    ) for param in params[c.exps]
                ]

            return builder.call(fn, parameters)
        if name == c.binop:
            target_type = ast[c.typ]
            return binop(ast, symbols, builder, target_type, cint = cint)           
            

        if name == c.assign:
            var_name = ast["var"]

            if var_name not in symbols:
                raise RuntimeError(str(var_name)+'has not been defined')

            ptr = symbols[var_name]
            if var_name in symbols["cint"]:
                ast["type"] = "cint"

            cint = False
            if "cint" in ast["type"]:
                cint = True

            if ast["exp"] is not None:
                value = expression(ast["exp"], symbols, builder, cint = cint)
                store_helper(builder, ptr, value)
                return None
            if ast["array"] is not None:
                return None

        raise RuntimeError('Not processed: ' + str(ast))

    except KeyError as err:
        raise RuntimeError('Error converting: ' + str(ast), err)


def prepare_parameters(function_name, symbols, params, builder):
    parameters = []
    if len(params) > 0:
        fnArgs = symbols[function_name].args
        for index in range(len(params[c.exps])):
            param = params[c.exps][index]
            argType = fnArgs[index]
            if argType.is_pointer:
                if c.var not in param:
                    raise RuntimeError("Non-variable object passed as ref type")
                var_name = param[c.var]
                parameters.append(
                    symbols[var_name]
                )
            else:
                cint = symbols[c.cint_args][function_name][index]
                value = expression(param, symbols, builder, cint=cint)
                parameters.append(
                    deference(
                        builder,
                        value
                    )
                )
    return parameters

def store_helper(builder, ptr, value):
    if value.type.is_pointer:
        value = builder.load(value)

    if ptr.type.pointee == i32:
        if value.type == i1:
            value = builder.uitofp(value, f32)
        if value.type == f32:
            value = builder.fptosi(value, ptr.type.pointee)
    elif ptr.type.pointee == f32:
        if value.type == i1 or value.type == i32:
            value = builder.uitofp(value, f32)

    builder.store(value, ptr)
    return None


def to_ir_type(_type):
    return ir_type(_type)

def overflows(ast, builder):
    overf = {"exp":
                 {"value": "Error: Int value overflowed", "name": "slit"}
             }
    printStmt(overf, builder, None)

    pass

def convert_externs(ast, module, *sysArgs):
    externList = ast["externs"]
    for i in externList:
        externs(i, module, *sysArgs)


def convert_funcs(ast, module, known_funcs):
    funcList = ast['funcs']
    for i in funcList:
        funcs(i, module, known_funcs)


def convert(ast, module, *sysArgs):
    if "externs" in ast:
    
        convert_externs(ast["externs"], module, *sysArgs)
    known_funcs = ast['funcList']

    define_built_ins(module, known_funcs)

    convert_funcs(ast["funcs"], module, known_funcs)

        
    # Code from  https://github.com/cea-sec/miasm/blob/master/miasm2/jitter/llvmconvert.py
    

def define_built_ins(module, known_funcs):
    char_pointer = ir.IntType(8).as_pointer()
    fnty = ir.FunctionType(ir.IntType(64), [char_pointer], var_arg=True)
    printf = ir.Function(module, fnty, name="printf")
    known_funcs["printf"] = "slit"
    fnty = ir.FunctionType(ir.VoidType(), [char_pointer])
    ir.Function(module, fnty, name="printString")
    fnty = ir.FunctionType(ir.VoidType(), [i32])
    ir.Function(module, fnty, name="printInt")
    fnty = ir.FunctionType(ir.VoidType(), [f32])
    ir.Function(module, fnty, name="printFloat")


def mainFunc(ast, *args):
    module = ir.Module(name="prog")
    convert(ast, module, *args)
    #print(module)

    
    return module
