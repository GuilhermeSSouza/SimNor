from yaml import dump
import copy


def semanticsCheck(ast):
    errors = []
    k_functions = {}

    vdecl_void(ast, errors)
    ref_void(ast, errors)
    func_order(ast, errors, k_functions)
    ref_initalization(ast, errors)
    func_ref_type(ast, errors)

    a = types(ast, k_functions, errors)
    return errors


def vdecl_void(ast, errors):
    vdeclType = list(find('vdecl', ast))
    for i in vdeclType:
        if i['type'] == 'void':
            errors.append('Erro: In ​ <vdecl>​ , the type may not be void.')


def ref_void(ast, errors):
    types = list(find('types', ast))
    types.append(list(find('ret_type', ast)))
    types.append(list(find('type', ast)))
    flat_list = [item for sublist in types for item in sublist]
    for t in flat_list:
        if 'ref' in t and 'void' in t:
            errors.append("Erro: In <ref type> the type may not be void or itself a reference type.")


def func_order(ast, errors, k_functions):
    f = ast['funcs']['funcs']
    if 'externs' in ast:
        if 'externs' in ast['externs']:
            externs = ast['externs']['externs']
            for extern in externs:
                k_functions[extern['globid']] = extern['ret_type']

    count_main = 0  # counts all the main functions

    for i in f:

        # checks to make sure run function doesn't have arguments
        if i['globid'] == "main":
            count_main = count_main + 1
            if "vdecls" in i:
                errors.append("Erro: A função 'main' não deve conter arqumentos!")

        # appends functions to a list in the order that they are found
        k_functions[i['globid']] = i['ret_type']

        # goes through the function bulk in order, to see what functions are called.
        glob = list(find('globid', i))
        for functionCall in glob:
            if functionCall not in k_functions:
                # print('function order is bad')
                errors.append("Erro: Todas as funções deve ser declaradas e/ou definidas antes de serem usadas!")

    # ensures that there is a run function, and that it must be 'def int run'

    for i in k_functions:
        if i == "main":
            if k_functions[i] != "int":
                errors.append("Erro: A função  'main' sempre deve retornar um 'int' ")

    # counts the number of run functions
    if count_main!= 1:
        
        errors.append("Erro: Os programas codificados nesse simulador requerem ao menos uma função  'main' para ser executado!")

    ast['funcList'] = k_functions


def ref_initalization(ast, errors):
    stmts = list(find('stmts', ast))
    flat_list = [item for sublist in stmts for item in sublist]
    for stmt in flat_list:
        if not stmt['name'] == 'vardeclstmt':
            continue
        if not 'ref' in stmt['vdecl']['type']:
            continue
        if stmt['exp']['name'] == 'lit':
            errors.append("Erro: Ao inicializar uma variavel de ref dentro de um bloco, \n"+ "essa variavel deve ser um tipo de ref. passado com argumento da função, cujo " + "bloco é interno.")


def func_ref_type(ast, errors):
    funcs = ast['funcs']['funcs']
    for func in funcs:
        if not 'ref' in func['ret_type']:
            continue
        errors.append("Erro: As funções não retornam variveis que sejam tipos de referência 'ref ...' ")


def find(key, dictionary):
    if not isinstance(dictionary, dict):
        return None
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


def types(ast, k_functions, errors):
    f = ast['funcs']['funcs']

    for i in ast['funcs']['funcs']:
        # adds all the function arguments and their types to the variable list
        knownVariables = {}
        if 'vdecls' in i:
            for j in i['vdecls']['vars']:
                knownVariables[j['var']] = j['type']
                if 'ref' in j['type'] and 'noalias' in j['type']:
                    knownVariables[j['var']] = j['type'][12:]
                elif 'ref' in j['type']:
                    knownVariables[j['var']] = j['type'][4:]

        i['blk']['knownVariables'] = knownVariables
        blkRecurs(i['blk'], k_functions, errors)

    return ast


def stmtRecurs(stmt, k_functions, knownVariables, errors):
    if 'vdecl' in stmt:
        vdecl = stmt['vdecl']
        knownVariables[vdecl['var']] = vdecl['type']
    if stmt['name'] in ['blk', 'while']:
        stmt['knownVariables'] = copy.deepcopy(knownVariables)
        blkRecurs(stmt, k_functions, errors)
    elif stmt['name'] in ['if']:
        stmt['stmt']['knownVariables'] = copy.deepcopy(knownVariables)
        stmtRecurs(stmt['stmt'], k_functions, knownVariables, errors)
        if 'else_stmt' in stmt:
            stmt['else_stmt']['knownVariables'] = copy.deepcopy(knownVariables)
            stmtRecurs(stmt['else_stmt'], k_functions, knownVariables, errors)

    if 'cond' in stmt:
        recurs2(stmt['cond'], knownVariables, k_functions, errors)
        return None
    if 'exp' not in stmt:  # print slit;
        return None

    
    recurs2(stmt['exp'], knownVariables, k_functions, errors)


def blkRecurs(blk, k_functions, errors):
    knownVariables = blk['knownVariables']
    statements = list(find('stmts', blk))
    flat_list = [item for sublist in statements for item in sublist]
    for stmt in flat_list:
        stmtRecurs(stmt, k_functions, knownVariables, errors)


# function arguments can be void and what not, or strings
def recurs2(exp, knownVars, k_functions, errors):
    if 'type' in exp:
        return exp['type']

    if isinstance(exp, list):
        
        raise RuntimeError('Não foi possivel fazer parse de codigo. Verificar o código fonte!')
        for i in exp:
            recurs2(exp, knownVars, k_functions, errors)


    if 'assign' == exp['name']:

        t = recurs2(exp['exp'], knownVars, k_functions, errors)
        exp['type'] = t
        knownVars[exp['var']] = t
        return t

    if 'var' in exp:
        if exp['var'] in knownVars:
            exp['type'] = knownVars[exp['var']]
            return exp['type']
        else:
            errors.append('Variavel:    ' + exp['var'] + '   não foi definida!!')

    # if it's a function, exp = fib(). Get the return type from k_functions.
    if exp['name'] == 'funccall':
        functionName = exp['globid']
        if functionName not in k_functions:
            raise RuntimeError('Desconhecida a função:  ' + functionName)
        exp['type'] = k_functions[functionName]
        if 'exps' not in exp['params']:
            return exp['type']
        for paramExp in exp['params']['exps']:
            recurs2(paramExp, knownVars, k_functions, errors)
        return exp['type']


    if exp["name"] == "binop":
        if 'type' not in exp['lhs']:
            left = recurs2(exp['lhs'], knownVars, k_functions, errors)
        if 'type' not in exp['rhs']:
            right = recurs2(exp['rhs'], knownVars, k_functions, errors)
        exp['type'] = calculateType(exp['lhs'], exp['rhs'])
        # logical binary operators return boolean values, which in our languages are ints
        bo = exp['op']
        if bo == 'eq' or bo == 'lt' or bo == 'gt' or bo == 'el' or bo == 'eg' or bo == 'df': # or bo == 'logAnd' or bo == 'logOr':
            exp['type'] = 'int'

        return exp['type']

       
def calculateType(lhs, rhs):
    if  lhs['type'] == 'int' or rhs['type'] == 'int':
        lhs['type'] = 'int'
        rhs['type'] = 'int'
        return 'int'
   
    return "undefined"
