import unittest




#Import for code scripts
import lexerAndParser
import analyzer
import main
import IR
import llvm_binder
import sys





class TestAplication(unittest.TestCase):

#Basic functions test

	def function_parse(self, code):
		return lexerAndParser.toAst(code)

	def function_base(self, code):
		return 'def int main(){%s}' %code

	def run_code(self, program):
		code = self.function_base(program)

		return main.executa(code)



#Tests code operation
	def test_parser_1(self):
		self.assertEqual(self.run_code('int R_a = 8; return R_a;'), 8, "Should be 8")

	def test_parser_2(self):
		self.assertEqual(self.run_code('int R_a = 8; return R_a-4;'), 4, "Should be 4")

	def test_parser_3(self):
		self.assertEqual(self.run_code('int R_a = 8; R_a = R_a +100; return R_a;'), 108, "Should be 108")


#Test parser 


	def test_parser_4(self):
		code = self.function_base('int R_a = 8; return R_a;')
		print(code)
		a, b = self.function_parse(code) 
		print(a)

	def test_parser_5(self):
		code = self.function_base(' return 2+3;')

		self.assertEqual(self.function_parse(code), self.function_wrap_node(binop(operator="+", left=Int32(value=2), right=Int32(value=3))))






#Test IR code


#Test analyzer


#Test feedbacks

if __name__ == '__main__':
	unittest.main()