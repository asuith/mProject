import unittest
from lisp import *

class TestLisp(unittest.TestCase):

	def test_tokenize(self):
		self.assertEqual(tokenize('(123)'), ['(', '123', ')'])
		self.assertEqual(tokenize('(* 2 3)'), ['(', '*', '2', '3', ')'])
		self.assertEqual(tokenize('(12(3))'), ['(', '12', '(', '3', ')', ')'])
		self.assertEqual(tokenize('(define( true ) 1 23)'), ['(', 'define', '(', 'true', ')', '1', '23', ')'])

	def test_nothing(self):
		pass

	def test_read_from_token(self):
		self.assertEqual(read_from_token(['(', 'define', 'x', '1', ')']), ['define', 'x', 1])

	def test_parse(self):
		func = "(begin (define r 10) (* pi (* r r)))"
		self.assertEqual(parse(func), ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]])

	def test_circle_area(self):
		func = "(define circle-area (lambda (r) (* pi (* r r))))"
		eval(parse(func))

		circle_area = "(circle-area 10)"
		test = eval(parse(circle_area))

		actual = 314.159265359

		self.assertAlmostEqual(test, actual, delta=10e-8)

	def test_fact(self):
		func = "(define fact (lambda (n) (if (= n 1) 1 (* n (fact (- n 1))))))"
		eval(parse(func))
		circle_area = "(fact 3)"

		expected = eval(parse(circle_area))
		actual = 6

		self.assertEqual(expected, actual)

		circle_area = "(fact 10)"

		expected = eval(parse(circle_area))
		actual = 3628800

		self.assertEqual(expected, actual)

		circle_area = "(fact 100)"

		expected = eval(parse(circle_area))
		actual = 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000

		self.assertEqual(expected, actual)

	def test_count(self):
		func0 = "(define first car)"
		func1 =	"(define rest cdr)"
		func2 = "(define count (lambda (item L) " \
				  		"(if L " \
				  			"(+ (equal? item (first L)) (count item (rest L))) " \
				  			"0)))"

		eval(parse(func0))
		eval(parse(func1))
		eval(parse(func2))

		count1 = eval(parse('(count 0 (list 0 1 2 3 0 0))'))
		self.assertEqual(count1, 3)

		count2 = eval(parse('(count (quote the) (quote (the more the merrier the bigger the better)))'))
		self.assertEqual(count2, 4)

	def test_cond(self):
		func = "(cond ((positive? -1) (don't go there))" \
			 			"((negative? 10) (don't go here))" \
			 			"(else 1))"
		expected = eval(parse(func))
		actual = 1

		self.assertEqual(expected, actual)

	def test_let(self):
		func1 = "(let ((a (list 1 2 3))" \
				  "	   (b (list 4 5 6)))" \
				  "	   (cons a b))"
		func2 = "((lambda (list-a list-b) (cons list-a list-b)) (list 1 2 3) (list 4 5 6))"

		expected = eval(parse(func1))
		actual = eval(parse(func2))

		self.assertEqual(expected, actual)

if __name__ == '__main__':
	unittest.main()
