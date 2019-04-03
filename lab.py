def foo(a,b,*c):
    for x in c:
        print(x,end = ' ')
    print('\n')

def make_lambda(a):
    return lambda x : x + a


#foo(1,2,"fuck","shit","114514",1919810)
print(make_lambda(1)(3))