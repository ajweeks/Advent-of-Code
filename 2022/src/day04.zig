const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;
const Map = std.AutoHashMap;
const StrMap = std.StringHashMap;
const BitSet = std.DynamicBitSet;

const util = @import("util.zig");
const gpa = util.gpa;

const Range = struct {
    begin: u32,
    end: u32,
};

pub fn main() !void {
    
    var file = try std.fs.cwd().openFile("src/data/day04.txt", .{});
    defer file.close(); 
    
    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    var ranges = ArrayList([2]Range).init(gpa);
    var overlaps: usize = 0;
    var full_overlaps: usize = 0;

    var buf: [1024]u8 = undefined;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        if (line.len == 0) continue;
        var iter = std.mem.split(u8, line, ",");
        var range_0 = iter.first();
        var range_1 = iter.next().?;
        var iter_0 = std.mem.split(u8, range_0, "-");
        var iter_1 = std.mem.split(u8, range_1, "-");
        try ranges.append([2]Range {
            Range {
                .begin = try parseInt(u32, iter_0.first(), 10),
                .end = try parseInt(u32, iter_0.next().?, 10),
            },
            Range {
                .begin = try parseInt(u32, iter_1.first(), 10),
                .end = try parseInt(u32, iter_1.next().?, 10),
            }
        });

        var range = &ranges.items[ranges.items.len - 1];
        if ((range[0].begin <= range[1].begin and range[0].end >= range[1].end) or
            (range[1].begin <= range[0].begin and range[1].end >= range[0].end)) {
                // print("full_overlap: {any}\n", .{ range.* });
                full_overlaps += 1;
        }
        if ((range[0].begin <= range[1].begin and range[1].begin <= range[0].end) or
            (range[0].begin <= range[1].end   and range[1].end   <= range[0].end) or
            (range[1].begin <= range[0].begin and range[0].begin <= range[1].end) or
            (range[1].begin <= range[0].end   and range[0].end   <= range[1].end)) {
                // print("overlap: {any}\n", .{ range.* });
                overlaps += 1;
        }
        // print("{any}\n", .{ ranges.items[ranges.items.len - 1] });
    }

    print("Part 1: {}\n", .{ full_overlaps });
    print("Part 2: {}\n", .{ overlaps });
}

const parseInt = std.fmt.parseInt;

const print = std.debug.print;
const assert = std.debug.assert;
