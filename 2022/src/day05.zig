const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;

const String = @import("external/zig-string.zig").String;
const util = @import("util.zig");
const gpa = util.gpa;

const Stack = struct {
    const Self = @This();

    crates: ArrayList(u8),

    pub fn clone(self: *Self) !Self {        
        return Self {
            .crates = try self.crates.clone(),
        };
    }
};

const Instruction = struct {
    count: u32,
    from: u8,
    to: u8,
};

pub fn main() !void {
    var file = try std.fs.cwd().openFile("src/data/day05.txt", .{});
    defer file.close(); 
    
    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    var stack_lines = ArrayList(String).init(gpa);

    var buf: [1024]u8 = undefined;
    var num_stacks: u32 = 0;
    outer: while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {

        var i = @intCast(i32, line.len - 1);
        inner: while (i > 0) : (i -= 1) {
            if (std.ascii.isWhitespace(line[@intCast(u32, i)])) continue;

            if (std.ascii.isDigit(line[@intCast(u32, i)])) {
                var int_str = [_]u8{ line[@intCast(u32, i)] };
                num_stacks = try parseInt(u32, &int_str, 10);
                break :outer;
            } else  {
                try stack_lines.append(try String.new(gpa, line));

                break :inner;
            }
        }
    }

    var stacks = try ArrayList(Stack).initCapacity(gpa, num_stacks);

    var i: usize = 0;
    while (i < num_stacks) : (i +=1 ) {
        try stacks.append(Stack {
            .crates = ArrayList(u8).init(gpa),
        });
    }

    var line_i = @intCast(i32, stack_lines.items.len - 1);
    while (line_i > -1) : (line_i -=1 ) {
        var line = stack_lines.items[@intCast(usize, line_i)];

        var x: usize = 0;
        while (x < num_stacks) : (x += 1) {
            if (line.str()[x * 4] == '[') {
                var crate = line.str()[x * 4 + 1];
                try stacks.items[x].crates.append(crate);
            }
        }
    }

    var instructions = ArrayList(Instruction).init(gpa);

    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        if (line.len == 0) continue;

        var iter = std.mem.split(u8, line, " ");

        _ = iter.first();
        var count = try parseInt(u32, iter.next().?, 10);      _ = iter.next().?;
        var from  = (try parseInt(u8, iter.next().?, 10)) - 1; _ = iter.next().?;
        var to    = (try parseInt(u8, iter.next().?, 10)) - 1;
        var inst = Instruction {
            .count = count,
            .from = from,
            .to = to,
        };

        try instructions.append(inst);
    }

    var stacks_2 = ArrayList(Stack).init(gpa);
    for (stacks.items) |*stack| {
        try stacks_2.append(try stack.clone());
    }

    try Operate(true, instructions, stacks);
    print("Part 1: ", .{});
    PrintStackTops(&stacks);

    try Operate(false, instructions, stacks_2);
    print("Part 2: ", .{});
    PrintStackTops(&stacks_2);
}

fn Operate(part1: bool, instructions: ArrayList(Instruction), stacks: ArrayList(Stack)) !void {
    for (instructions.items) |inst| {
        var count = @intCast(i32, inst.count);
        const init_count = @intCast(usize, count);

        const stack_from = &stacks.items[inst.from].crates;

        while (count > 0) : (count -= 1) {
            if (part1) {
                const from_idx = stack_from.items.len - 1;
                try stacks.items[inst.to].crates.append(stack_from.items[from_idx]);
                _ = stack_from.pop();
            } else {
                const from_idx = stack_from.items.len - @intCast(usize, count);
                try stacks.items[inst.to].crates.append(stack_from.items[from_idx]);
            }

            // PrintStacks(&stacks);
        }
        
        if (!part1) {
            try stack_from.resize(stack_from.items.len - init_count);
        }
    }
}

fn PrintStacks(stacks: *const ArrayList(Stack)) void {
    for (stacks.items) |stack| {
        for (stack.crates.items) |c| {
            print("{c} ", .{ c });
        }
        print("\n", .{});
    }
    print("\n", .{});
}

fn PrintStackTops(stacks: *const ArrayList(Stack)) void {
    for (stacks.items) |stack| {
        print("{c}", .{ stack.crates.items[stack.crates.items.len - 1] });
    }
    print("\n", .{});
}

// Useful stdlib functions
const parseInt = std.fmt.parseInt;

const print = std.debug.print;
const assert = std.debug.assert;
