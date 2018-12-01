
def knot_hash(instructions, current_pos, skip_size, nums, mutate_instructions):
    if mutate_instructions:
        instructions = [ord(c) for c in instructions]
        for suffix in [17, 31, 73, 47, 23]:
            instructions.append(suffix)

    for length in instructions:
        # Reverse section
        for i in range(int(length / 2)):
            i1 = (i + current_pos) % len(nums)
            i2 = (length - i - 1 + current_pos) % len(nums)
            nums[i1], nums[i2] = nums[i2], nums[i1]

        current_pos = (current_pos + length + skip_size) % len(nums)
        skip_size += 1

    return current_pos, skip_size, nums


def to_hex(num):
    res = hex(num)[2:].zfill(2)
    return res


def knot_hash_to_hex_str(nums):
    dense = []
    for i in range(16):
        dense.append(nums[i * 16])
        for j in range(1, 16):
            dense[i] ^= nums[i * 16 + j]

    hash_str = ""
    for d in dense:
        hash_str += to_hex(d)

    return hash_str
