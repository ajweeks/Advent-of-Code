
f = open("day_12_input.txt")
fileStr = f.read()

# fileStr = "0 <-> 2\n\
# 1 <-> 1\n\
# 2 <-> 0, 3, 4\n\
# 3 <-> 2, 4\n\
# 4 <-> 2, 3, 6\n\
# 5 <-> 6\n\
# 6 <-> 4, 5"

pipes = []
for line in fileStr.splitlines():
    pipes.append([int(x.strip(',')) for x in line.split()[2:]])

pipe_groups = [[]]

group_index = 0
group_count = 0

for p_ind in range(len(pipes)):
    if p_ind in pipes[p_ind]:
        group_count += 1
        if p_ind not in pipe_groups[group_index]:
            pipe_groups[group_index].append(p_ind)

# Don't ask me how this one works - I was just lucky to find the solution
print(len(pipe_groups[0]), group_count)

