import drawsvg as dw
import pybrl as brl
from PIL import ImageFont
import math
import platform


def textToBraille(s):
    return brl.toUnicodeSymbols(brl.translate(s), flatten=True)

def mmToPx(mm, dpi):
    return mm*dpi/25.4

def textToSVG(s, mirror=False):
    osname = platform.system()
    if osname == "Windows":
        fontName = "cour.ttf"  # Windows path
    elif osname == "Darwin":  # macOS
        fontName = "Courier New.ttf"  # macOS path
    else:
        fontName = "cour.ttf"
    
    fontSize = 24
    dpi = 96
    margins = mmToPx(15, dpi)
    rightMarginBonus = 0 # Depending on the svg viewer/conversions/other nonsense, the auto text wrapping may break down. Change this to tune the margins!
    charSizeBonus = 1.1 # same purpose as above: increase predicted size of characters by this factor
    paperSizes = {
        "A4": (210, 297), # In mm
        "A3": (297, 420),

        "B4": (250, 353),
        "B5": (176, 250)
    }
    width = mmToPx(paperSizes["A4"][0],dpi)
    height = mmToPx(paperSizes["A4"][1],dpi)
    try:
        font = ImageFont.truetype(fontName, fontSize) # Even with monospace font, braille dots are larger than letters!!! this lib doesn't seem to respect that
    except:
        print("Courier New not found! Using Liberation Mono as a backup.")
        font = ImageFont.truetype("LiberationMono-Regular.ttf", fontSize)
    charLen = font.getlength("⠻")*charSizeBonus
    testb1 = font.getbbox("⠻")
    testb2 = font.getbbox("w")
    print("diff: "+str(testb1[2]-testb1[0])) # This works!!!
    charsPerLine = math.floor((width-(margins*2)-rightMarginBonus)/charLen)
    s=s.replace("\n"," ")

    news = ""
    while (len(s)>charsPerLine):
        index = s.rfind(" ", 0, charsPerLine)
        news+=s[0:index]+"\n"
        s = s[index+1:]
    s=news
    print(s)


    d = dw.Drawing(width, height, origin=(0,0), font_family="Courier New") #Switch this to monospace if possible! May not matter, but online viewers are being strange.
    # Mark top right corner
    if mirror:
        e = dw.Group(transform="scale(-1, 1) translate({}, 0)".format(-1*width))
        e.append(dw.Text(s, font_size=fontSize, x=margins, y=60))
        e.append(dw.Line(width-50, 0, width, 50))
        d.append(e)
    else:
        d.append(dw.Text(s, font_size=fontSize, x=margins, y=60))
        d.append(dw.Line(width-50, 0, width, 50, stroke='black'))

    d.save_svg("test.svg")

if __name__ == "__main__":
    #print(brl.toUnicodeSymbols(brl.translate(input("Enter: ")), flatten=True))
    textToSVG("⠠⠭ ⠴ ⠮ ⠆⠌ ⠷ ⠞⠊⠍⠑⠎ ⠭ ⠴ ⠮ ⠺⠕⠗⠌ ⠷ ⠞⠊⠍⠑⠎ ⠭ ⠴ ⠮ ⠁⠛⠑ ⠷ ⠺⠊⠎⠙⠕⠍ ⠭ ⠴ ⠮ ⠁⠛⠑ ⠷ ⠋⠕⠕⠇⠊⠩⠝⠑⠎⠎ ⠭ ⠴ ⠮ ⠑⠏⠕⠡ ⠷ ⠆⠑⠇⠊⠋ ⠭ ⠴ ⠮ ⠑⠏⠕⠡ ⠷ ⠔⠉⠗⠫⠥⠇⠊⠞⠽ ⠭ ⠴ ⠮ ⠎⠂⠎⠕⠝ ⠷ ⠠⠇⠊⠣⠞ ⠭ ⠴ ⠮ ⠎⠂⠎⠕⠝ ⠷ ⠠⠙⠜⠅⠝⠑⠎⠎ ⠭ ⠴ ⠮ ⠎⠏⠗⠬ ⠷ ⠓⠕⠏⠑ ⠭ ⠴ ⠮ ⠺⠔⠞⠻ ⠷ ⠙⠑⠎⠏⠁⠊⠗ ⠺⠑ ⠓⠁⠙ ⠑⠧⠻⠽⠹⠬ ⠆⠑⠿ ⠥ ⠺⠑ ⠓⠁⠙ ⠝⠕⠹⠬ ⠆⠑⠿ ⠥ ⠺⠑ ⠛⠛ ⠁⠇⠇ ⠛⠕⠬ ⠙⠊⠗⠑⠉⠞ ⠋⠋ ⠠⠓⠂⠧⠢ ⠺⠑ ⠛⠛ ⠁⠇⠇ ⠛⠕⠬ ⠙⠊⠗⠑⠉⠞ ⠮ ⠕⠮⠗ ⠺⠁⠽⠔ ⠩⠕⠗⠞ ⠮ ⠏⠻⠊⠕⠙ ⠴ ⠎ ⠋⠜ ⠇⠊⠅⠑ ⠮ ⠏⠗⠑⠎⠢⠞ ⠏⠻⠊⠕⠙ ⠞ ⠎⠕⠍⠑ ⠷ ⠊⠞⠎ ⠝⠕⠊⠎⠊⠑⠌ ⠁⠥⠹⠕⠗⠊⠞⠊⠑⠎ ⠔⠎⠊⠌⠫ ⠕⠝ ⠊⠞⠎ ⠆⠬ ⠗⠑⠉⠑⠊⠧⠫ ⠿ ⠛⠕⠕⠙ ⠕⠗ ⠿ ⠑⠧⠊⠇ ⠔ ⠮ ⠎⠥⠏⠻⠇⠁⠞⠊⠧⠑ ⠙⠑⠛⠗⠑⠑ ⠷ ⠉⠕⠍⠏⠜⠊⠎⠕⠝ ⠕⠝⠇⠽ It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way--in short, the period was so far like the present period, that some of its noisiest authorities insisted on its being received, for good or for evil, in the superlative degree of comparison only.")