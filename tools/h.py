KPS=[]
def J(stem,ans,exp): return ('判断',stem,['正确','错误'],'A' if ans else 'B',exp)
def S(stem,opts,ans,exp): return ('单选',stem,opts,ans,exp)
def M(stem,opts,ans,exp): return ('多选',stem,opts,ans,exp)
def kp(id,domain,day,title,summary,points,pitfalls,commands,qs,todo=None):
    KPS.append(dict(id=id,domain=domain,day=day,title=title,summary=summary,points=points,pitfalls=pitfalls,commands=commands,todo=todo or [],qs=qs))
