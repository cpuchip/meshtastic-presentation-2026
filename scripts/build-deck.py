"""Render slides/slides.md into a single presentable HTML deck.

Two jobs at once: something Michael can actually read to review the talk, and
something that can BE the talk on the pavilion TV if cpuchip.net is not ready.

Design constraints come from the venue, not taste:
  - A TV is smaller than a projector image and the back row is the constraint,
    so type is large and slides carry few words.
  - No internet at a park pavilion, so no CDN, no web fonts, no JS libraries.
    Images are referenced by relative path, which works from the repo folder.
  - Speaker notes (the *italic* lines in slides.md) are HIDDEN by default and
    toggle with N. They are for Michael, not the room.

Keys:  arrows / space = move   N = notes   F = fullscreen   G = grid overview

Usage: python scripts/build-deck.py   ->  deck/deck.html
"""

import html
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "slides" / "slides.md"
OUT_DIR = ROOT / "deck"
OUT = OUT_DIR / "deck.html"

raw = io.open(SRC, encoding="utf-8").read()
blocks = [b.strip() for b in raw.split("\n---\n")]
# the first block is the file's own preamble, not a slide
blocks = [b for b in blocks if b.strip().startswith("## SLIDE")]

IMG_RE = re.compile(r"^\(?(?:image|photo|wide|\d-up|diagram)\s*:\s*(.+?)\)?$", re.I)


def inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    # [text](url) links, and a literal <br> inside a headline
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = t.replace("&lt;br&gt;", "<br>")
    return t


def unwrap(lines):
    """Join hard-wrapped continuation lines into single logical lines.

    slides.md is written for humans at ~80 columns, so one bullet, one image
    directive or one italic note can span several physical lines. Parsing line
    by line leaks the tail of each onto the slide as stray body text - which is
    exactly what put "of the treeline)" on screen in the first build.
    """
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append("")
            continue
        # A bare "(" only starts a new block when it is an image directive.
        # Otherwise it is a parenthetical continuing the previous line, e.g.
        # "(4.16 volts, still going)" wrapped off the end of a bullet.
        is_directive = bool(IMG_RE.match(s)) and "." in s
        starts_new = (s.startswith(("#", "-", "|", "*")) or is_directive
                      or re.match(r"^\d+\.\s", s))
        prev = out[-1] if out else ""
        if prev:
            unclosed_paren = prev.startswith("(") and prev.count("(") > prev.count(")")
            unclosed_ital = prev.startswith("*") and not prev.rstrip().endswith("*")
            if unclosed_paren or unclosed_ital or not starts_new:
                out[-1] = prev + " " + s
                continue
        out.append(s)
    return out


def render(block):
    lines = unwrap(block.split("\n"))
    label = lines[0].replace("## ", "").strip()
    body, notes, table = [], [], []

    def flush_table():
        if not table:
            return
        rows = [r for r in table if not re.match(r"^\|[\s:|-]+\|$", r)]
        out = ["<table>"]
        for i, r in enumerate(rows):
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            tag = "th" if i == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
        out.append("</table>")
        body.append("\n".join(out))
        table.clear()

    ul = False
    for ln in lines[1:]:
        s = ln.strip()
        if s.startswith("|"):
            table.append(s); continue
        flush_table()
        if not s:
            if ul: body.append("</ul>"); ul = False
            continue
        m = IMG_RE.match(s)
        if m and ("." in m.group(1)):
            if ul: body.append("</ul>"); ul = False
            files = re.findall(r"[\w\-.]+\.(?:webp|png|jpg|svg)", m.group(1))
            if files:
                def tag(f):
                    # A diagram is inlined, not linked: its colours are CSS variables
                    # (see the --sd-* palette below) and an <img> cannot see them.
                    d = ROOT / "assets" / "diagrams" / f
                    if d.is_file():
                        return io.open(d, encoding="utf-8").read()
                    return f'<img src="../assets/images/{f}" alt="">'
                cls = "imgs grid" if len(files) > 4 else ("imgs wide" if s.lower().startswith(("(wide", "wide")) else "imgs")
                body.append(f'<div class="{cls}">' + "".join(tag(f) for f in files) + "</div>")
            else:
                notes.append(inline(s))
            continue
        if s.startswith("# "):
            if ul: body.append("</ul>"); ul = False
            body.append(f"<h1>{inline(s[2:])}</h1>")
        elif s.startswith("### "):
            if ul: body.append("</ul>"); ul = False
            body.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("- "):
            if not ul: body.append("<ul>"); ul = True
            body.append(f"<li>{inline(s[2:])}</li>")
        elif re.match(r"^\d+\.\s", s):
            if not ul: body.append("<ul>"); ul = True
            body.append(f"<li>{inline(re.sub(chr(94)+r'\d+\.\s*','',s))}</li>")
        elif s.startswith("*") and s.endswith("*") and len(s) > 2:
            notes.append(inline(s.strip("*")))
        else:
            if ul: body.append("</ul>"); ul = False
            body.append(f"<p>{inline(s)}</p>")
    if ul: body.append("</ul>")
    flush_table()

    # Lay a single image BESIDE the text rather than above it. Stacked, a
    # headline plus a portrait photo plus four bullets has to shrink a long way
    # to fit; side by side it uses the width a 16:9 screen actually has.
    # Multi-image slides (the 4-up) stay full width, and a slide that is only a
    # picture stays full width too.
    imgs = [b for b in body if b.startswith('<div class="imgs')]
    others = [b for b in body if not b.startswith('<div class="imgs')]
    heads = [b for b in others if b.startswith("<h1>")]
    rest = [b for b in others if not b.startswith("<h1>")]

    single = len(imgs) == 1 and (imgs[0].count("<img") + imgs[0].count("<svg")) == 1 and "imgs wide" not in imgs[0]
    if single and not rest:
        # a picture-only slide (the diagrams) gets the whole stage
        solo = imgs[0].replace('class="imgs"', 'class="imgs solo"', 1)
        body = [solo if b == imgs[0] else b for b in body]
    if single and rest:
        inner = ("".join(heads)
                 + '<div class="split"><div class="col-text">' + "\n".join(rest)
                 + '</div><div class="col-img">' + imgs[0] + "</div></div>")
    else:
        inner = "\n".join(body)

    note_html = ("<div class='notes'>" + "".join(f"<p>{n}</p>" for n in notes) + "</div>") if notes else ""
    return f"<section><div class='label'>{html.escape(label)}</div><div class='content'>" \
           + inner + "</div>" + note_html + "</section>"

slides = "\n".join(render(b) for b in blocks)

CSS = """
*{box-sizing:border-box}
:root{--sd-bg:#111;--sd-text:#f5f5f0;--sd-head:#ff9900;--sd-sub:#ffd479;--sd-muted:rgba(245,245,240,.65);
  --sd-line:rgba(245,245,240,.22);--sd-accent:#ff9c00;--sd-blue:#47a3ff;--sd-green:#3fb950;--sd-red:#e5534b}
html,body{margin:0;height:100%;background:#111;color:#f5f5f0;
  font:400 1.5vw/1.4 "Segoe UI",system-ui,Helvetica,Arial,sans-serif;overflow:hidden}
section{display:none;position:absolute;inset:0;padding:3vh 6vw 8vh;font-size:1.5vw;
  flex-direction:column;justify-content:center;overflow:hidden}
section .content{display:flex;flex-direction:column;justify-content:center;min-height:0;flex:1;overflow:hidden}
section.on{display:flex}
h1{font-size:2.95em;line-height:1.06;margin:0 0 2.2vh;letter-spacing:-.02em}
h3{font-size:1.68em;line-height:1.2;margin:1.6vh 0 .8vh;color:#ffd479}
ul{margin:.6vh 0;padding-left:3vw}
li{font-size:1.40em;margin:.7vh 0}
p{font-size:1.34em;margin:.7vh 0}
b{color:#fff}
code{font-family:Consolas,monospace;font-size:.9em;background:#000;padding:.1em .35em;border-radius:3px}
table{border-collapse:collapse;margin:1.4vh 0;font-size:1.30em}
th,td{border:1px solid #666;padding:.7vh 1.1vw;text-align:left}
th{background:#222;font-size:1.10em;text-transform:uppercase;letter-spacing:.05em}
.imgs{display:flex;gap:1.4vw;justify-content:center;align-items:center;margin:1.6vh 0;min-height:0}
.imgs img{max-height:32vh;max-width:80vw;object-fit:contain;border-radius:6px}
.imgs.solo img,.imgs.solo svg{max-height:62vh;max-width:88vw;width:auto;height:62vh}
.imgs.wide img{max-height:64vh;max-width:88vw}
.imgs.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4vw;justify-items:center;max-width:88vw;margin-left:auto;margin-right:auto}
.imgs.grid img{max-height:24vh;max-width:100%}
.imgs svg{max-width:88vw;height:auto}
.split .col-img svg{max-height:62vh;max-width:100%;height:62vh;width:auto}
a{color:#99ccff}
/* text left, one picture right - uses the width a 16:9 screen actually has */
.split{display:flex;gap:3vw;align-items:center;min-height:0;flex:1}
.split .col-text{flex:1 1 58%;min-width:0}
.split .col-img{flex:0 1 38%;display:flex;align-items:center;justify-content:center;min-height:0}
.split .col-img .imgs{margin:0}
.split .col-img img{max-height:62vh;max-width:100%}
.split ul{padding-left:2vw}
.label{position:absolute;top:1.4vh;left:6vw;font-size:1.1vw;color:#666;letter-spacing:.06em}
.notes{display:none;position:absolute;left:6vw;right:6vw;bottom:5vh;
  border-top:2px solid #ffd479;padding-top:1vh;color:#ffd479;font-size:1.35vw;font-style:italic}
body.notes .notes{display:block}
#bar{position:absolute;bottom:0;left:0;height:5px;background:#ffd479;transition:width .2s}
#num{position:absolute;bottom:1.6vh;right:6vw;font-size:1.2vw;color:#777}
#help{position:absolute;bottom:1.6vh;left:6vw;font-size:1.1vw;color:#555}
body.grid{overflow:auto}
body.grid section{display:block;position:relative;inset:auto;height:32vh;padding:1.5vh 2vw;
  border:1px solid #333;margin:0;overflow:hidden;zoom:.42}
body.grid #bar,body.grid #num,body.grid #help{display:none}
body.grid .notes{display:none}
"""

JS = """
const S=[...document.querySelectorAll('section')];let i=0;
// Shrink a slide's content until it fits. Guessing font sizes per slide is a
// losing game - a headline plus an image plus five bullets will overflow at any
// size that suits a sparse slide. Measuring is the only thing that always works,
// and an overflowing slide on a TV means the room reads a cut-off sentence.
// Scale the SECTION font size so the slide reflows to fit. A transform looked
// right in theory and misaligned everything in practice, because the element
// still occupies its unscaled box. Binary search is overkill-looking and is
// simply the shortest way to land on the largest size that fits.
function fit(sec){
  const c=sec.querySelector('.content'); if(!c) return;
  const base=1.5;                    // vw, matches the CSS
  // Each probe forces a synchronous reflow, so keep the count low. Six steps
  // resolve to ~1% of the range, which is finer than anyone can see. Eleven
  // steps across nine image-load events made the page miss document_idle
  // entirely - a deck that never settles is a deck that stalls on stage.
  let lo=0.5, hi=1.0;
  for(let n=0;n<6;n++){
    const mid=(lo+hi)/2;
    sec.style.fontSize=(base*mid)+'vw';
    const fits = c.scrollHeight<=c.clientHeight+1 && c.scrollWidth<=c.clientWidth+1;
    if(fits) lo=mid; else hi=mid;
  }
  sec.style.fontSize=(base*lo*0.97)+'vw';   // small margin so nothing grazes the edge
}
let pend=0;
function refit(){ if(pend) return; pend=requestAnimationFrame(()=>{pend=0;fit(S[i]);}); }
function show(n){i=Math.max(0,Math.min(S.length-1,n));
  S.forEach((s,k)=>s.classList.toggle('on',k===i));
  fit(S[i]);
  document.getElementById('bar').style.width=((i+1)/S.length*100)+'%';
  document.getElementById('num').textContent=(i+1)+' / '+S.length;
  location.hash=i+1;}
addEventListener('resize',refit);
// An image that has not decoded yet measures as zero height, so the first fit
// on an image slide is computed against the wrong content and comes out too
// large. Re-fit as they land - but coalesced into one frame, not once per image.
document.querySelectorAll('img').forEach(im=>{
  im.addEventListener('load',refit,{once:true});
  im.addEventListener('error',refit,{once:true});
});
addEventListener('load',refit);
addEventListener('keydown',e=>{
  if(document.body.classList.contains('grid')&&e.key!=='g'&&e.key!=='G')return;
  if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){show(i+1);e.preventDefault();}
  else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){show(i-1);e.preventDefault();}
  else if(e.key==='Home')show(0); else if(e.key==='End')show(S.length-1);
  else if(e.key==='n'||e.key==='N')document.body.classList.toggle('notes');
  else if(e.key==='g'||e.key==='G')document.body.classList.toggle('grid');
  else if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
});
addEventListener('click',e=>{if(!document.body.classList.contains('grid'))show(i+(e.clientX>innerWidth/2?1:-1));});
show(parseInt(location.hash.slice(1)||'1')-1);
"""

OUT_DIR.mkdir(exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(
    f"""<!doctype html><meta charset="utf-8">
<title>Off-Grid Communication with Meshtastic</title>
<style>{CSS}</style>
{slides}
<div id="bar"></div><div id="num"></div>
<div id="help">&larr;&rarr; move &middot; N notes &middot; G grid &middot; F fullscreen</div>
<script>{JS}</script>""")

print(f"built {OUT.relative_to(ROOT)}  -  {len(blocks)} slides")
print("open it in Chrome, press F for fullscreen, N for speaker notes, G for a grid overview")
print("offline-safe: no CDN, no web fonts. Images load by relative path from assets/images/.")
