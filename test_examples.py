from functools import reduce

print('=== Examples from Requirements ===')

print('1. Square of even numbers from 1 to 10:')
result1 = [i*i for i in range(1, 11) if i % 2 == 0]
print('One-liner: [i*i for i in range(1, 11) if i % 2 == 0]')
print(f'Result: {result1}')

print('\n2. Capitalize all words in a list:')
result2 = list(map(str.capitalize, ['hello', 'world']))
print('One-liner: list(map(str.capitalize, [\'hello\', \'world\']))')
print(f'Result: {result2}')

print('\n3. Sum of all numbers using reduce:')
result3 = reduce(lambda x, y: x + y, [1, 2, 3, 4])
print('One-liner: reduce(lambda x, y: x + y, [1, 2, 3, 4])')
print(f'Result: {result3}')
