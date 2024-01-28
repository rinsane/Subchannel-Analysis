from tester2 import vars

class checker(vars):

    def do(self):
        print(self.one, self.two)

apple = checker()

print(apple.two, apple.one)
apple.two = 55
print(apple.two, apple.one)

a = [1,2,3]

b = a
print(a,b)
b[2] = 111
print(a,b)
