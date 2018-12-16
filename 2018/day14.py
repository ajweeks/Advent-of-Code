
s = int(open("day14.in").read())
digits = [int(x) for x in str(s)]

# s = 9
# s = 59414

recipes = [3, 7]
elf1, elf2 = 0, 1
p1 = ''
i = 0
while recipes[-len(digits):] != digits and recipes[-len(digits)-1:-1] != digits:
    recipes.extend([int(x) for x in str(int(recipes[elf1]) + int(recipes[elf2]))])

    elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
    elf2 = (elf2 + 1 + recipes[elf2]) % len(recipes)

    i += 1

    if len(p1) == 0 and len(recipes) == s + 10:
        p1 = ''.join([str(s) for s in recipes[-10:]])

    if i % 1000000 == 0:
        print(i, len(recipes))

print(f"p1: {p1}")
print(f"p2: {len(recipes) - len(digits) - (0 if recipes[-len(digits):] == digits else 1)}")
