
lines = open("day04.in").readlines()

# lines = """[1518-11-01 00:00] Guard #10 begins shift
# [1518-11-01 00:05] falls asleep
# [1518-11-01 00:25] wakes up
# [1518-11-01 00:30] falls asleep
# [1518-11-01 00:55] wakes up
# [1518-11-01 23:58] Guard #99 begins shift
# [1518-11-02 00:40] falls asleep
# [1518-11-02 00:50] wakes up
# [1518-11-03 00:05] Guard #10 begins shift
# [1518-11-03 00:24] falls asleep
# [1518-11-03 00:29] wakes up
# [1518-11-04 00:02] Guard #99 begins shift
# [1518-11-04 00:36] falls asleep
# [1518-11-04 00:46] wakes up
# [1518-11-05 00:03] Guard #99 begins shift
# [1518-11-05 00:45] falls asleep
# [1518-11-05 00:55] wakes up""".splitlines()

guards = dict()
for line in lines:
    a = line.split(' ')[2]
    if a == "Guard":
        num = int(line.split(' ')[3][1:])
        guards[num] = []

dateTimes = []
for line in lines:
    dateTimeRough = line.split(']')[0]
    dateTime = [
        int(dateTimeRough.split('-')[1]),       # Month
        int(dateTimeRough.split('-')[2][:2]),   # Day
        int(dateTimeRough.split(':')[0][-2:]),  # Hour
        int(dateTimeRough.split(':')[1])]       # Min
    dateTimes.append([dateTime, line.split(']')[1]])


def date_time_cmp(a):
    return a[0][0] * 1000000 + a[0][1] * 10000 + a[0][2] * 100 + a[0][3]


dateTimes = sorted(dateTimes, key=date_time_cmp)

guardIdx = 0
for dateTimePair in dateTimes:
    dateTime = dateTimePair[0]
    actionRough = dateTimePair[1]
    a = actionRough.split(' ')[1]
    if a == "Guard":
        guardIdx = int(actionRough.split(' ')[2][1:])
    else:
        guards[guardIdx].append(dateTime)

sleepiest = 0
sleepiestI = 0
sleepiestMins = 0
i = 0
for g, v in guards.items():
    print(f"{g}: {v}")
    minsAsleep = 0
    for k in range(0, len(v) - 1, 2):
        minsAsleep += (v[k+1][2]*60+v[k+1][3]) - (v[k][2]*60+v[k][3])
    if minsAsleep > sleepiestMins:
        sleepiestMins = minsAsleep
        sleepiest = g
        sleepiestI = i
    i += 1

print(f"sleepiest: {sleepiest}, sleepiestI: {sleepiestI}, sleepiestMins: {sleepiestMins}")

minsAsleep = []
for i in range(len(guards)):
    minsAsleep.append([0] * 60)

for g, gi in enumerate(guards):
    for i in range(0, len(guards[gi]) - 1, 2):
        for j in range(guards[gi][i][3], guards[gi][i+1][3]):
            # TODO: Handle hours & days
            minsAsleep[g][j] += 1

print(minsAsleep)

mostAsleepSleepiest = 0
mostAsleepSleepiestMin = 0
for s in range(len(minsAsleep[sleepiestI])):
    if minsAsleep[sleepiestI][s] > mostAsleepSleepiestMin:
        mostAsleepSleepiestMin = minsAsleep[sleepiestI][s]
        mostAsleepSleepiest = s

mostAsleep = 0
mostAsleepMin = 0
minuteSnoozer = 0
for g, gi in enumerate(guards):
    for s in range(len(minsAsleep[g])):
        if minsAsleep[g][s] > mostAsleepMin:
            mostAsleepMin = minsAsleep[g][s]
            mostAsleep = s
            minuteSnoozer = gi

print(f"most asleep: {mostAsleepSleepiest}, for {mostAsleepSleepiestMin}m - product: {sleepiest*mostAsleepSleepiest}")
print(f"most asleep on min: {mostAsleep}, for {mostAsleepMin}m, minuteSnoozer: {minuteSnoozer} - product: {minuteSnoozer*mostAsleep}")


