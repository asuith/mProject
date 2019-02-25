Symbol = str
List = list
Number = (int, float)


def parse(char):
    # print(read_from_token(tokenize(char)))
    return read_from_token(tokenize(char))


def tokenize(char):
    return char.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_token(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            # read_from_token return one object
            L.append(read_from_token(tokens))
        tokens.pop(0)  # remove ')'
        return L
    elif token == ')':  # input gone mad
        raise SyntaxError('Invalid input')
    # token by now can be either a number or a symbol
    else:
        return atom(token)


def atom(token):
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


import math
import operator as op


def standard_env():
    """return an standard Scheme environment"""
    env = {}
    env.update(vars(math))  # sin, cos, exp...
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'map': lambda *args: list(map(*args)),
        'apply': lambda proc, args: proc(*args),
        'number?': lambda num: isinstance(num, Number),
        'begin': lambda *x: x[-1],
        'length': len,
        'equal?': op.eq,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, List),
        '#t': True,
        '#f': False,
        ' ': None,
        'positive?': lambda x: x > 0,
        'negative?': lambda x: x <= 0
    })
    return env


global_env = standard_env()

from collections import ChainMap as Environment


class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env


class ProcedureLambda(Procedure):
    def __call__(self, *args):
        env = Environment(dict(zip(self.parms, args)), self.env)
        return eval(self.body, env)


class ProcedureLet(Procedure):  
    def result(self):
        self.parms = {parm: eval(arg, self.env) for (parm, arg) in self.parms}
        env = Environment(dict(self.parms), self.env)
        return eval(self.body, env)


def eval(x, env=global_env):
    if isinstance(x, Symbol):
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'cond':
        (_, *body) = x
        exp = ' '
        for (p, e) in body:
            if p == 'else' or eval(p, env):
                exp = e
                break
        return eval(exp, env)
    elif x[0] == 'define':
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'lambda':
        (_, parms, body) = x
        return ProcedureLambda(parms, body, env)
    elif x[0] == 'let':
        (_, parms, body) = x
        return ProcedureLet(parms, body, env).result()
    else:  # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(evl, env) for evl in x[1:]]
        return proc(*args)


def repl():
    """read eval print loop, repl"""
    while True:
        try:
            code = read()
            if code.strip() == 'exit':
                print("Till next time~")
                break
            val = eval(parse(code))
            if val is not None:
                print(schemestr(val))
        except SyntaxError as e:
            print("[syntax] Something wrong with the syntax of the code:")
            print(e)
            repl()
        except ValueError as e:
            print("[number] Something wrong with the number of the code:")
            print(e)
            repl()
        except:
            print("[unknown] Error unknown, please check")
            repl()


def read():
    code = input("LISP > ")
    while not valid_code(code):
        code += input()
    return code


def valid_code(code):
    count = 0
    for c in code:
        if c == '(':
            count += 1
        elif c == ')':
            if count <= 0:
                raise SyntaxError("Invalid Input")
            count -= 1
    # the '(' and ')' match each other perfectly if count is 0
    return count == 0


def schemestr(exp):
    "Scheme readable form"
    if isinstance(exp, List):
        # list in Python is surrounded by square brackets e.g. [1, 3, 5]
        # rather than parentheses e.g. (1, 3, 5)
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


if __name__ == '__main__':
    repl()
