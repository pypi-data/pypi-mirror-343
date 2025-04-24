from collections import defaultdict
import time


def next_number(num: int) -> int:
    if num % 2 == 0:
        return num // 2

    else:
        return 3 * num + 1


def verifies_conjecture(num: int) -> bool:
    while num != 1:
        num = next_number(num)

    return True


"""
t1 = time.time()
for i in range(1, 10000000):
    if verifies_conjecture(i):
        if i % 1000  == 0:
            print("Verifies conjecture:", i)
t2 = time.time()

print("Total time:", t2 - t1)
"""

distribution = [0] * 9

for i in range(1, 100000000):
    num = i
    while not num == 1:
        first_digit = int(str(num)[0])
        distribution[first_digit - 1] += 1
        num = next_number(num)

    if i % 1000 == 0:
        print(i)

total_nums = sum(distribution)
for num in range(1, 10):
    print(str(num) + ":", round(distribution[num - 1] / total_nums * 100, 2), "%")



print("\nTotal numbers:", total_nums)

"""
Distribution found up to 10,000,000:

1: 29.44 %
2: 17.54 %
3: 12.04 %
4: 10.99 %
5: 7.99 %
6: 6.03 %
7: 5.78 %
8: 5.41 %
9: 4.77 %

Total numbers: 1,552,724,686


Distribution found up to 100,000,000:

1: 29.53 %
2: 17.55 %
3: 12.1 %
4: 10.82 %
5: 7.98 %
6: 6.12 %
7: 5.78 %
8: 5.37 %
9: 4.74 %

Total numbers: 17,923,493,476
"""
