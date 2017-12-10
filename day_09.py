
f = open("day_09_input.txt")
fileStr = f.read()

# fileStr = "<{o\"i!a,<{i<a>"

groups = 0
groups_deep = 0
score = 0
garbage_count = 0

cancelled = False
in_garbage = False

for c in fileStr:
    if cancelled:
        cancelled = False
        print("cancelled")
        continue
    elif in_garbage:
        if c == '>':
            in_garbage = False
            print("out of garbage")
        elif c == '!':
            cancelled = True
            print("next is cancelled")
        else:
            print("in garbage")
            garbage_count  += 1
    else:
        if c == '{':
            groups_deep += 1
            print("into group")
        elif c == '}':
            score += groups_deep
            groups_deep -= 1
            groups += 1
            print("out of group")
        elif c == '!':
            cancelled = True
            print("next is cancelled (!!!??!)")
        elif c == '<':
            in_garbage = True
            print("into garbage")
        elif c == '>':
            in_garbage = False
            print("out of garbage!")

print("groups:", groups, "score:", score, "garbage count:", garbage_count)
