
f = open("day_18_input.txt")

fileStr = f.read()
rowCount = 400000

safe_tile_count = 0


def count_safe_spots(tiles):
    count = 0
    for i in range(len(tiles)):
        if tiles[i] == '.':
            count += 1
    return count


safe_tile_count += count_safe_spots(fileStr)


def trap_at_index(index, p_row):
    if index == 0:
        return p_row[index + 1] == '^'
    elif index == len(p_row) - 1:
        return p_row[index - 1] == '^'
    else:
        return (p_row[index - 1] == '^' and p_row[index + 1] == '.') or (p_row[index - 1] == '.' and p_row[index + 1] == '^')


pRow = fileStr
for i in range(rowCount - 1):
    row = ""
    for j in range(len(pRow)):
        trap = trap_at_index(j, pRow)
        row += '^' if trap else '.'

    safe_tile_count += count_safe_spots(row)
    pRow = row

print(safe_tile_count)
