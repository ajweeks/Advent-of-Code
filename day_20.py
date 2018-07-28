
f = open("day_20_input.txt")
particlesS = f.read()


class V3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]'

    def __repr__(self):
        return f'[{self.x}, {self.y}, {self.z}]'

    x, y, z = 0, 0, 0


class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def __str__(self):
        return f'[p: {self.p}, v: {self.v}, a: {self.a}]'

    def __repr__(self):
        return f'[p: {self.p}, v: {self.v}, a: {self.a}]'

    p = 0
    v = 0
    a = 0


particles = []
for pS in particlesS.split('\n'):
    parts = pS.split('<')
    posS = parts[1].split('>')[0]
    posSParts = posS.split(',')
    p = V3(int(posSParts[0]), int(posSParts[1]), int(posSParts[2]))
    velS = parts[2].split('>')[0]
    velSParts = velS.split(',')
    v = V3(int(velSParts[0]), int(velSParts[1]), int(velSParts[2]))
    accS = parts[3].split('>')[0]
    accSParts = accS.split(',')
    a = V3(int(accSParts[0]), int(accSParts[1]), int(accSParts[2]))
    particles.append(Particle(p, v, a))

print(particles)

closestTo0 = -1

part_1 = False

while 1:
    min_dst = 99999999
    min_dst_idx = 0
    to_remove = set()

    for pi in range(len(particles)):
        particles[pi].v.x += particles[pi].a.x
        particles[pi].v.y += particles[pi].a.y
        particles[pi].v.z += particles[pi].a.z
        particles[pi].p.x += particles[pi].v.x
        particles[pi].p.y += particles[pi].v.y
        particles[pi].p.z += particles[pi].v.z

        if part_1:
            dst = abs(particles[pi].p.x) + abs(particles[pi].p.y) + abs(particles[pi].p.z)
            if dst < min_dst:
                min_dst = dst
                min_dst_idx = pi

            print(min_dst, min_dst_idx)

    if not part_1:
        for pi in range(len(particles)):
            for pi2 in range(pi + 1, len(particles)):
                if particles[pi2].p.x == particles[pi].p.x and \
                        particles[pi2].p.y == particles[pi].p.y and \
                        particles[pi2].p.z == particles[pi].p.z:
                    to_remove.add(pi)
                    to_remove.add(pi2)

        if len(to_remove) > 0:
            to_remove = (sorted(to_remove, reverse=True))

            for tr in to_remove:
                particles = particles[:tr] + particles[tr + 1:]
            print(f"removed {len(to_remove)} particles, {len(particles)} remaining")
