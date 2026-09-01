from pathlib import Path
from PIL import Image, ImageDraw
import math, os, shutil, subprocess

SCRIPT = Path(__file__).resolve()
if SCRIPT.parent.name == "source" and SCRIPT.parent.parent.name == "slackworld-cursor-theme":
    PKG = SCRIPT.parent.parent
else:
    PKG = SCRIPT.parents[1] / "outputs" / "slackworld-cursor-theme"
THEME = PKG / "Slackworld"
SRC = PKG / "source"
PNG = SRC / "png"
CONF = SRC / "config"
CUR = THEME / "cursors"
SIZES = (16, 24, 32, 48, 64)
AA = 4

NAVY = "#07131f"
WHITE = "#f4f8fb"
ACCENT = "#587990"
LIGHT = "#b7d2e5"
SHADOW = "#03101a88"
RED = "#c85d68"

for p in (PNG, CONF, CUR):
    p.mkdir(parents=True, exist_ok=True)

def C(hexv):
    hexv = hexv.lstrip("#")
    if len(hexv) == 6: hexv += "ff"
    return tuple(int(hexv[i:i+2], 16) for i in (0,2,4,6))

def canvas(size):
    return Image.new("RGBA", (size*AA, size*AA), (0,0,0,0)), ImageDraw.Draw(Image.new("RGBA", (1,1)))

def draw_scaled(size, fn):
    # Draw once on a high-resolution 32-unit design grid.  Every exported
    # Xcursor image still has its own native pixel size, while the geometry
    # remains identical and unclipped from 16 through 64 pixels.
    design_size = 32 * AA
    im = Image.new("RGBA", (design_size, design_size), (0,0,0,0))
    d = ImageDraw.Draw(im)
    fn(d, design_size, AA)
    return im.resize((size,size), Image.Resampling.LANCZOS)

def line(d, pts, fill, width, joint="curve"):
    d.line(pts, fill=C(fill), width=width, joint=joint)

def arrow_draw(d, n, s, badge=None):
    pts=[(2*s,1*s),(2*s,25*s),(8*s,19*s),(13*s,30*s),(18*s,27*s),(13*s,17*s),(23*s,17*s)]
    shadow=[(x+2*s,y+2*s) for x,y in pts]
    d.polygon(shadow, fill=C(SHADOW))
    d.polygon(pts, fill=C(WHITE), outline=C(NAVY), width=max(1,2*s))
    line(d, pts+[pts[0]], NAVY, max(1,2*s))
    if badge:
        bx,by,r=22*s,23*s,7*s
        d.ellipse((bx-r,by-r,bx+r,by+r), fill=C(ACCENT if badge!="no" else RED), outline=C(NAVY), width=2*s)
        if badge=="copy":
            line(d,[(bx-r//2,by),(bx+r//2,by)],WHITE,2*s); line(d,[(bx,by-r//2),(bx,by+r//2)],WHITE,2*s)
        elif badge=="link":
            line(d,[(bx-4*s,by+2*s),(bx-1*s,by-2*s),(bx+2*s,by+1*s),(bx+5*s,by-3*s)],WHITE,2*s)
        elif badge=="help":
            # compact question mark
            line(d,[(bx-3*s,by-3*s),(bx,by-5*s),(bx+3*s,by-3*s),(bx+2*s,by),(bx,by+2*s)],WHITE,2*s)
            d.ellipse((bx-s,by+4*s,bx+s,by+6*s),fill=C(WHITE))
        elif badge=="no":
            line(d,[(bx-4*s,by-4*s),(bx+4*s,by+4*s)],WHITE,2*s)

def ibeam_draw(d,n,s,vertical=False):
    if vertical:
        line(d,[(6*s,16*s),(26*s,16*s)],NAVY,6*s); line(d,[(8*s,16*s),(24*s,16*s)],WHITE,2*s)
        line(d,[(7*s,11*s),(7*s,21*s)],NAVY,3*s); line(d,[(25*s,11*s),(25*s,21*s)],NAVY,3*s)
    else:
        line(d,[(16*s,5*s),(16*s,27*s)],NAVY,6*s); line(d,[(16*s,7*s),(16*s,25*s)],WHITE,2*s)
        line(d,[(11*s,6*s),(21*s,6*s)],NAVY,3*s); line(d,[(11*s,26*s),(21*s,26*s)],NAVY,3*s)

def cross_draw(d,n,s):
    line(d,[(16*s,4*s),(16*s,28*s)],NAVY,6*s); line(d,[(4*s,16*s),(28*s,16*s)],NAVY,6*s)
    line(d,[(16*s,6*s),(16*s,26*s)],WHITE,2*s); line(d,[(6*s,16*s),(26*s,16*s)],WHITE,2*s)

def resize_draw(d,n,s,kind):
    vectors={"ew":((4,16),(28,16)),"ns":((16,4),(16,28)),"nwse":((6,6),(26,26)),"nesw":((26,6),(6,26))}
    a,b=vectors[kind]
    line(d,[(a[0]*s,a[1]*s),(b[0]*s,b[1]*s)],NAVY,7*s)
    line(d,[(a[0]*s,a[1]*s),(b[0]*s,b[1]*s)],WHITE,3*s)
    ang=math.atan2(b[1]-a[1],b[0]-a[0])
    for p,rev in ((a,0),(b,math.pi)):
        base=ang+rev
        q1=(int((p[0]+7*math.cos(base+.65))*s),int((p[1]+7*math.sin(base+.65))*s))
        q2=(int((p[0]+7*math.cos(base-.65))*s),int((p[1]+7*math.sin(base-.65))*s))
        line(d,[(p[0]*s,p[1]*s),q1],NAVY,7*s); line(d,[(p[0]*s,p[1]*s),q2],NAVY,7*s)
        line(d,[(p[0]*s,p[1]*s),q1],WHITE,3*s); line(d,[(p[0]*s,p[1]*s),q2],WHITE,3*s)

def move_draw(d,n,s):
    resize_draw(d,n,s,"ew"); resize_draw(d,n,s,"ns")

def hand_draw(d,n,s,closed=False):
    # Readable modern pointing hand, deliberately simplified for 16 px.
    if closed:
        pts=[(8,14),(11,11),(13,12),(14,8),(17,8),(18,11),(20,9),(23,10),(24,14),(24,22),(20,28),(12,27),(8,21)]
    else:
        pts=[(8,15),(11,13),(13,15),(13,5),(16,4),(18,6),(18,12),(20,10),(23,11),(24,15),(24,22),(20,28),(12,27),(8,21)]
    pts=[(x*s,y*s) for x,y in pts]
    d.polygon([(x+2*s,y+2*s) for x,y in pts],fill=C(SHADOW))
    d.polygon(pts,fill=C(WHITE),outline=C(NAVY),width=2*s)
    line(d,pts+[pts[0]],NAVY,2*s)

def no_draw(d,n,s):
    d.ellipse((5*s,5*s,27*s,27*s),fill=C(WHITE),outline=C(NAVY),width=3*s)
    d.ellipse((8*s,8*s,24*s,24*s),fill=C(RED))
    line(d,[(9*s,23*s),(23*s,9*s)],WHITE,4*s)

def zoom_draw(d,n,s,minus=False):
    d.ellipse((4*s,4*s,21*s,21*s),fill=C(WHITE),outline=C(NAVY),width=3*s)
    line(d,[(19*s,19*s),(28*s,28*s)],NAVY,6*s); line(d,[(19*s,19*s),(28*s,28*s)],WHITE,2*s)
    line(d,[(9*s,13*s),(17*s,13*s)],ACCENT,3*s)
    if not minus: line(d,[(13*s,9*s),(13*s,17*s)],ACCENT,3*s)

def cell_draw(d,n,s):
    cross_draw(d,n,s)
    d.rectangle((11*s,11*s,21*s,21*s),fill=C(ACCENT),outline=C(NAVY),width=2*s)

def context_draw(d,n,s):
    arrow_draw(d,n,s)
    for j in range(3):
        d.rounded_rectangle((19*s,(18+j*4)*s,30*s,(20+j*4)*s),radius=s,fill=C(LIGHT),outline=C(NAVY),width=s)

def spinner_draw(d,n,s,frame,with_arrow=False):
    if with_arrow: arrow_draw(d,n,s)
    cx,cy=(23*s,23*s) if with_arrow else (16*s,16*s)
    r=7*s if with_arrow else 10*s
    for i in range(12):
        a=2*math.pi*i/12-math.pi/2
        alpha=int(45+210*((i-frame)%12)/11)
        x1=cx+int(math.cos(a)*(r-3*s)); y1=cy+int(math.sin(a)*(r-3*s))
        x2=cx+int(math.cos(a)*r); y2=cy+int(math.sin(a)*r)
        d.line((x1,y1,x2,y2),fill=(*C(LIGHT)[:3],alpha),width=max(1,2*s))

STATIC={
    "arrow":lambda d,n,s:arrow_draw(d,n,s), "hand":lambda d,n,s:hand_draw(d,n,s),
    "grabbing":lambda d,n,s:hand_draw(d,n,s,True), "text":lambda d,n,s:ibeam_draw(d,n,s),
    "vertical_text":lambda d,n,s:ibeam_draw(d,n,s,True), "crosshair":cross_draw,
    "move":move_draw, "ew_resize":lambda d,n,s:resize_draw(d,n,s,"ew"),
    "ns_resize":lambda d,n,s:resize_draw(d,n,s,"ns"), "nwse_resize":lambda d,n,s:resize_draw(d,n,s,"nwse"),
    "nesw_resize":lambda d,n,s:resize_draw(d,n,s,"nesw"), "copy":lambda d,n,s:arrow_draw(d,n,s,"copy"),
    "link":lambda d,n,s:arrow_draw(d,n,s,"link"), "help":lambda d,n,s:arrow_draw(d,n,s,"help"),
    "not_allowed":no_draw, "zoom_in":lambda d,n,s:zoom_draw(d,n,s),
    "zoom_out":lambda d,n,s:zoom_draw(d,n,s,True), "cell":cell_draw, "context_menu":context_draw,
}

HOT={"arrow":(2,2),"hand":(10,5),"grabbing":(14,13),"text":(16,16),"vertical_text":(16,16),
     "crosshair":(16,16),"move":(16,16),"ew_resize":(16,16),"ns_resize":(16,16),
     "nwse_resize":(16,16),"nesw_resize":(16,16),"copy":(2,2),"link":(2,2),"help":(2,2),
     "not_allowed":(16,16),"zoom_in":(11,11),"zoom_out":(11,11),"cell":(16,16),"context_menu":(2,2)}

def scaled_hot(name,size):
    x,y=HOT[name]
    return max(0,round(x*size/32)),max(0,round(y*size/32))

for name, painter in STATIC.items():
    lines=[]
    for size in SIZES:
        path=PNG/f"{name}-{size}.png"
        draw_scaled(size,painter).save(path,optimize=True)
        x,y=scaled_hot(name,size)
        lines.append(f"{size} {x} {y} ../png/{path.name}")
    (CONF/f"{name}.conf").write_text("\n".join(lines)+"\n")

for name, with_arrow in (("wait",False),("progress",True)):
    lines=[]
    for size in SIZES:
        for frame in range(12):
            path=PNG/f"{name}-{size}-{frame:02}.png"
            draw_scaled(size,lambda d,n,s,f=frame,a=with_arrow:spinner_draw(d,n,s,f,a)).save(path,optimize=True)
            if with_arrow: x,y=max(1,round(size/16)),max(1,round(size/16))
            else: x=y=round(size/2)
            lines.append(f"{size} {x} {y} ../png/{path.name} 75")
    (CONF/f"{name}.conf").write_text("\n".join(lines)+"\n")

for conf in sorted(CONF.glob("*.conf")):
    subprocess.run(
        ["xcursorgen", conf.name, str(CUR / conf.stem)],
        check=True,
        cwd=CONF,
    )

ALIASES={
 "default":"arrow","left_ptr":"arrow","arrow":"arrow","top_left_arrow":"arrow","right_ptr":"arrow",
 "pointer":"hand","hand":"hand","hand1":"hand","hand2":"hand","openhand":"hand","grab":"hand",
 "closedhand":"grabbing","grabbing":"grabbing","xterm":"text","ibeam":"text","text":"text",
 "vertical-text":"vertical_text","cross":"crosshair","cross_reverse":"crosshair","tcross":"crosshair",
 "plus":"crosshair","crosshair":"crosshair","fleur":"move","all-scroll":"move","move":"move",
 "size_hor":"ew_resize","h_double_arrow":"ew_resize","sb_h_double_arrow":"ew_resize","col-resize":"ew_resize",
 "ew-resize":"ew_resize","left_side":"ew_resize","right_side":"ew_resize","sb_left_arrow":"ew_resize","sb_right_arrow":"ew_resize",
 "size_ver":"ns_resize","v_double_arrow":"ns_resize","sb_v_double_arrow":"ns_resize","row-resize":"ns_resize",
 "ns-resize":"ns_resize","top_side":"ns_resize","bottom_side":"ns_resize","sb_up_arrow":"ns_resize","sb_down_arrow":"ns_resize",
 "size_fdiag":"nwse_resize","bd_double_arrow":"nwse_resize","nwse-resize":"nwse_resize","top_left_corner":"nwse_resize","bottom_right_corner":"nwse_resize",
 "size_bdiag":"nesw_resize","fd_double_arrow":"nesw_resize","nesw-resize":"nesw_resize","top_right_corner":"nesw_resize","bottom_left_corner":"nesw_resize",
 "copy":"copy","dnd-copy":"copy","alias":"link","link":"link","dnd-link":"link","question_arrow":"help","help":"help",
 "crossed_circle":"not_allowed","not-allowed":"not_allowed","no-drop":"not_allowed","forbidden":"not_allowed","X_cursor":"not_allowed","pirate":"not_allowed",
 "zoom-in":"zoom_in","zoom-out":"zoom_out","cell":"cell","context-menu":"context_menu",
 "watch":"wait","wait":"wait","left_ptr_watch":"progress","progress":"progress",
 "center_ptr":"arrow","draft_large":"arrow","draft_small":"arrow",
 "base_arrow_up":"ns_resize","base_arrow_down":"ns_resize","based_arrow_up":"ns_resize","based_arrow_down":"ns_resize","double_arrow":"ns_resize",
 "ll_angle":"nesw_resize","lr_angle":"nwse_resize","ul_angle":"nwse_resize","ur_angle":"nesw_resize",
 "circle":"not_allowed","dnd-none":"not_allowed","dnd-move":"move","dnd-ask":"help",
}

HASHES={
 "00008160000006810000408080010102":"ns_resize","028006030e0e7ebffc7f7070c0600140":"ew_resize",
 "03b6e0fcb3499374a867c041f52298f0":"not_allowed","08e8e1c95fe2fc01f976f1e063a24ccd":"progress",
 "14fef782d02440884392942c11205230":"ew_resize","2870a09082c103050810ffdffffe0204":"ns_resize",
 "3085a0e285430894940527032f8b26df":"link","3ecb610c1bf2410f44200f48c40d3599":"progress",
 "4498f0e0c1937ffe01fd06f973665830":"move","5c6cd98b3f3ebcb1f9c7f1c204630408":"help",
 "6407b0e94181790501fd1e167b474872":"copy","640fb0e74195791501fd1ed57b41487f":"link",
 "9081237383d90e509aa00f00170e968f":"move","9d800788f1b08800ae810202380a0822":"hand",
 "c7088f0f3e6c8088236ef8e1e3e70000":"nwse_resize","d9ce0ab605698f320427677b458ad60b":"help",
 "e29285e634086352946a0e7090d73106":"hand","fcf1c3c7cd4491d801f1e1c78f100000":"nesw_resize",
}

for alias,target in {**ALIASES,**HASHES}.items():
    if alias == target:
        continue
    p=CUR/alias
    if p.exists() or p.is_symlink(): p.unlink()
    os.symlink(target,p)

(THEME/"index.theme").write_text("""[Icon Theme]\nName=Slackworld\nComment=Modern Slackware cursor theme\nExample=left_ptr\nInherits=Adwaita\n""")
(THEME/"cursor.theme").write_text("""[Icon Theme]\nName=Slackworld\nInherits=Adwaita\n""")

# Contact sheets for visual QA at each native size.
order=["arrow","hand","grabbing","text","vertical_text","crosshair","move","ew_resize","ns_resize",
       "nwse_resize","nesw_resize","copy","link","help","not_allowed","zoom_in","zoom_out","cell","context_menu","wait","progress"]
for size in SIZES:
    cell=max(96,size+46); cols=7; rows=3
    sheet=Image.new("RGB",(cell*cols,cell*rows),C("#294f75")[:3]); d=ImageDraw.Draw(sheet)
    for i,name in enumerate(order):
        suffix=f"-{size}-00.png" if name in ("wait","progress") else f"-{size}.png"
        im=Image.open(PNG/f"{name}{suffix}")
        x=(i%cols)*cell+(cell-size)//2; y=(i//cols)*cell+24
        sheet.paste(im,(x,y),im); d.text(((i%cols)*cell+4,(i//cols)*cell+5),name,fill="white")
    sheet.save(PKG/f"preview-{size}.png",optimize=True)

builder_copy = SRC / "build_slackworld_cursor.py"
if SCRIPT != builder_copy:
    shutil.copy2(SCRIPT, builder_copy)
print(THEME)
