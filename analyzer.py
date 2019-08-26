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

    a = types(ast, k_functions)
    return errors


def vdecl_void(ast, errorList):
    vdeclType = list(find('vdecl', ast))
    for i in vdeclType:
        if i['type'] == 'void':
            errorList.append('Erro: In ​ <vdecl>​ , the type may not be void.')


def ref_void(ast, errors):
    types = list(find('types', ast))
    types.append(list(find('ret_type', ast)))
    types.append(list(find('type', ast)))
    flat_list = [item for sublist in types for item in sublist]
    for t in flat_list:
        if 'ref' in t and 'void' in t:
            errors.append("Erro: In <ref type> the type may not be void or itself a reference type.")


def func_order(ast, errorList, k_functions):
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
            count_run = count_main + 1
            if "vdecls" in i:
                errorList.append("Erro: The 'main' function cannot have arguments.")

        # appends functions to a list in the order that they are found
        k_functions[i['globid']] = i['ret_type']

        # goes through the function bulk in order, to see what functions are called.
        glob = list(find('globid', i))
        for functionCall in glob:
            if functionCall not in k_functions:
                # print('function order is bad')
                errorList.append("Erro: All functions must be declared and/or defined before they are used")

    # ensures that there is a run function, and that it must be 'def int run'

    for i in k_functions:
        if i == "main":
            if k_functions[i] != "int":
                errorList.append("Erro: The 'main' function must return an int")

    # counts the number of run functions
    if count_run != 1:
        errorList.append("Erro: All programs must define exactly one function named 'main'")

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
            errors.append("Erro: The initialization expression for a reference variable (including "
                          + "function arguments) must be a variable.")


def func_ref_type(ast, errors):
    funcs = ast['funcs']['funcs']
    for func in funcs:
        if not 'ref' in func['ret_type']:
            continue
        errors.append("Erro: A function may not return a ref type.")


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


def types(ast, k_functions):
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
        blkRecurs(i['blk'], k_functions)

    return ast


def stmtRecurs(stmt, k_functions, knownVariables):
    if 'vdecl' in stmt:
        vdecl = stmt['vdecl']
        knownVariables[vdecl['var']] = vdecl['type']
    if stmt['name'] in ['blk', 'while']:
        stmt['knownVariables'] = copy.deepcopy(knownVariables)
        blkRecurs(stmt, k_functions)
    elif stmt['name'] in ['if']:
        stmt['stmt']['knownVariables'] = copy.deepcopy(knownVariables)
        stmtRecurs(stmt['stmt'], k_functions, knownVariables)
        if 'else_stmt' in stmt:
            stmt['else_stmt']['knownVariables'] = copy.deepcopy(knownVariables)
            stmtRecurs(stmt['else_stmt'], k_functions, knownVariables)

    if 'cond' in stmt:
        recurs2(stmt['cond'], knownVariables, k_functions)
        return None
    if 'exp' not in stmt:  # print slit;
        return None
    recurs2(stmt['exp'], knownVariables, k_functions)


def blkRecurs(blk, k_functions):
    knownVariables = blk['knownVariables']
    statements = list(find('stmts', blk))
    flat_list = [item for sublist in statements for item in sublist]
    for stmt in flat_list:
        stmtRecurs(stmt, k_functions, knownVariables)


# function arguments can be void and what not, or strings
def recurs2(exp, knownVars, k_functions):
    if 'type' in exp:
        return exp['type']

    if isinstance(exp, list):
        # suspecting this is probably never reached
        raise RuntimeError('Look if the code makes sense')
        for i in exp:
            recurs2(exp, knownVars, k_functions)

    #if exp['name'] == 'slit':
     #   exp['type'] = 'slit'
      #  return 'slit'

    if 'assign' == exp['name']:
        t = recurs2(exp['exp'], knownVars, k_functions)
        exp['type'] = t
        knownVars[exp['var']] = t
        return t

    if 'var' in exp:
        exp['type'] = knownVars[exp['var']]
        return exp['type']

    # if it's a function, exp = fib(). Get the return type from k_functions.
    if exp['name'] == 'funccall':
        functionName = exp['globid']
        if functionName not in k_functions:
            raise RuntimeError('function name unknown: ' + functionName)
        exp['type'] = k_functions[functionName]
        if 'exps' not in exp['params']:
            return exp['type']
        for paramExp in exp['params']['exps']:
            recurs2(paramExp, knownVars, k_functions)
        return exp['type']

    # this should take care of logical negations
    #if exp['name'] == 'uop':
    #   exp['type'] = recurs2(exp['exp'], knownVars, k_functions)
    #   return exp['type']

    if exp["name"] == "binop":
        if 'type' not in exp['lhs']:
            left = recurs2(exp['lhs'], knownVars, k_functions)
        if 'type' not in exp['rhs']:
            right = recurs2(exp['rhs'], knownVars, k_functions)
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
    # elif lhs['type'] == 'sfloat' or rhs['type'] == 'sfloat':
    #     lhs['type'] = 'sfloat'
    #     rhs['type'] = 'sfloat'
    #     return 'sfloat'
    # elif lhs['type'] == 'float' or rhs['type'] == 'float':
    #     lhs['type'] = 'float'
    #     rhs['type'] = 'float'
    #     return 'float'
    # elif lhs['type'] == 'cint' or rhs['type'] == 'cint':
    #     lhs['type'] = 'cint'
    #     rhs['type'] = 'cint'
    #     return 'cint'
    return "undefined"
