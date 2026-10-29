import json,collections,sys
q=json.load(open('data/questions.json'));k=json.load(open('data/knowledge.json'))
kid={x['id'] for x in k};err=[]
ids=collections.Counter(x['id'] for x in q)
for x in q:
    keys=[o['key'] for o in x['options']]
    for f in ['id','source_url','edition','stage','domain','type','stem','options','answer','explanation','tags','credibility']:
        if f not in x: err.append((x['id'],'缺字段',f))
    if ids[x['id']]>1: err.append((x['id'],'重复id'))
    if x['type'] not in ('判断','单选','多选'): err.append((x['id'],'type'))
    if x['credibility'] not in ('官方','回忆','题库','自编'): err.append((x['id'],'cred'))
    if not x['answer'] or any(a not in keys for a in x['answer']): err.append((x['id'],'答案不在选项'))
    if x['type'] in('判断','单选') and len(x['answer'])!=1: err.append((x['id'],'单答案题多答案'))
    if x['type']=='多选' and len(x['answer'])<2: err.append((x['id'],'多选少于2个答案'))
    if x['type']=='判断' and keys!=['A','B']: err.append((x['id'],'判断选项'))
    if x.get('kp') not in kid: err.append((x['id'],'kp不存在'))
print('errors',err)
print('题目',len(q),collections.Counter(x['credibility'] for x in q),collections.Counter(x['domain'] for x in q),collections.Counter(x['type'] for x in q))
print('知识点',len(k),collections.Counter(x['domain'] for x in k))
sys.exit(1 if err else 0)
