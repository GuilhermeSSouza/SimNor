from yaml import dump
import argparse
import mmap
import sys
import lexerAndParser
import lexerAndParserL
import analyzer
import IR
import llvm_binder

def readFile(fileName):
  f = open(fileName,"r")
  mMap = mmap.mmap(f.fileno(),0, prot = mmap.PROT_READ)
  stringFile =str(mMap[:])
  stringFile = stringFile[2:-1]
  data = mMap[:].decode('utf-8')
  return data

def emitAst(fileName, output):
  yaml = dump(output, default_flow_style=False)
  file = open(fileName, 'w')
  file.write(yaml)
  file.close()


def emit_ir(fileName, module):
  file = open(fileName, 'w')
  file.write(
      str(module)
  )
  file.close()




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


def executa(code, wholexer):
  
  #print(wholexer)
  ast = None
  erro = None
 
  if wholexer == 2:
    ast, erro = lexerAndParserL.toAst(code)
  if wholexer == 1:
    ast, erro = lexerAndParser.toAst(code)

  
  if ast is None:
    return 'Erro ao criar arquivo de parser, verifique o código fonte \n' + str(erro[-1])

  #print(ast)

  errors = analyzer.semanticsCheck(ast)
  #print(errors)

  if not errors:  
    module = IR.mainFunc(ast, '*')
    #Mostrar codigo em IR
    #print(module)
    module = llvm_binder.bind(module, '*', optimize = True)
    return module[1]
  else:    
    return '\n'+ str(errors[-1])
    



def executaVerificar(code, wholexer):
  
  #print(wholexer)
  ast = None
  erro = None

  if wholexer == 2:
    ast, erro = lexerAndParserL.toAst(code)
  if wholexer == 1:
    ast, erro = lexerAndParser.toAst(code)

  if ast is None:
    return 'AST parsing failure \n' + str(erro[-1]) 

  
  #print(ast)

  errors = analyzer.semanticsCheck(ast)
  #print(errors)

  if errors: 
    return '\n'+ str(errors[-1])
  else:
    return '\n' + 'Nenhum erro de sintaxe encontrado! Runtime e Exception não são verificados.'  
    

def execultaDebug(code, wholexer):
  
  if wholexer == 2:
    lexerAndParserL.toAstDebug(code)
  if wholexer == 1:
    lexerAndParser.toAstDebug(code)

  