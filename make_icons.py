import struct, zlib, os

def write_png(path, w, h, img):
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    raw = bytearray()
    for row in img:
        raw.append(0)
        for r, g, b in row:
            raw.extend((r & 255, g & 255, b & 255))
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(bytes(raw), 9)))
        f.write(chunk(b'IEND', b''))
    print('Creato: ' + path)

def make_icon(size):
    s = size / 192.0
    img = [[(19, 32, 46)] * size for _ in range(size)]

    def fill(x0, y0, w, h, color):
        for y in range(max(0, int(y0)), min(size, int(y0 + h))):
            for x in range(max(0, int(x0)), min(size, int(x0 + w))):
                img[y][x] = color

    def blend(x0, y0, w, h, color, a):
        r1, g1, b1 = color
        for y in range(max(0, int(y0)), min(size, int(y0 + h))):
            for x in range(max(0, int(x0)), min(size, int(x0 + w))):
                r0, g0, b0 = img[y][x]
                img[y][x] = (int(r0*(1-a)+r1*a), int(g0*(1-a)+g1*a), int(b0*(1-a)+b1*a))

    Y = (255, 215, 0)
    G = (255, 251, 230)

    fill(90*s, 82*s, 12*s, 78*s, Y)          # palo
    fill(91*s, 62*s,  8*s, 20*s, Y)          # braccio verticale
    fill(62*s, 58*s, 33*s,  8*s, Y)          # braccio orizzontale
    fill(42*s, 52*s, 44*s, 18*s, Y)          # corpo lampada
    fill(48*s, 54*s, 32*s, 14*s, G)          # vetro lampada

    # cono di luce (triangolo): apice=(46,70), base=(30,120)-(98,120)
    y0t, y0b = int(70*s), int(120*s)
    xa, xl, xr = 46*s, 30*s, 98*s
    r1, g1, b1 = Y
    for y in range(max(0, y0t), min(size, y0b + 1)):
        t = (y - y0t) / max(y0b - y0t, 1)
        for x in range(max(0, int(xa + (xl-xa)*t)), min(size, int(xa + (xr-xa)*t) + 1)):
            r0, g0, b0 = img[y][x]
            img[y][x] = (int(r0*0.78+r1*0.22), int(g0*0.78+g1*0.22), int(b0*0.78+b1*0.22))

    blend(30*s, 160*s, 132*s, 5*s, Y, 0.35)  # linea terra
    return img

for sz in [192, 512]:
    write_png('icons/icon-%d.png' % sz, sz, sz, make_icon(sz))

print('Fatto!')
