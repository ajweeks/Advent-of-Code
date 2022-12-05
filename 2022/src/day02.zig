const std = @import("std");
const Allocator = std.mem.Allocator;
const List = std.ArrayList;
const Map = std.AutoHashMap;
const StrMap = std.StringHashMap;
const BitSet = std.DynamicBitSet;

const util = @import("util.zig");
const gpa = util.gpa;

const Move = enum {
    rock,
    paper,
    scissors,
};

const Result = enum {
    loss,
    draw,
    win
};

const Pair = struct {
    theirs: Move,
    mine: Move,
};

// Return -1 if they win, 0 for draw, 1 if we won
fn winner(theirs: Move, mine: Move) i32 {
    const rock_wins     = [_]i32{  0,  1, -1 };
    const paper_wins    = [_]i32{ -1,  0,  1 };
    const scissor_wins  = [_]i32{  1, -1,  0 };
    return switch (theirs)  {
        .rock =>     rock_wins[@enumToInt(mine)],
        .paper =>    paper_wins[@enumToInt(mine)],
        .scissors => scissor_wins[@enumToInt(mine)],
    };
}
    
pub fn main() !void {
    var file = try std.fs.cwd().openFile("src/data/day02.txt", .{});
    defer file.close(); 
    
    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();

    const score_map = [_]usize{ 0, 3, 6 };

    var pairs = std.ArrayList(Pair).init(std.heap.page_allocator);
    var buf: [1024]u8 = undefined;
    var part1_score: usize = 0;
    var part2_score: usize = 0;
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var theirs = @intToEnum(Move, line[0] - 'A');
        var mine = @intToEnum(Move, line[2] - 'X');
        var round_winner = winner(theirs, mine);
        part1_score += @enumToInt(mine) + 1;
        part1_score += score_map[@intCast(usize, round_winner + 1)];

        var part2_winner = @intToEnum(Result, @enumToInt(mine));
        var part2_move = switch (part2_winner) {
            .loss => @intToEnum(Move, @mod(@intCast(i32, @enumToInt(theirs)) - 1, 3)),
            .draw => theirs,
            .win  => @intToEnum(Move, @mod(@intCast(i32, @enumToInt(theirs)) + 1, 3)),
        };

        part2_score += @enumToInt(part2_move) + 1;
        part2_score += score_map[@enumToInt(part2_winner)];

        try pairs.append(Pair { .theirs = theirs, .mine = mine });
    }

    print("Part 1 score: {}\n", .{ part1_score });
    print("Part 2 score: {}\n", .{ part2_score });
}

const print = std.debug.print;
const assert = std.debug.assert;
