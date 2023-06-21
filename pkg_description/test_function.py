a = 10

def test(num):
    num += 1
    a = 30
    return num


print(a)
print(test(5))
print(a)