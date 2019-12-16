
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightEqualleftEqualityDifferentleftPLUSMinusleftMultiplyDivideArray COMMA DEF Different Divide EXTERN Else Equal Equality GLOBID If LBracket LParen LSquare Minus Multiply PLUS Print RBracket RParen RSquare Return Semicolon While int lit noalias ref voidprog : funcs\n          | externs funcsexterns : extern\n             | extern externsfuncs : func\n           | func funcsextern : EXTERN TYPE GLOBID LParen RParen Semicolonextern : EXTERN TYPE GLOBID LParen tdecls RParen Semicolonfunc : DEF TYPE GLOBID LParen RParen blkfunc : DEF TYPE GLOBID LParen vdecls RParen blkblk : LBracket stmts RBracketblk : LBracket RBracketstmts : stmt\n           | stmt stmtsstmt : blkstmt : Return Semicolon\n          | Return exp Semicolonstmt : vdecl Equal exp Semicolonstmt : exp Semicolonstmt : While LParen exp RParen stmtstmt : If LParen exp RParen stmt\n          | If LParen exp RParen stmt Else stmtstmt : Print exp Semicolonstmt : Array LSquare lit RSquare PLUS lit Semicolon\n          | Array LSquare GLOBID RSquare  PLUS lit Semicolon\n          | Array LSquare lit RSquare Minus lit Semicolon\n          | Array LSquare GLOBID RSquare Minus lit Semicolon stmt : GLOBID Equal Vector Semicolon Vector : Array LSquare  RSquare\n            | Array LSquare lit RSquare\n            | Array LSquare GLOBID RSquare exps : exp\n           | exp COMMA expsexp : LParen exp RParenexp : litexp : binopexp : GLOBIDexp : GLOBID expWrapperexpWrapper : LParen RParen\n                | LParen exps RParenbinop : exp Multiply exp\n           | exp PLUS exp\n           | exp Divide exp\n           | exp Minus exp\n           | GLOBID Equal exp\n           | exp Equality exp\n           | exp Different expvdecls : vdecl COMMA vdecls\n            | vdeclvdecl : TYPE GLOBIDtdecls : TYPE\n            | TYPE COMMA tdeclsTYPE : int\n          | voidTYPE : ref TYPETYPE : noalias ref TYPE'
    
_lr_action_items = {'DEF':([0,3,4,5,10,32,37,40,54,57,58,],[6,6,6,-3,-4,-9,-7,-12,-10,-8,-11,]),'EXTERN':([0,5,37,57,],[7,7,-7,-8,]),'$end':([1,2,4,8,9,32,40,54,58,],[0,-1,-5,-2,-6,-9,-12,-10,-11,]),'int':([6,7,14,19,21,23,33,35,36,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[12,12,12,12,12,12,12,12,12,-12,12,-15,-11,-16,-19,-17,-23,-18,12,12,-28,-20,-21,12,-22,-24,-26,-25,-27,]),'void':([6,7,14,19,21,23,33,35,36,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[13,13,13,13,13,13,13,13,13,-12,13,-15,-11,-16,-19,-17,-23,-18,13,13,-28,-20,-21,13,-22,-24,-26,-25,-27,]),'ref':([6,7,14,15,19,21,23,33,35,36,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[14,14,14,19,14,14,14,14,14,14,-12,14,-15,-11,-16,-19,-17,-23,-18,14,14,-28,-20,-21,14,-22,-24,-26,-25,-27,]),'noalias':([6,7,14,19,21,23,33,35,36,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[15,15,15,15,15,15,15,15,15,-12,15,-15,-11,-16,-19,-17,-23,-18,15,15,-28,-20,-21,15,-22,-24,-26,-25,-27,]),'GLOBID':([11,12,13,16,18,22,24,33,40,41,42,43,47,49,58,60,63,64,65,66,67,68,69,70,71,73,75,76,78,79,80,91,100,101,102,105,106,108,109,110,119,126,127,128,129,130,],[17,-53,-54,20,-55,-56,31,52,-12,52,-15,62,62,62,-11,-16,-19,62,62,62,62,62,62,62,62,62,93,62,62,-17,62,-23,-18,52,52,-28,117,62,-20,-21,52,-22,-24,-26,-25,-27,]),'COMMA':([12,13,18,22,27,28,31,51,53,62,77,81,82,83,84,85,86,89,95,97,99,107,],[-53,-54,-55,-56,35,36,-50,-35,-36,-37,-38,-41,-42,-43,-44,-46,-47,-34,-45,-39,108,-40,]),'RParen':([12,13,18,21,22,23,26,27,28,30,31,51,53,55,56,62,72,77,78,81,82,83,84,85,86,88,89,90,95,97,98,99,107,118,],[-53,-54,-55,25,-56,29,34,-49,-51,38,-50,-35,-36,-48,-52,-37,89,-38,97,-41,-42,-43,-44,-46,-47,101,-34,102,-45,-39,107,-32,-40,-33,]),'LParen':([17,20,33,40,41,42,43,46,47,48,49,52,58,60,62,63,64,65,66,67,68,69,70,71,73,76,78,79,80,91,100,101,102,105,108,109,110,119,126,127,128,129,130,],[21,23,47,-12,47,-15,47,71,47,73,47,78,-11,-16,78,-19,47,47,47,47,47,47,47,47,47,47,47,-17,47,-23,-18,47,47,-28,47,-20,-21,47,-22,-24,-26,-25,-27,]),'LBracket':([25,33,34,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[33,33,33,-12,33,-15,-11,-16,-19,-17,-23,-18,33,33,-28,-20,-21,33,-22,-24,-26,-25,-27,]),'Semicolon':([29,38,43,44,51,52,53,61,62,74,77,81,82,83,84,85,86,87,89,94,95,97,107,115,120,121,122,123,124,125,],[37,57,60,63,-35,-37,-36,79,-37,91,-38,-41,-42,-43,-44,-46,-47,100,-34,105,-45,-39,-40,-29,127,128,129,130,-30,-31,]),'Equal':([31,45,52,62,],[-50,70,76,80,]),'RBracket':([33,39,40,41,42,58,59,60,63,79,91,100,105,109,110,126,127,128,129,130,],[40,58,-12,-13,-15,-11,-14,-16,-19,-17,-23,-18,-28,-20,-21,-22,-24,-26,-25,-27,]),'Return':([33,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[43,-12,43,-15,-11,-16,-19,-17,-23,-18,43,43,-28,-20,-21,43,-22,-24,-26,-25,-27,]),'While':([33,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[46,-12,46,-15,-11,-16,-19,-17,-23,-18,46,46,-28,-20,-21,46,-22,-24,-26,-25,-27,]),'If':([33,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[48,-12,48,-15,-11,-16,-19,-17,-23,-18,48,48,-28,-20,-21,48,-22,-24,-26,-25,-27,]),'Print':([33,40,41,42,58,60,63,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[49,-12,49,-15,-11,-16,-19,-17,-23,-18,49,49,-28,-20,-21,49,-22,-24,-26,-25,-27,]),'Array':([33,40,41,42,58,60,63,76,79,91,100,101,102,105,109,110,119,126,127,128,129,130,],[50,-12,50,-15,-11,-16,-19,96,-17,-23,-18,50,50,-28,-20,-21,50,-22,-24,-26,-25,-27,]),'lit':([33,40,41,42,43,47,49,58,60,63,64,65,66,67,68,69,70,71,73,75,76,78,79,80,91,100,101,102,105,106,108,109,110,111,112,113,114,119,126,127,128,129,130,],[51,-12,51,-15,51,51,51,-11,-16,-19,51,51,51,51,51,51,51,51,51,92,51,51,-17,51,-23,-18,51,51,-28,116,51,-20,-21,120,121,122,123,51,-22,-24,-26,-25,-27,]),'Else':([40,42,58,60,63,79,91,100,105,109,110,126,127,128,129,130,],[-12,-15,-11,-16,-19,-17,-23,-18,-28,-20,119,-22,-24,-26,-25,-27,]),'Multiply':([44,51,52,53,61,62,72,74,77,81,82,83,84,85,86,87,88,89,90,95,97,99,107,],[64,-35,-37,-36,64,-37,64,64,-38,-41,64,-43,64,64,64,64,64,-34,64,64,-39,64,-40,]),'PLUS':([44,51,52,53,61,62,72,74,77,81,82,83,84,85,86,87,88,89,90,95,97,99,103,104,107,],[65,-35,-37,-36,65,-37,65,65,-38,-41,-42,-43,-44,65,65,65,65,-34,65,65,-39,65,111,113,-40,]),'Divide':([44,51,52,53,61,62,72,74,77,81,82,83,84,85,86,87,88,89,90,95,97,99,107,],[66,-35,-37,-36,66,-37,66,66,-38,-41,66,-43,66,66,66,66,66,-34,66,66,-39,66,-40,]),'Minus':([44,51,52,53,61,62,72,74,77,81,82,83,84,85,86,87,88,89,90,95,97,99,103,104,107,],[67,-35,-37,-36,67,-37,67,67,-38,-41,-42,-43,-44,67,67,67,67,-34,67,67,-39,67,112,114,-40,]),'Equality':([44,51,52,53,61,62,72,74,77,81,82,83,84,85,86,87,88,89,90,95,97,99,107,],[68,-35,-37,-36,68,-37,68,68,-38,-41,-42,-43,-44,-46,-47,68,68,-34,68,68,-39,68,-40,]),'Different':([44,51,52,53,61,62,72,74,77,81,82,83,84,85,86,87,88,89,90,95,97,99,107,],[69,-35,-37,-36,69,-37,69,69,-38,-41,-42,-43,-44,-46,-47,69,69,-34,69,69,-39,69,-40,]),'LSquare':([50,96,],[75,106,]),'RSquare':([92,93,106,116,117,],[103,104,115,124,125,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'prog':([0,],[1,]),'funcs':([0,3,4,],[2,8,9,]),'externs':([0,5,],[3,10,]),'func':([0,3,4,],[4,4,4,]),'extern':([0,5,],[5,5,]),'TYPE':([6,7,14,19,21,23,33,35,36,41,101,102,119,],[11,16,18,22,24,28,24,24,28,24,24,24,24,]),'vdecls':([21,35,],[26,55,]),'vdecl':([21,33,35,41,101,102,119,],[27,45,27,45,45,45,45,]),'tdecls':([23,36,],[30,56,]),'blk':([25,33,34,41,101,102,119,],[32,42,54,42,42,42,42,]),'stmts':([33,41,],[39,59,]),'stmt':([33,41,101,102,119,],[41,41,109,110,126,]),'exp':([33,41,43,47,49,64,65,66,67,68,69,70,71,73,76,78,80,101,102,108,119,],[44,44,61,72,74,81,82,83,84,85,86,87,88,90,95,99,95,44,44,99,44,]),'binop':([33,41,43,47,49,64,65,66,67,68,69,70,71,73,76,78,80,101,102,108,119,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'expWrapper':([52,62,],[77,77,]),'Vector':([76,],[94,]),'exps':([78,108,],[98,118,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> prog","S'",1,None,None,None),
  ('prog -> funcs','prog',1,'p_prog','lexerAndParser.py',170),
  ('prog -> externs funcs','prog',2,'p_prog','lexerAndParser.py',171),
  ('externs -> extern','externs',1,'p_externs','lexerAndParser.py',178),
  ('externs -> extern externs','externs',2,'p_externs','lexerAndParser.py',179),
  ('funcs -> func','funcs',1,'p_funcs','lexerAndParser.py',187),
  ('funcs -> func funcs','funcs',2,'p_funcs','lexerAndParser.py',188),
  ('extern -> EXTERN TYPE GLOBID LParen RParen Semicolon','extern',6,'p_extern','lexerAndParser.py',197),
  ('extern -> EXTERN TYPE GLOBID LParen tdecls RParen Semicolon','extern',7,'p_externWithTypes','lexerAndParser.py',201),
  ('func -> DEF TYPE GLOBID LParen RParen blk','func',6,'p_func','lexerAndParser.py',206),
  ('func -> DEF TYPE GLOBID LParen vdecls RParen blk','func',7,'p_funcWithParams','lexerAndParser.py',210),
  ('blk -> LBracket stmts RBracket','blk',3,'p_blk','lexerAndParser.py',215),
  ('blk -> LBracket RBracket','blk',2,'p_blkEmpty','lexerAndParser.py',219),
  ('stmts -> stmt','stmts',1,'p_statements','lexerAndParser.py',224),
  ('stmts -> stmt stmts','stmts',2,'p_statements','lexerAndParser.py',225),
  ('stmt -> blk','stmt',1,'p_blkStmt','lexerAndParser.py',234),
  ('stmt -> Return Semicolon','stmt',2,'p_return','lexerAndParser.py',238),
  ('stmt -> Return exp Semicolon','stmt',3,'p_return','lexerAndParser.py',239),
  ('stmt -> vdecl Equal exp Semicolon','stmt',4,'p_vdeclStmt','lexerAndParser.py',247),
  ('stmt -> exp Semicolon','stmt',2,'p_expSemi','lexerAndParser.py',259),
  ('stmt -> While LParen exp RParen stmt','stmt',5,'p_while','lexerAndParser.py',263),
  ('stmt -> If LParen exp RParen stmt','stmt',5,'p_if','lexerAndParser.py',267),
  ('stmt -> If LParen exp RParen stmt Else stmt','stmt',7,'p_if','lexerAndParser.py',268),
  ('stmt -> Print exp Semicolon','stmt',3,'p_print','lexerAndParser.py',275),
  ('stmt -> Array LSquare lit RSquare PLUS lit Semicolon','stmt',7,'p_arrayOperator','lexerAndParser.py',279),
  ('stmt -> Array LSquare GLOBID RSquare PLUS lit Semicolon','stmt',7,'p_arrayOperator','lexerAndParser.py',280),
  ('stmt -> Array LSquare lit RSquare Minus lit Semicolon','stmt',7,'p_arrayOperator','lexerAndParser.py',281),
  ('stmt -> Array LSquare GLOBID RSquare Minus lit Semicolon','stmt',7,'p_arrayOperator','lexerAndParser.py',282),
  ('stmt -> GLOBID Equal Vector Semicolon','stmt',4,'p_arrayGLOBID','lexerAndParser.py',287),
  ('Vector -> Array LSquare RSquare','Vector',3,'p_vector','lexerAndParser.py',292),
  ('Vector -> Array LSquare lit RSquare','Vector',4,'p_vector','lexerAndParser.py',293),
  ('Vector -> Array LSquare GLOBID RSquare','Vector',4,'p_vector','lexerAndParser.py',294),
  ('exps -> exp','exps',1,'p_exps','lexerAndParser.py',304),
  ('exps -> exp COMMA exps','exps',3,'p_exps','lexerAndParser.py',305),
  ('exp -> LParen exp RParen','exp',3,'p_expParen','lexerAndParser.py',321),
  ('exp -> lit','exp',1,'p_exp','lexerAndParser.py',325),
  ('exp -> binop','exp',1,'p_expBinOpUop','lexerAndParser.py',336),
  ('exp -> GLOBID','exp',1,'p_var','lexerAndParser.py',340),
  ('exp -> GLOBID expWrapper','exp',2,'p_expGlobid','lexerAndParser.py',344),
  ('expWrapper -> LParen RParen','expWrapper',2,'p_expWrapper','lexerAndParser.py',348),
  ('expWrapper -> LParen exps RParen','expWrapper',3,'p_expWrapper','lexerAndParser.py',349),
  ('binop -> exp Multiply exp','binop',3,'p_binop','lexerAndParser.py',357),
  ('binop -> exp PLUS exp','binop',3,'p_binop','lexerAndParser.py',358),
  ('binop -> exp Divide exp','binop',3,'p_binop','lexerAndParser.py',359),
  ('binop -> exp Minus exp','binop',3,'p_binop','lexerAndParser.py',360),
  ('binop -> GLOBID Equal exp','binop',3,'p_binop','lexerAndParser.py',361),
  ('binop -> exp Equality exp','binop',3,'p_binop','lexerAndParser.py',362),
  ('binop -> exp Different exp','binop',3,'p_binop','lexerAndParser.py',363),
  ('vdecls -> vdecl COMMA vdecls','vdecls',3,'p_vdecls','lexerAndParser.py',402),
  ('vdecls -> vdecl','vdecls',1,'p_vdecls','lexerAndParser.py',403),
  ('vdecl -> TYPE GLOBID','vdecl',2,'p_vdeclare','lexerAndParser.py',411),
  ('tdecls -> TYPE','tdecls',1,'p_tdecls','lexerAndParser.py',416),
  ('tdecls -> TYPE COMMA tdecls','tdecls',3,'p_tdecls','lexerAndParser.py',417),
  ('TYPE -> int','TYPE',1,'p_type','lexerAndParser.py',425),
  ('TYPE -> void','TYPE',1,'p_type','lexerAndParser.py',426),
  ('TYPE -> ref TYPE','TYPE',2,'p_refType','lexerAndParser.py',430),
  ('TYPE -> noalias ref TYPE','TYPE',3,'p_refTypeNoAlias','lexerAndParser.py',435),
]
