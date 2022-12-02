const std = @import("std");
const Allocator = std.mem.Allocator;
const List = std.ArrayList;
const Map = std.AutoHashMap;
const StrMap = std.StringHashMap;
const BitSet = std.DynamicBitSet;

const util = @import("util.zig");
const gpa = util.gpa;

pub fn main() !void {
    var file = try std.fs.cwd().openFile("C:/Code/Advent-of-Code/2022/src/data/day01.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();
        
    var numsArray = std.ArrayList(usize).init(std.heap.page_allocator);
    var buf: [1024]u8 = undefined;
    var most_calories = [3]usize{ 0, 0, 0};
    var current_calories: usize = 0;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        if (line.len > 0) {
            var cal = try parseInt(usize, line, 10);
            try numsArray.append(cal);
            current_calories += cal;
        } else {
            var min_cal: usize = 99999999;

            for (most_calories) |max_cal| {
                if (max_cal < min_cal) {
                    min_cal = max_cal;
                }
            }

            if (current_calories > min_cal) {
                for (most_calories) |*max_cal, i| {
                    if (max_cal.* == min_cal) {
                        var before = max_cal.*;
                        max_cal.* = current_calories;
                        print("{}) {} -> {}\n", .{ i, before, max_cal.* });
                        break;
                    }
                }
            }

            current_calories = 0;
        }
    }

    // for (numsArray.items) |a, i| {
    //     print("{}: {}\n", .{ i, a });
    // }
    
    print("\n", .{ });

    var max_cal: usize = 0;
    var max_sum_cal: usize = 0;
    for (most_calories) |max_i, i| {
        print("{}) {}\n", .{ i, max_i });
        max_sum_cal += max_i;
        max_cal = if (max_i > max_cal) max_i else max_cal;
    }

    print("\n", .{ });

    print("Part 1: {}\n", .{ max_cal });
    print("Part 2: {}\n", .{ max_sum_cal });
}

// Useful stdlib functions
const tokenize = std.mem.tokenize;
const split = std.mem.split;
const indexOf = std.mem.indexOfScalar;
const indexOfAny = std.mem.indexOfAny;
const indexOfStr = std.mem.indexOfPosLinear;
const lastIndexOf = std.mem.lastIndexOfScalar;
const lastIndexOfAny = std.mem.lastIndexOfAny;
const lastIndexOfStr = std.mem.lastIndexOfLinear;
const trim = std.mem.trim;
const sliceMin = std.mem.min;
const sliceMax = std.mem.max;

const parseInt = std.fmt.parseInt;
const parseFloat = std.fmt.parseFloat;

const min = std.math.min;
const min3 = std.math.min3;
const max = std.math.max;
const max3 = std.math.max3;

const print = std.debug.print;
const assert = std.debug.assert;

const sort = std.sort.sort;
const asc = std.sort.asc;
const desc = std.sort.desc;

// Generated from template/template.zig.
// Run `zig build generate` to update.
// Only unmodified days will be updated.
