# 生成内联SVG的小工具：节点+连线+文字，颜色用currentColor以适配深色模式
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
class G:
    def __init__(s,w,h,title): s.w,s.h,s.t,s.el=w,h,title,[]
    def box(s,x,y,t,w=90,h=34,c='#c7000b',sub=None):
        s.el.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="7" fill="none" stroke="{c}" stroke-width="2"/><text x="{x}" y="{y+5 if not sub else y-2}" text-anchor="middle" font-size="13" fill="currentColor">{esc(t)}</text>')
        if sub: s.el.append(f'<text x="{x}" y="{y+12}" text-anchor="middle" font-size="10" fill="#888">{esc(sub)}</text>')
        return s
    def line(s,x1,y1,x2,y2,lab=None,dash=False,c='#888',arrow=False,lx=0,ly=-5):
        d=' stroke-dasharray="5,4"' if dash else ''
        m=' marker-end="url(#ar)"' if arrow else ''
        s.el.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2"{d}{m}/>')
        if lab: s.el.append(f'<text x="{(x1+x2)/2+lx}" y="{(y1+y2)/2+ly}" text-anchor="middle" font-size="11" fill="currentColor">{esc(lab)}</text>')
        return s
    def text(s,x,y,t,size=11,c='currentColor',anchor='middle'):
        s.el.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{c}">{esc(t)}</text>'); return s
    def x(s,x,y): s.el.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="16" fill="#d93025" font-weight="bold">✕</text>'); return s
    def out(s):
        return (f'<figure class="fig"><svg viewBox="0 0 {s.w} {s.h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(s.t)}"><defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#888"/></marker></defs>'+''.join(s.el)+f'</svg><figcaption>{esc(s.t)}</figcaption></figure>')
def seq(title,a,b,msgs,w=520):
    """时序图：msgs=[(dir,'文字')] dir='>' a→b, '<' b→a"""
    h=60+len(msgs)*30; g=G(w,h,title); xa,xb=90,w-90
    g.box(xa,22,a,w=130).box(xb,22,b,w=130)
    g.line(xa,40,xa,h-5,dash=True).line(xb,40,xb,h-5,dash=True)
    for i,(d,t) in enumerate(msgs):
        y=62+i*30
        if d=='>': g.line(xa,y,xb-4,y,t,arrow=True,c='#c7000b')
        else: g.line(xb,y,xa+4,y,t,arrow=True,c='#1a73e8')
    return g.out()
def flow(title,steps,w=640):
    n=len(steps); bw=min(110,(w-20)/n-14); g=G(w,80,title)
    for i,s in enumerate(steps):
        x=10+bw/2+i*(bw+14); g.box(x,40,s,w=bw,h=40)
        if i<n-1: g.line(x+bw/2,40,x+bw/2+12,40,arrow=True)
    return g.out()
