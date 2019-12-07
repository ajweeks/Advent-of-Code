import intcode


def get_input_str():
    return open("day07.in").readlines()[0]


def get_inputs(input_str):
    return [int(y) for y in input_str.split(',')]


def part1():
    # inputs = get_inputs("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    max_power = 0
    for a in range(0, 5):
        for b in range(0, 5):
            if b == a: continue
            for c in range(0, 5):
                if c == b or c == a: continue
                for d in range(0, 5):
                    if d == c or d == b or d == a: continue
                    for e in range(0, 5):
                        if e == d or e == c or e == b or e == a: continue

                        inputs = get_inputs(get_input_str())

                        ampA = intcode.Intcode()
                        ampB = intcode.Intcode()
                        ampC = intcode.Intcode()
                        ampD = intcode.Intcode()
                        ampE = intcode.Intcode()

                        ampA.receive_signal(a)
                        ampA.receive_signal(0)
                        out = ampA.run(inputs, False, True)
                        ampB.receive_signal(b)
                        ampB.receive_signal(out)
                        out = ampB.run(inputs, False, True)
                        ampC.receive_signal(c)
                        ampC.receive_signal(out)
                        out = ampC.run(inputs, False, True)
                        ampD.receive_signal(d)
                        ampD.receive_signal(out)
                        out = ampD.run(inputs, False, True)
                        ampE.receive_signal(e)
                        ampE.receive_signal(out)
                        out = ampE.run(inputs, False, True)
                        if out > max_power:
                            max_power = out

    return max_power


def part2():
    max_power = 0
    for a in range(5, 10):
        for b in range(5, 10):
            if b == a: continue
            for c in range(5, 10):
                if c == b or c == a: continue
                for d in range(5, 10):
                    if d == c or d == b or d == a: continue
                    for e in range(5, 10):
                        if e == d or e == c or e == b or e == a: continue

                        inputs = get_inputs(get_input_str())

                        ampA = intcode.Intcode()
                        ampB = intcode.Intcode()
                        ampC = intcode.Intcode()
                        ampD = intcode.Intcode()
                        ampE = intcode.Intcode()

                        ampA.receive_signal(a)
                        ampA.receive_signal(0)
                        ampB.receive_signal(b)
                        ampC.receive_signal(c)
                        ampD.receive_signal(d)
                        ampE.receive_signal(e)

                        some_running = True
                        final_out = 0
                        while some_running:
                            out = ampA.run(inputs, False, True)
                            ampB.receive_signal(out)
                            out = ampB.run(inputs, False, True)
                            ampC.receive_signal(out)
                            out = ampC.run(inputs, False, True)
                            ampD.receive_signal(out)
                            out = ampD.run(inputs, False, True)
                            ampE.receive_signal(out)
                            out = ampE.run(inputs, False, True)

                            if not ampA.is_complete() or not ampB.is_complete() or not ampC.is_complete() or not ampD.is_complete() or not ampE.is_complete():
                                ampA.receive_signal(out)
                            else:
                                final_out = out
                                some_running = False

                        if final_out > max_power:
                            max_power = final_out

    return max_power
