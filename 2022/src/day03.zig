const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;
const Map = std.AutoHashMap;
const StrMap = std.StringHashMap;
const BitSet = std.DynamicBitSet;

const util = @import("util.zig");
const gpa = util.gpa;

const Rucksack = struct {
    items: ArrayList(u8),
    dupe: u8,
    badge: u8,
};

pub fn main() !void {
    var file = try std.fs.cwd().openFile("src/data/day03.txt", .{});
    defer file.close(); 
    
    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    var rucksacks = ArrayList(Rucksack).init(gpa);
    
    var summed_prio: usize = 0;
    var summed_badges: usize = 0;

    var buf: [1024]u8 = undefined;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var left = ArrayList(u8).init(gpa);
        var right = ArrayList(u8).init(gpa);
        var dupe: u8 = std.math.maxInt(u8);

        for (line) |char, i| {
            if (char == ' ' or char == '\n' or char == '\r') continue;

            var in_left = i < line.len / 2;
            if (in_left) {
               try left.append(char);
            } else {
               try right.append(char);
            }
        }
    
        outer: for (left.items) |left_item| {
            for (right.items) |right_item| {
                if (left_item == right_item) {
                    dupe = left_item;
                    break :outer;
                }
            }
        }

        assert(dupe != std.math.maxInt(u8));

        var prio = if (dupe <= 'Z') dupe - 'A' + 27 else dupe - 'a' + 1;

        summed_prio += prio;

        var items = left;
        try items.appendSlice(right.items);
        try rucksacks.append(Rucksack {
            .items = items,
            .dupe = dupe,
            .badge = std.math.maxInt(u8),
        });
    }

    var i: usize = 0;
    while (i < rucksacks.items.len - 2) : (i += 3) {
        var badge = outer: {
            for (rucksacks.items[i].items.items) |char_0| {
                for (rucksacks.items[i + 1].items.items) |char_1| {
                    for (rucksacks.items[i + 2].items.items) |char_2| {
                        if (char_0 == char_1 and char_1 == char_2) {
                            break :outer char_0;
                        }
                    }
                }
            }
            assert(false);
            break :outer std.math.maxInt(u8);
        };
        assert(badge != std.math.maxInt(u8));

        rucksacks.items[i].badge = badge;
        rucksacks.items[i + 1].badge = badge;
        rucksacks.items[i + 2].badge = badge;
        summed_badges += if (badge <= 'Z') badge - 'A' + 27 else badge - 'a' + 1;
    }

    print("Part 1 {}\n", .{ summed_prio });
    print("Part 2 {}\n", .{ summed_badges });
}

const print = std.debug.print;
const assert = std.debug.assert;
