"""Render both silent H.264 cuts, their posters, and descriptive captions.
Requires system Python with Pycairo and Pillow, and ffmpeg on PATH.
Run check.py before rendering to regenerate the source models.
"""
import argparse
import io
import json
import math
import random
import subprocess
from functools import lru_cache
from pathlib import Path

import cairo
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "assets/model-films"
STEM = "change-the-grammar"
MODEL = json.loads((HERE / "model.json").read_text())
EX = [item["pairs"] for item in MODEL["examples"]]
SEQ = MODEL["sequence"]
W, H, FPS = 1280, 720, 24
PI = math.pi
STOPS = (0, 9, 18, 28, 38, 49, 61, 69)
CUES = (
    "Two solo practitioners trace different arcs. Bruce Lee’s Jeet Kune Do is Dana Edwards’s influence for treating computational thinking as a martial art.",
    "Six positions spell A G C G U U. Pair 1 with 6, 2 with 5, and 3 with 4. Three nested arcs earn three points.",
    "Try the pairs 1–5 and 2–6. Their endpoints alternate. The second, dashed arc crosses the first, so the nesting grammar refuses it.",
    "Allow these crossing pairs. Replay the same proposal and add 3–4. This fold now earns three points too.",
    "The two nested drawings were already expressible. The two crossing drawings are now expressible as well. The best score stays at three.",
    "An auction rule gives the caller or the exchange the same price range. Naming the chooser separates two promises. A sentence and a table can both show who decides.",
    "Choose the form that reveals the mistake you need to see. One personal practice can use several languages."
)
TONES = {
    "light": ("#f8f6ee", "#172e31", "#465b5b", "#9aa7a0", "#cad0c5", "#156860", "#a0402f", "#e3eae0"),
    "dark": ("#101e24", "#f3f0df", "#b5c9c7", "#7d9797", "#3b5051", "#77d5bb", "#f6a283", "#243b3a"),
}
SERIF, SANS, MONO = "Latin Modern Roman", "Noto Sans", "DejaVu Sans Mono"


def rgb(hex_value):
    return tuple(int(hex_value[i:i+2], 16)/255 for i in (1, 3, 5))


def color(c, name, a=1):
    c.set_source_rgba(*rgb(pal[name]), a)


def bound(x):
    return min(1., max(0., x))


def smooth(x):
    x = bound(x)
    return x*x*(3-2*x)


def line(c, points, col, width=2, alpha=1, dash=False):
    if len(points) < 2:
        return
    c.save()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    if dash:
        c.set_dash([10, 10])
    color(c, col, alpha)
    c.set_line_width(width)
    c.move_to(*points[0])
    for p in points[1:]:
        c.line_to(*p)
    c.stroke()
    c.restore()


def circle(c,x,y,r,col,a=1):
    color(c,col,a)
    c.arc(x,y,max(0,r),0,2*PI)
    c.fill()


def font(c,face,size,bold=False,italic=False):
    c.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                       cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)


def label(c,x,y,value,size=28,face=SANS,col="ink",align="left",bold=False,italic=False,a=1):
    font(c,face,size,bold,italic)
    dx,_,width,_,_,_ = c.text_extents(value)
    if align=="center":
        x-=dx+width/2
    elif align=="right":
        x-=dx+width
    color(c,col,a)
    c.move_to(x,y)
    c.show_text(value)


def brush(c, pts, rad, col, alpha=1):
    slopes = [(pts[min(i+1,len(pts)-1)][0]-pts[max(0,i-1)][0],
               pts[min(i+1,len(pts)-1)][1]-pts[max(0,i-1)][1]) for i in range(len(pts))]
    sides = [[],[]]
    for i,((x,y),(dx,dy)) in enumerate(zip(pts, slopes)):
        n=max(0.001,math.hypot(dx,dy))
        r=rad(i/(len(pts)-1))
        for side,sign in zip(sides,(1,-1)):
            side.append((x-sign*dy*r/n,y+sign*dx*r/n))
    p=sides[0]+sides[1][::-1]
    color(c,col,alpha)
    c.move_to(*p[0])
    for xy in p[1:]:
        c.line_to(*xy)
    c.close_path()
    c.fill()


def curve(a,b,d,e,n=40):
    out=[]
    for k in range(n+1):
        u=k/n
        v=1-u
        out.append(tuple(v**3*a[i]+3*v*v*u*b[i]+3*v*u*u*d[i]+u**3*e[i] for i in (0,1)))
    return out


def stroke(c,a,b,d,e,r1,r2,col):
    brush(c,curve(a,b,d,e),lambda u:r1*(1-u)+r2*u,col)


def practice(c, x,y,scale,phase,variant=0):
    # A non-contact exercise. Curves show a hand's path in two bodies.
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    reach = 98 if not variant else 79
    def hand(q):
        ang=-2.58+q*2.35
        return (34+reach*math.cos(ang), 9+69*math.sin(ang))
    q=.12+.82*smooth(phase)
    trail=[hand(.05+(q-.05)*k/64) for k in range(65)]
    brush(c,trail,lambda u:1+3.8*u,"accent" if variant else "teal",.85)
    for step in range(3):
        dot=hand(.05+step*.25)
        circle(c,*dot,2.2,"quiet")
    p=hand(q)
    bend=8*math.sin(q*PI)
    col="ink"
    stroke(c,(-5,57),(-27,79),(-43,120),(-80,140),12,5,col)
    stroke(c,(-80,140),(-90,142),(-95,142),(-101,140),5,2,col)
    stroke(c,(-5,60),(11,78),(29,105),(40,137),14,5,col)
    stroke(c,(40,137),(48,141),(56,141),(63,138),5,2,col)
    stroke(c,(-11,61),(-20,37),(-11,11),(0,-6),16,12,col)
    stroke(c,(-4,-4),(-8,-11),(-8,-11),(-8,-14),7,6,col)
    c.save()
    c.translate(-6,-31);c.rotate(.10);c.scale(.82,1)
    circle(c,0,0,18,col);c.restore()
    stroke(c,(2,0),(15,11),(25,bend),(31,5+bend),7,5,col)
    stroke(c,(31,5+bend),((p[0]+31)/2,p[1]*.2),(p[0]-8,p[1]+5),p,5,2.6,col)
    stroke(c,(-7,5),(-31,20),(-51,31),(-64,24),7,3,col)
    stroke(c,(-64,24),(-71,18),(-77,8),(-81,-1),3,1.5,col)
    circle(c,*p,4.2,"accent" if variant else "teal")
    c.restore()


@lru_cache(None)
def background(theme):
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H)
    c=cairo.Context(surf)
    color(c,"bg");c.paint()
    rng=random.Random(5432)
    for _ in range(14000):
        x,y=rng.uniform(0,W),rng.uniform(0,H)
        c.rectangle(x,y,rng.uniform(.4,1.6),rng.uniform(.4,1.4))
        color(c,"ink",rng.uniform(.012,.05));c.fill()
    return surf


def rule(c,y):
    line(c,[(66,y),(1214,y)],"rule",1)


def header(c,part):
    label(c,68,53,"ZAL   /   DANA EDWARDS",19,MONO,"mute")
    label(c,1212,53,part,19,MONO,"mute","right")
    rule(c,76)


def arc(c,x,y,g,i,j,frac,col,width=6,alpha=1,dash=False):
    if frac <= 0:
        return
    r=(j-i)*g/2
    centre=x+(i-1)*g+r
    pts=[(centre-r*math.cos(PI*frac*k/100),y-.61*r*math.sin(PI*frac*k/100)) for k in range(101)]
    line(c,pts,col,width,alpha,dash)


def strand(c,x,y,g,pairs,progress,colors=None,marks=True,small=False,dashed=()):
    line(c,[(x-g*.22,y),(x+g*5.22,y)],"rule",2)
    colors=colors or ("teal","teal","teal")
    for idx,((i,j),p) in enumerate(zip(pairs,progress)):
        arc(c,x,y,g,i,j,bound(p),colors[idx],3.2 if small else 6,1,idx in dashed)
    for idx,b in enumerate(SEQ):
        px=x+idx*g
        circle(c,px,y,3.8 if small else 6.2,"ink")
        if not small:
            label(c,px,y+48,b,37,MONO,"ink","center")
            if marks: label(c,px,y+78,str(idx+1),19,MONO,"mute","center")
        else:
            label(c,px,y+26,b,20,MONO,"ink","center")


def title(c,head,desc):
    label(c,66,155,head,63,SERIF)
    label(c,69,206,desc,29,SANS,"mute")


def score(c,num,sub,col="teal"):
    line(c,[(902,277),(902,570)],"rule",1.6)
    label(c,958,327,"SCORE",21,MONO,"mute")
    label(c,953,471,str(num),141,SERIF,col)
    label(c,958,524,sub,25,SANS,"mute")


def footer(c,a,b):
    rule(c,610)
    label(c,68,659,a,27,SANS,"ink")
    if b: label(c,1212,658,b,20,MONO,"mute","right")


def intro(c,t):
    header(c,"A FILM ABOUT PERSONAL LANGUAGES")
    label(c,68,172,"Computational",72,SERIF)
    label(c,68,251,"thinking as a",72,SERIF)
    label(c,68,332,"martial art",84,SERIF,"teal",italic=True)
    label(c,73,428,"Two people can learn the same",31)
    label(c,73,475,"movement. Each has to find",31)
    label(c,73,522,"what fits.",31)
    phase=bound((t-.3)/6.5)
    practice(c,775,365,1.22,phase)
    practice(c,1067,370,.98,phase,1)
    footer(c,"Bruce Lee’s Jeet Kune Do shaped how I think about computation.","")


def nested(c,t):
    header(c,"THE FOLD   /   NESTING")
    title(c,"What can six letters earn?","Join compatible letters. Each pair earns one point.")
    frac=[smooth((t-.55-i*1.30)/1.25) for i in range(3)]
    strand(c,123,471,139,EX[0],frac)
    score(c,sum(p>=.999 for p in frac),"points from pairs")
    footer(c,"Each smaller arc fits inside a larger one.","AGCGUU")


def blocked(c,t):
    header(c,"THE FOLD   /   A MISSING ANSWER")
    title(c,"Try drawing this fold.","The first two pairs have alternating endpoints.")
    p1=smooth((t-.2)/1.7);p2=smooth((t-2.15)/1.9)
    strand(c,123,471,139,EX[2],(p1,p2,0),("teal","accent","teal"),dashed=(1,))
    line(c,[(905,282),(905,548)],"rule",1.6)
    label(c,952,336,"RULE",21,MONO,"mute")
    label(c,949,402,"Nesting",53,SERIF)
    label(c,951,447,"only",42,SERIF)
    if t>3.1:
        label(c,951,507,"Crossing refused",26,SANS,"accent",a=smooth((t-3.1)/.55))
    footer(c,"More search time cannot make the dashed arc legal.","1–5   2–6")


def admitted(c,t):
    header(c,"THE FOLD   /   CHANGE THE GRAMMAR")
    title(c,"Let the arcs cross.","Keep the strand and the scoring rule. Change which folds can be written.")
    frac=[1,smooth((t-.4)/1.6),smooth((t-2.65)/1.3)]
    strand(c,123,471,139,EX[2],frac,("teal","accent","teal"))
    score(c,sum(p>=.999 for p in frac),"points from pairs")
    footer(c,"The same proposal now completes. The third pair joins 3 to 4.","")


def gallery(c,t):
    header(c,"THE RESULT   /   ALL WINNING FOLDS")
    title(c,"Same best score. Twice the answers.","Every drawing below uses all six letters and earns three points.")
    for idx,(x,y) in enumerate(((108,381),(108,537),(745,381),(745,537))):
        p=smooth((t-.3-(idx>=2)*2.35)/1.15)
        colors=("teal","accent" if idx==2 else "teal","accent" if idx==3 else "teal")
        strand(c,x,y,63,EX[idx],[p]*3,colors,small=True)
    label(c,108,254,"NESTED",21,MONO,"teal")
    label(c,745,254,"CROSSING",21,MONO,"accent")
    line(c,[(633,239),(633,561)],"rule",1.5)
    footer(c,"The narrow grammar admits two. The wider grammar admits all four.","")


def transfer(c,t):
    header(c,"BACK TO THE PRACTITIONER   /   ZAL")
    title(c,"Who chooses the price?","Both rules allow a price from 10 to 12. Try asking for 12.")
    label(c,74,304,"IN A SENTENCE",21,MONO,"teal")
    label(c,72,380,"The caller chooses.",42,SERIF)
    label(c,72,454,"The exchange chooses.",42,SERIF)
    if t>1:
        p=smooth((t-1)/1.2)
        line(c,[(155,391),(155+99*p,391)],"teal",3)
        line(c,[(155,465),(155+168*p,465)],"accent",3)
    a=smooth((t-2)/.9)
    if a:
        c.push_group()
        label(c,680,304,"IN A TABLE",21,MONO,"teal")
        label(c,680,352,"Who decides?",26,SANS,"mute")
        label(c,932,352,"Can exchange insist?",24,SANS,"mute")
        line(c,[(680,368),(1208,368)],"rule")
        for i,(who,may) in enumerate((("Caller","No"),("Exchange","Yes"))):
            yy=422+i*73
            label(c,680,yy,who,33,SERIF)
            label(c,932,yy,may,33,SERIF,"accent" if i else "teal")
        c.pop_group_to_source();c.paint_with_alpha(a)
    footer(c,"Can the exchange insist on 10? Naming the chooser settles it.","")


def ending(c,t):
    header(c,"A STYLE OF MY OWN")
    label(c,68,194,"What does your",71,SERIF)
    label(c,68,276,"language help",71,SERIF)
    label(c,68,359,"you see?",83,SERIF,"teal",italic=True)
    label(c,72,465,"I can keep the question",32)
    label(c,72,513,"and change the form.",32)
    phase=smooth((t-.3)/5)
    practice(c,868,356,1.43,phase)
    # The drawn line from the opening becomes the model's arcs.
    for idx,(i,j) in enumerate(EX[2]):
        arc(c,729,539,76,i,j,smooth((t-2.2-idx*.45)/1.6),"accent" if idx==1 else "teal",3)
    footer(c,"Computational thinking as a martial art","DANA EDWARDS")


SCENES=(intro,nested,blocked,admitted,gallery,transfer,ending)


def render_frame(theme,t):
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,W,H)
    c=cairo.Context(surf)
    c.set_source_surface(background(theme));c.paint()
    shot=next((i for i in range(len(SCENES)) if t<STOPS[i+1]),len(SCENES)-1)
    local=t-STOPS[shot]
    SCENES[shot](c,local)
    # Short paper dissolves keep consecutive frames legible.
    fade=1-smooth(local/.28) if shot else 0
    if shot!=len(SCENES)-1:
        fade=max(fade,1-smooth((STOPS[shot+1]-t)/.22))
    if fade:
        c.set_source_surface(background(theme));c.paint_with_alpha(fade)
    surf.flush()
    return surf


def as_image(s):
    stream=io.BytesIO()
    s.write_to_png(stream);stream.seek(0)
    return Image.open(stream).convert("RGB")


def render(theme,preview):
    global pal
    pal=dict(zip(("bg","ink","mute","quiet","rule","teal","accent","tint"),TONES[theme]))
    poster=as_image(render_frame(theme,6.6))
    if preview:
        thumb=Image.new("RGB",(960,4*270))
        for i,t in enumerate((6.6,15,24,35,45,57,66)):
            thumb.paste(as_image(render_frame(theme,t)).resize((480,270),Image.Resampling.LANCZOS),
                       (i%2*480,i//2*270))
        thumb.save(preview);return
    poster.save(OUT/f"{STEM}-{theme}.webp",quality=91,method=6)
    args=["ffmpeg","-nostdin","-y","-loglevel","error","-f","rawvideo","-pix_fmt","bgr0",
          "-s",f"{W}x{H}","-r",str(FPS),"-i","-","-an","-c:v","libx264","-threads","3",
          "-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",
          str(OUT/f"{STEM}-{theme}.mp4")]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    with proc.stdin:
        for i in range(STOPS[-1]*FPS):
            surf=render_frame(theme,i/FPS)
            proc.stdin.write(surf.get_data())
    if proc.wait():
        raise RuntimeError("ffmpeg encoding failed")


def stamp(sec):
    return f"00:{sec//60:02d}:{sec%60:02d}.000"


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("theme",choices=TONES)
    parser.add_argument("--preview")
    args=parser.parse_args()
    render(args.theme,args.preview)
    if not args.preview and args.theme=="light":
        vtt="WEBVTT\n\n"+"\n\n".join(f"{stamp(a)} --> {stamp(b)}\n{text}" for a,b,text in zip(STOPS,STOPS[1:],CUES))
        (OUT/f"{STEM}.vtt").write_text(vtt+"\n")
