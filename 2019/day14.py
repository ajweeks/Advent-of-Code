import math


def get_input_str():
    return open("day14.in").readlines()


def get_inputs(input_str):
    res = []
    for line in input_str:
        parts = line.strip().split('=>')
        ingredients = parts[0].split(',')
        res.append(([(int(i.strip().split(' ')[0]), i.strip().split(' ')[1]) for i in ingredients],
                    (int(parts[1].strip().split(' ')[0]), parts[1].strip().split(' ')[1])))
    return res


surplus = dict()


def required_ore_for_product(product, quantity, recipes):
    global surplus

    recipe = list(filter(lambda r: r[1][1] == product, recipes))[0]
    existing = surplus.get(product) or 0
    batches = math.ceil(max(quantity - existing, 0) / recipe[1][0])
    extra = recipe[1][0] * batches - (quantity - existing)
    if recipe[1][1] != 'ORE':
        surplus[recipe[1][1]] = extra
    required_ore = 0
    for ingredient in recipe[0]:
        if ingredient[1] == 'ORE':
            required_ore += batches * ingredient[0]
        else:
            required_ore += required_ore_for_product(ingredient[1], batches * ingredient[0], recipes)
    return required_ore


def part1():
    recipes = get_inputs(get_input_str())
    recipes2 = get_inputs("""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".splitlines())

    return required_ore_for_product('FUEL', 1, recipes)


def part2():
    recipes = get_inputs(get_input_str())
    recipes1 = get_inputs("""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".splitlines())

    min_fuel = 1000
    max_fuel = 1000000000

    while 1:
        fuel_guess = min_fuel + (max_fuel - min_fuel) // 2
        required_ore = required_ore_for_product('FUEL', fuel_guess, recipes)
        if required_ore > 1_000_000_000_000:
            max_fuel = fuel_guess
        elif required_ore < 1_000_000_000_000:
            min_fuel = fuel_guess

        if min_fuel == max_fuel - 1:
            max_fuel = min_fuel
            break

    return max_fuel
