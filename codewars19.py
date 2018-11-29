class add(int):
    def __call__(self,n):
        return add(self+n)

result = add(1)(2)(3)(4)(5)
print(result)
