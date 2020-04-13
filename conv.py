from PIL import Image
import math

MAX_VALUE = 15 #for 12 bit/ 4 bit per color => 0 - 15 the values
SHIFT_FACTOR = 4 #to lighten the image 

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * MAX_VALUE), int(g * MAX_VALUE), int(b * MAX_VALUE)
    return r, g, b
    
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


imgs = ["1.png"] #list of images
get_bin = lambda x, n: format(x, 'x').zfill(n)  #format for binary
output = open("raw.out","w") #if you need the data for a ROM memory

output.write("(")
for t in range(len(imgs)):
    output.write("(")
    im = Image.open(imgs[t])
    pix = im.load()
    size = im.size
    print(size)
    lenx = int(size[0])
    leny = int(size[1])
    imrez = Image.new("RGB",size) #the output

    print(lenx, leny)
    for y in range(leny):
        output.write("(")
        for x in range(lenx):
            r = pix[x, y][0] 
            g = pix[x, y][1] 
            b = pix[x, y][2] 

            h, s, v = rgb2hsv(r, g, b)
            r, g, b = hsv2rgb(h, s, v)

            imrez.putpixel((x,y),(r<<SHIFT_FACTOR, g<<SHIFT_FACTOR, b<<SHIFT_FACTOR)) 
            output.write("x\"" + get_bin(r,1) + get_bin(g,1) + get_bin(b,1) + "\"")

            if x != lenx - 1:
                output.write(",")
       
        if(y != leny -1):
            output.write("),\n");
        else:
            output.write(")")

    if(t != len(imgs) - 1):
        output.write("),\n\n")
    else: 
        output.write(")")

    imrez.save("{}out.png".format(imgs[t].replace(".png","")))
    imrez.close()
output.write(");")
output.close()

