from z3 import *

A, B, C, X, Y, Z = Bools('A B C X Y Z')
vars = [ A, B, C, X, Y, Z ]

s = Solver()

expr = Or(And(Not(A), B, Not(X), Y, Z),
          And(A, C, Not(X), Y, Z),
          And(A, Not(B), Not(C), Not(X), Z),
          And(A, Not(B), Not(C), X, Not(Y), Not(Z)),
          And(Not(A), Not(B), C, X, Not(Y), Not(Z)),
          And(A, Not(B), Not(C), Not(X), Y),
          And(Not(A), Not(B), C, Not(X), Y, Not(Z)))
s.add(expr)

models = []

def convert_model(model):
    return [
        is_true(model[I])
        if is_true(model[I]) or is_false(model[I])
        else None
        for I in vars
    ]

while s.check() == sat:
    model = s.model()

    models.append(convert_model(model))

    expr = simplify(Or([False if model[I] is None else I != model[I] for I in vars]))

    s.add(expr)

print(models)

def trasnform_to_binary(models):
    binaries = [False for i in range(2**len(vars))]
    
    for model in models:
        cases = [ 0 ]
        for elt in model:
            if elt == True or elt == False:
                cases = [(c << 1) + int(elt) for c in cases]
            else:
                cases = [(c << 1) for c in cases] + [(c << 1) + 1 for c in cases]
        for case in cases:
            binaries[case] = True
    return binaries

def print_karnaugh(binaries):
    placeholer_true, placeholer_false = '#', ' '
    width = 2**(len(vars) // 2)
    height = 2**(len(vars) // 2 + (1 if len(vars) % 2 == 1 else 0))

    for i in range(height):
        for j in range(width):
            print(placeholer_true
                  if binaries[i * width + j]
                  else placeholer_false,
                  end='')
        print()

binaries = trasnform_to_binary(models)

print_karnaugh(binaries)
