def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    
    return quick_sort(left) + middle + quick_sort(right)

data_set = [3, 6, 8, 10, 1, 2, 1]



import math

def square(x):
    return x * x

def process():
    values = [1, 2, 3]

    for v in values:
        res = square(v)
        print(res)

    return True

flag = process()


value = 4

def calc(n):
    total = 0
    for i in range(n):
        total = total + i
    return total

result = calc(value)


def sum(a, b):
    result = a + b
    return result

x = 4
y = 6

res = sum(x, y)




import math

def cube(a):
    return a * a * a

def run():
    data = [2, 3, 4]

    for item in data:
        result = cube(item)
        print(result)

    return False

status = run()


count = 3

def compute(k):
    acc = 1
    for j in range(k):
        acc = acc * (j + 1)
    return acc

final = compute(count)


def multiply(a, b):
    output = a * b
    return output

m = 3
n = 5

res = multiply(m, n)

