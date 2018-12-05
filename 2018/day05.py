
from timeit import default_timer as timer

inputStr = open("day05.in").read()

# inputStr = "dabAcCaCBAcCcaDA"
result = inputStr


def react(a, b):
    return a.lower() == b.lower() and ((a.islower() and b.isupper()) or (a.isupper() and b.islower()))


start = timer()
reactions = 0
reacted = True
lastReactionSite = 0
while reacted:
    reacted = False
    for c in range(max(lastReactionSite - 1, 0), len(result) - 1):
        if react(result[c], result[c + 1]):
            result = result[:c] + result[c + 2:]
            reacted = True
            reactions += 1
            lastReactionSite = c
            break
end = timer()

print(f"polymer len: {len(result)}, reactions: {reactions}, took {end-start}s")

start2 = timer()
modifiedPolymers = []
for i in range(26):
    modified = inputStr

    modified = modified.replace(chr(ord('a') + i), "")
    modified = modified.replace(chr(ord('A') + i), "")

    modifiedPolymers.append(modified)

print(modifiedPolymers)

for m in range(len(modifiedPolymers)):
    reacted = True
    lastReactionSite = 0
    while reacted:
        reacted = False
        for c in range(max(lastReactionSite - 1, 0), len(modifiedPolymers[m]) - 1):
            if react(modifiedPolymers[m][c], modifiedPolymers[m][c + 1]):
                modifiedPolymers[m] = modifiedPolymers[m][:c] + modifiedPolymers[m][c + 2:]
                reacted = True
                lastReactionSite = c
                break
end2 = timer()

print(modifiedPolymers)

shortestLen = len(modifiedPolymers[0])
shortestIdx = 0
for i in range(len(modifiedPolymers)):
    mLen = len(modifiedPolymers[i])
    if mLen < shortestLen:
        shortestIdx = i
        shortestLen = mLen

print(f"shortest modified polymer len: {shortestLen},"
      f"(removed {chr(ord('A') + shortestIdx)}/{chr(ord('a') + shortestIdx)}),"
      f" took {end2-start2}s")
