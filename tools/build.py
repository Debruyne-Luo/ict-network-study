import json,sys
sys.path.insert(0,'.')
from h import KPS
import kp_dt, kp_other
from real import R
qs=[];kps=[]
for k in KPS:
    for i,(t,stem,opts,ans,exp) in enumerate(k['qs'],1):
        qs.append(dict(id=f"self-{k['id']}-{i}",source_url='',edition='',stage='自编练习',domain=k['domain'],type=t,stem=stem,
          options=[dict(key=c,text=o) for c,o in zip('ABCDEFG',opts)],answer=list(ans),explanation=exp,tags=[k['title']],credibility='自编',kp=k['id']))
    kk={x:k[x] for x in k if x!='qs'}; kps.append(kk)
allq=R+qs
json.dump(kps,open('../data/knowledge.json','w'),ensure_ascii=False,indent=1)
json.dump(allq,open('../data/questions.json','w'),ensure_ascii=False,indent=1)
open('../js/data.js','w').write('// 自动生成：python3 tools/build.py\nwindow.KPS='+json.dumps(kps,ensure_ascii=False)+';\nwindow.QUESTIONS='+json.dumps(allq,ensure_ascii=False)+';\n')
print(len(kps),len(allq))
