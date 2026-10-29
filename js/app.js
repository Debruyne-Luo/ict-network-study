(function(){
'use strict';
var KPS=window.KPS||[],QS=window.QUESTIONS||[];
var DOMAINS=['数通','DCN','安全','WLAN'],QUOTA={'数通':24,'DCN':12,'安全':12,'WLAN':12};
var EXAM=new Date(2026,10,14,9,0,0),START=new Date(2026,9,29);
var PLAN=[
['10/29','网络分层、TCP/UDP、IP与子网划分',['dt-osi','dt-tcpudp','dt-ip'],'子网划分题反复算，直到不用草稿也能算出/26、/27'],
['10/30','ARP、华为命令行、VLAN',['dt-arp','dt-vrp','dt-vlan'],'有条件装eNSP，敲一遍VLAN配置'],
['10/31','STP、RSTP/MSTP、链路聚合',['dt-stp','dt-rstp','dt-trunk'],'画一张小拓扑手算根桥/根端口'],
['11/01','路由基础、静态路由、VRRP',['dt-route','dt-vrrp'],'背默认优先级表；做VRRP真题'],
['11/02','OSPF',['dt-ospf1','dt-ospf2'],'记住邻居7个状态和LSA 1/2/3/5/7类'],
['11/03','BGP与路由策略',['dt-bgp1','dt-bgp2','dt-policy'],'背BGP选路顺序；会算ip-prefix题'],
['11/04','ACL、NAT、DHCP',['dt-acl','dt-nat','dt-dhcp'],'数通前半部分错题复盘'],
['11/05','IPv6、MPLS VPN、拓展(SRv6/组播/FRR)',['dt-ipv6','dt-mplsvpn','dt-ext'],'数通全部知识点刷一遍，正确率>70%再往下'],
['11/06','防火墙：安全区域、安全策略、NAT、vsys、URPF',['sec-zone','sec-policy','sec-nat','sec-vsys','sec-urpf'],'区分“转换前/后地址”'],
['11/07','IPSec、SSL VPN、攻击防范、云安全',['sec-ipsec','sec-ssl','sec-attack','sec-cloud'],'背IPSec配置六步'],
['11/08','WLAN基础、CAPWAP、组网转发、配置模板',['wl-basic','wl-capwap','wl-net','wl-profile'],'画出模板引用关系图'],
['11/09','AC备份、认证、漫游、Wi-Fi 6、射频优化',['wl-backup','wl-auth','wl-roam','wl-wifi6','wl-rf'],'对比冷备/热备/N+1'],
['11/10','DCN：Spine-Leaf、VXLAN、EVPN、M-LAG、堆叠、ECMP、PFC',['dc-arch','dc-vxlan','dc-evpn','dc-mlag','dc-stack','dc-ecmp','dc-lossless'],'记端口号：4789、4791、5246/5247'],
['11/11','模拟考①＋错题复盘',[],'60题/60分钟完整做一套，按知识点复盘错题'],
['11/12','模拟考②＋薄弱点回炉',[],'看“统计”页最薄弱的3个知识点，重读讲义'],
['11/13','模拟考③＋考前检查',[],'确认考试平台、账号、网络、摄像头等要求（以组委会通知为准）'],
['11/14','考试日',[],'放松，按时登录。理论考试时间以本省通知为准(11/14–15)']];
// storage
var S={get:function(k,d){try{var v=localStorage.getItem('ict_'+k);return v?JSON.parse(v):d}catch(e){return d}},set:function(k,v){try{localStorage.setItem('ict_'+k,JSON.stringify(v))}catch(e){}}};
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function kpById(id){for(var i=0;i<KPS.length;i++)if(KPS[i].id===id)return KPS[i];return null}
function qById(id){for(var i=0;i<QS.length;i++)if(QS[i].id===id)return QS[i];return null}
function ymd(d){return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate()}
function todayIdx(){var t=new Date();t.setHours(0,0,0,0);var i=Math.round((t-START)/864e5);return i}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var x=a[i];a[i]=a[j];a[j]=x}return a}
function sameAns(a,b){return a.slice().sort().join('')===b.slice().sort().join('')}
function record(q,ok){var st=S.get('stat',{});var s=st[q.id]||{n:0,ok:0};s.n++;if(ok)s.ok++;st[q.id]=s;S.set('stat',st);
 var w=S.get('wrong',{}),ws=S.get('wstreak',{});if(!ok){w[q.id]=(w[q.id]||0)+1;ws[q.id]=0}else if(w[q.id]){ws[q.id]=(ws[q.id]||0)+1;if(ws[q.id]>=2){delete w[q.id];delete ws[q.id]}}S.set('wrong',w);S.set('wstreak',ws);checkin()}
function checkin(){var c=S.get('checkin',{});c[ymd(new Date())]=true;S.set('checkin',c)}
function toggleFav(id){var f=S.get('fav',{});if(f[id])delete f[id];else f[id]=1;S.set('fav',f);return !!f[id]}
var app=document.getElementById('app');
// question renderer (practice mode)
function renderQ(q,idx,opts){opts=opts||{};var fav=S.get('fav',{})[q.id];
 var h='<div class="card q" data-id="'+q.id+'"><div class="mut">'+(idx!=null?('第'+(idx+1)+'题 · '):'')+'<span class="tag">'+q.domain+'</span><span class="tag">'+q.type+'</span><span class="tag c-'+q.credibility+'">'+q.credibility+'</span>'+(q.stage?'<span class="tag">'+esc(q.edition+' '+q.stage)+'</span>':'')+'</div>';
 h+='<p><b>'+esc(q.stem)+'</b></p>';
 q.options.forEach(function(o){h+='<label class="opt" data-k="'+o.key+'">'+o.key+'. '+esc(o.text)+'</label>'});
 if(!opts.exam){h+='<button class="btn sub">提交</button><button class="btn o favb">'+(fav?'★ 已收藏':'☆ 收藏')+'</button>';if(opts.removable)h+='<button class="btn o rm">移出错题本</button>';h+='<div class="res"></div>'}
 return h+'</div>'}
function bindQ(root,onAnswer){root.querySelectorAll('.q').forEach(function(el){var q=qById(el.dataset.id),sel=[],done=false;
 el.querySelectorAll('.opt').forEach(function(o){o.onclick=function(){if(done)return;var k=o.dataset.k;
  if(q.type==='多选'){var i=sel.indexOf(k);if(i>=0)sel.splice(i,1);else sel.push(k)}else sel=[k];
  el.querySelectorAll('.opt').forEach(function(x){x.classList.toggle('sel',sel.indexOf(x.dataset.k)>=0)});if(onAnswer)onAnswer(q,sel)}});
 var sb=el.querySelector('.sub');if(sb)sb.onclick=function(){if(!sel.length||done)return;done=true;var ok=sameAns(sel,q.answer);record(q,ok);
  el.querySelectorAll('.opt').forEach(function(x){var k=x.dataset.k;if(q.answer.indexOf(k)>=0)x.classList.add('right');else if(sel.indexOf(k)>=0)x.classList.add('wrong')});
  var kp=kpById(q.kp);el.querySelector('.res').innerHTML='<div class="exp"><b style="color:var('+(ok?'--ok':'--bad')+')">'+(ok?'✔ 回答正确':'✘ 回答错误')+'</b>　正确答案：'+q.answer.join('')+'<br>'+esc(q.explanation)+(kp?'<br><a href="#kp/'+kp.id+'">→ 复习知识点：'+esc(kp.title)+'</a>':'')+(q.source_url?'<br><span class="mut">来源：<a target="_blank" href="'+esc(q.source_url)+'">'+esc(q.source_url)+'</a></span>':'')+'</div>';sb.disabled=true};
 var fb=el.querySelector('.favb');if(fb)fb.onclick=function(){fb.textContent=toggleFav(q.id)?'★ 已收藏':'☆ 收藏'};
 var rm=el.querySelector('.rm');if(rm)rm.onclick=function(){var w=S.get('wrong',{});delete w[q.id];S.set('wrong',w);el.remove()}})}
// pages
var P={};
P.cards=function(){app.innerHTML=window.CARDS_HTML||'速记卡加载失败'};
P.home=function(){var now=new Date(),ms=EXAM-now,d=Math.max(0,Math.ceil(ms/864e5));var ti=todayIdx(),done=S.get('days',{}),nd=Object.keys(done).length;
 var lk=S.get('learned',{}),nl=Object.keys(lk).length,ci=S.get('checkin',{});
 var h='<div class="grid"><div class="card"><div class="mut">距 11月14日 省资格赛理论</div><div class="big">'+(ms>0?d+' 天':'已开考')+'</div><div class="mut" id="cd"></div></div>';
 h+='<div class="card"><div class="mut">计划完成</div><div class="big">'+nd+'/17</div><div class="bar"><i style="width:'+(nd/17*100)+'%"></i></div></div>';
 h+='<div class="card"><div class="mut">知识点已学</div><div class="big">'+nl+'/'+KPS.length+'</div><div class="bar"><i style="width:'+(nl/KPS.length*100)+'%"></i></div></div>';
 h+='<div class="card"><div class="mut">累计打卡</div><div class="big">'+Object.keys(ci).length+' 天</div><button class="btn" id="ck">'+(ci[ymd(now)]?'今日已打卡 ✔':'今日打卡')+'</button></div></div>';
 var i=Math.min(Math.max(ti,0),16),p=PLAN[i];
 h+='<div class="card today"><h3>'+(ti<0?'即将开始 · 第1天':ti>16?'考试已结束':'今日任务 · 第'+(i+1)+'天')+'（'+p[0]+'）</h3><p><b>'+p[1]+'</b></p><p class="mut">'+p[3]+'</p>';
 p[2].forEach(function(id){var k=kpById(id);h+='<a class="btn o" href="#kp/'+id+'">'+(lk[id]?'✔ ':'')+esc(k.title)+'</a>'});
 if(p[2].length)h+='<br><a class="btn" href="#practice/day'+i+'">练习今日知识点题目</a>';else if(i<16)h+='<br><a class="btn" href="#mock">开始模拟考</a>';
 h+='<label style="display:block;margin-top:8px"><input type="checkbox" id="dd" '+(done[i]?'checked':'')+'> 标记今天的计划已完成</label></div>';
 h+='<div class="card"><b>题库</b>：共 '+QS.length+' 题（'+cnt(QS,'credibility')+'）。<span class="mut">“回忆”为网友回忆真题，“自编”为本站基于讲义自编的巩固题，不是真题。</span></div>';
 app.innerHTML=h;
 document.getElementById('ck').onclick=function(){checkin();route()};
 document.getElementById('dd').onchange=function(){var d=S.get('days',{});if(this.checked)d[i]=1;else delete d[i];S.set('days',d);route()};
 var cd=document.getElementById('cd');function tick(){var m=EXAM-new Date();if(m<0){cd.textContent='';return}cd.textContent=Math.floor(m/864e5)+'天'+Math.floor(m/36e5%24)+'时'+Math.floor(m/6e4%60)+'分'+Math.floor(m/1e3%60)+'秒（按11/14 09:00估算，具体场次以通知为准）'}tick();clearInterval(window._t);window._t=setInterval(function(){if(document.getElementById('cd'))tick();else clearInterval(window._t)},1000)};
function cnt(arr,f){var c={};arr.forEach(function(x){c[x[f]]=(c[x[f]]||0)+1});return Object.keys(c).map(function(k){return k+' '+c[k]}).join('，')}
P.plan=function(){var done=S.get('days',{}),ti=todayIdx(),h='<div class="card"><h2>17天计划（10/29–11/14）</h2><p class="mut">每天2–4小时：约60%看讲义、40%刷题。勾选保存在本浏览器。</p><table><tr><th>天</th><th>日期</th><th>内容</th><th>完成</th></tr>';
 PLAN.forEach(function(p,i){h+='<tr class="'+(i===ti?'today':'')+(done[i]?' done':'')+'"><td>'+(i+1)+'</td><td>'+p[0]+'</td><td>'+esc(p[1])+'<br>'+p[2].map(function(id){return '<a href="#kp/'+id+'">'+esc(kpById(id).title)+'</a>'}).join(' · ')+'<div class="mut">'+esc(p[3])+'</div></td><td><input type="checkbox" data-i="'+i+'" '+(done[i]?'checked':'')+'></td></tr>'});
 app.innerHTML=h+'</table></div>';app.querySelectorAll('input[data-i]').forEach(function(c){c.onchange=function(){var d=S.get('days',{});if(c.checked)d[c.dataset.i]=1;else delete d[c.dataset.i];S.set('days',d);route()}})};
P.learn=function(){var lk=S.get('learned',{}),h='<div class="card"><input id="ks" class="search" placeholder="🔍 搜索知识点（如 OSPF、VRRP、5246、Option 43、安全组）"><div id="kr"></div></div>';var pct={'数通':'40%','DCN':'20%','安全':'20%','WLAN':'20%'};
 DOMAINS.forEach(function(d){var ks=KPS.filter(function(k){return k.domain===d});h+='<div class="card"><h2>'+d+' <span class="mut">（占比约'+pct[d]+'，'+ks.length+'个知识点）</span></h2>';
  ks.forEach(function(k){h+='<div><a href="#kp/'+k.id+'">'+(lk[k.id]?'✔ ':'○ ')+esc(k.title)+'</a> <span class="mut">第'+k.day+'天 · '+esc(k.summary)+'</span></div>'});h+='</div>'});app.innerHTML=h;var ks=document.getElementById('ks'),kr=document.getElementById('kr');ks.oninput=function(){var v=ks.value.trim().toLowerCase();if(!v){kr.innerHTML='';return}
 var r=KPS.map(function(k){var d=k.deep||{},t=[k.title,k.summary,k.points.join(' '),k.pitfalls.join(' '),k.commands.join(' '),d.intro||'',(d.steps||[]).join(' '),d.example||'',d.table?JSON.stringify(d.table):''].join(' ').toLowerCase();var sc=(k.title.toLowerCase().indexOf(v)>=0?10:0)+t.split(v).length-1;return [k,sc]}).filter(function(x){return x[1]>0}).sort(function(a,b){return b[1]-a[1]});
 kr.innerHTML=r.length?r.map(function(x){return '<div><a href="#kp/'+x[0].id+'">'+esc(x[0].title)+'</a> <span class="tag">'+x[0].domain+'</span> <span class="mut">命中'+x[1]+'处</span></div>'}).join(''):'<p class="mut">没有找到，换个关键词试试</p>'}};
P.kp=function(id){var k=kpById(id);if(!k){app.innerHTML='未找到';return}var lk=S.get('learned',{});
 var h='<div class="card"><a href="#learn">← 讲义目录</a><h2>'+esc(k.title)+' <span class="tag">'+k.domain+'</span></h2><p class="exp"><b>一句话：</b>'+esc(k.summary)+'</p><h3>要点</h3><ul>'+k.points.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul>';
 var D=k.deep;if(D){var dh='<h3>📖 通俗理解（零基础先读）</h3><p class="intro">'+esc(D.intro)+'</p>';
  if(D.svg)dh+='<h3>🖼 图解</h3>'+D.svg;
  if(D.steps.length)dh+='<h3>🔁 原理 / 工作流程</h3><ol class="steps">'+D.steps.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ol>';
  if(D.table)dh+='<h3>📊 对比 / 速查表</h3><div class="tw"><table><tr>'+D.table.head.map(function(x){return '<th>'+esc(x)+'</th>'}).join('')+'</tr>'+D.table.rows.map(function(r){return '<tr>'+r.map(function(x){return '<td>'+esc(x)+'</td>'}).join('')+'</tr>'}).join('')+'</table></div>';
  if(D.example)dh+='<h3>🛠 典型配置示例（华为，# 后为注释）</h3><pre>'+esc(D.example)+'</pre>';
  if(D.exam.length)dh+='<h3>🎯 常见考法</h3><ul>'+D.exam.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul>';
  h=h.replace('<h3>要点</h3>',dh+'<h3>📌 要点归纳</h3>')}
 if(k.pitfalls.length)h+='<h3>⚠ 易错点 / 考点提示</h3><ul>'+k.pitfalls.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul>';
 if(k.commands.length)h+='<h3>常用命令（华为VRP）</h3><pre>'+esc(k.commands.join('\n'))+'</pre>';
 if(k.todo.length)h+='<p class="todo">待核实：'+k.todo.map(esc).join('；')+'</p>';
 h+='<button class="btn" id="lb">'+(lk[id]?'✔ 已学会（点击取消）':'标记为已学')+'</button><a class="btn o" href="#practice/kp-'+id+'">练习本知识点</a></div>';
 app.innerHTML=h;document.getElementById('lb').onclick=function(){var l=S.get('learned',{});if(l[id])delete l[id];else{l[id]=1;checkin()}S.set('learned',l);route()}};
P.practice=function(arg){var dom=S.get('pd','全部'),kp='',typ='全部',cred='全部';
 if(arg&&arg.indexOf('kp-')===0){kp=arg.slice(3);dom='全部'}
 var dayKps=null;if(arg&&arg.indexOf('day')===0)dayKps=PLAN[+arg.slice(3)][2];
 var h='<div class="card"><h2>刷题</h2>领域 <select id="fd"><option>全部</option>'+DOMAINS.map(function(d){return '<option'+(d===dom?' selected':'')+'>'+d+'</option>'}).join('')+'</select> 知识点 <select id="fk"><option value="">全部</option>'+KPS.map(function(k){return '<option value="'+k.id+'"'+(k.id===kp?' selected':'')+'>'+k.domain+'·'+esc(k.title)+'</option>'}).join('')+'</select> 题型 <select id="ft"><option>全部</option><option>判断</option><option>单选</option><option>多选</option></select> 来源 <select id="fc"><option>全部</option><option>回忆</option><option>自编</option><option>题库</option><option>官方</option></select> <label><input type="checkbox" id="fr"> 乱序</label> <button class="btn" id="go">出题</button>'+(dayKps?'<p class="mut">当前：今日知识点题目</p>':'')+'</div><div id="ql"></div>';
 app.innerHTML=h;function go(){var d=fd.value,k=fk.value,t=ft.value,c=fc.value;S.set('pd',d);
  var l=QS.filter(function(q){return (d==='全部'||q.domain===d)&&(!k||q.kp===k)&&(t==='全部'||q.type===t)&&(c==='全部'||q.credibility===c)&&(!dayKps||dayKps.indexOf(q.kp)>=0)});dayKps=null;
  if(fr.checked)l=shuffle(l);var ql=document.getElementById('ql');ql.innerHTML='<p class="mut">共 '+l.length+' 题</p>'+l.map(function(q,i){return renderQ(q,i)}).join('');bindQ(ql)}
 var fd=document.getElementById('fd'),fk=document.getElementById('fk'),ft=document.getElementById('ft'),fc=document.getElementById('fc'),fr=document.getElementById('fr');document.getElementById('go').onclick=go;go()};
function listPage(title,ids,removable,empty){var l=ids.map(qById).filter(Boolean);app.innerHTML='<div class="card"><h2>'+title+'</h2><p class="mut">'+(l.length?'共 '+l.length+' 题':empty)+'</p></div><div id="ql">'+l.map(function(q,i){return renderQ(q,i,{removable:removable})}).join('')+'</div>';bindQ(document.getElementById('ql'))}
P.wrong=function(){var w=S.get('wrong',{});var ids=Object.keys(w).sort(function(a,b){return w[b]-w[a]});listPage('错题本（按错误次数排序）'+(ids.length?' <a class="btn" href="#redo">🔁 错题重做</a>':''),ids,true,'还没有错题。做错的题会自动收录到这里。复盘方法见“备考指南”。')};
P.redo=function(){var w=S.get('wrong',{}),ids=shuffle(Object.keys(w)).slice(0,20);if(!ids.length){app.innerHTML='<div class="card"><h2>错题重做</h2><p>错题本是空的。</p><a class="btn" href="#practice">去刷题</a></div>';return}
 var l=ids.map(qById).filter(Boolean);app.innerHTML='<div class="card"><h2>🔁 错题重做</h2><p class="mut">从错题本随机抽 '+l.length+' 题（最多20题）。同一题<b>连续答对2次</b>自动移出错题本；答错会重新计数。</p><a class="btn o" href="#redo">换一批</a><a class="btn o" href="#wrong">返回错题本</a></div><div id="ql">'+l.map(function(q,i){return renderQ(q,i)}).join('')+'</div>';bindQ(document.getElementById('ql'))};
P.fav=function(){listPage('收藏',Object.keys(S.get('fav',{})),false,'还没有收藏。')};
// mock exam
var EX=null;
P.mock=function(){if(EX&&!EX.done){renderExam();return}
 var avail={};DOMAINS.forEach(function(d){avail[d]=QS.filter(function(q){return q.domain===d}).length});
 var h='<div class="card"><h2>模拟考</h2><p>60题 / 60分钟，按 数通24 · DCN12 · 安全12 · WLAN12 抽题，判断/单选/多选混合。多选题须全部选对才得分（真实计分规则未公开，待核实）。</p><table><tr><th>领域</th><th>需要</th><th>题库现有</th></tr>';
 DOMAINS.forEach(function(d){h+='<tr><td>'+d+'</td><td>'+QUOTA[d]+'</td><td>'+avail[d]+(avail[d]<QUOTA[d]?' <span class="todo">题库待扩充</span>':'')+'</td></tr>'});
 h+='</table><p class="mut">提示：当前题库以自编巩固题为主，模拟考分数只反映对本站讲义的掌握程度，不代表真实考试难度。</p><button class="btn" id="st">开始考试</button></div>';
 var hist=S.get('exams',[]);if(hist.length){h+='<div class="card"><h3>历史成绩</h3><table><tr><th>时间</th><th>得分(折合1000)</th><th>正确</th><th>用时</th></tr>'+hist.slice().reverse().map(function(e){return '<tr><td>'+e.t+'</td><td>'+e.score+'</td><td>'+e.ok+'/'+e.n+'</td><td>'+e.min+'分</td></tr>'}).join('')+'</table></div>'}
 app.innerHTML=h;document.getElementById('st').onclick=startExam};
function startExam(){var picked=[],short=false;DOMAINS.forEach(function(d){var pool=shuffle(QS.filter(function(q){return q.domain===d}));if(pool.length<QUOTA[d])short=true;picked=picked.concat(pool.slice(0,QUOTA[d]))});
 var order={'判断':0,'单选':1,'多选':2};picked.sort(function(a,b){return order[a.type]-order[b.type]});
 EX={ids:picked.map(function(q){return q.id}),ans:{},start:Date.now(),end:Date.now()+3600e3,done:false,short:short};renderExam()}
function renderExam(){var h='<div class="timer" id="tm"></div>'+(EX.short?'<p class="todo">部分领域题量不足，已按现有题目出题（题库待扩充）。</p>':'')+'<div class="card qnav" id="qn"></div><div id="ql">'+EX.ids.map(function(id,i){return '<div id="q'+i+'">'+renderQ(qById(id),i,{exam:true})+'</div>'}).join('')+'</div><button class="btn" id="sb">交卷</button>';
 app.innerHTML=h;var ql=document.getElementById('ql');bindQ(ql,function(q,sel){EX.ans[q.id]=sel.slice();nav()});
 ql.querySelectorAll('.q').forEach(function(el){var a=EX.ans[el.dataset.id]||[];el.querySelectorAll('.opt').forEach(function(o){if(a.indexOf(o.dataset.k)>=0)o.classList.add('sel')})});
 function nav(){document.getElementById('qn').innerHTML=EX.ids.map(function(id,i){return '<span class="'+((EX.ans[id]||[]).length?'a':'')+'" data-i="'+i+'">'+(i+1)+'</span>'}).join('');document.querySelectorAll('#qn span').forEach(function(s){s.onclick=function(){document.getElementById('q'+s.dataset.i).scrollIntoView({behavior:'smooth',block:'center'})}})}nav();
 document.getElementById('sb').onclick=function(){var un=EX.ids.filter(function(id){return !(EX.ans[id]||[]).length}).length;if(confirm(un?'还有'+un+'题未作答，确定交卷？':'确定交卷？'))finishExam()};
 clearInterval(window._et);function tk(){var m=EX.end-Date.now();var t=document.getElementById('tm');if(!t){return}if(m<=0){clearInterval(window._et);alert('时间到，自动交卷');finishExam();return}t.textContent='剩余 '+Math.floor(m/6e4)+':'+('0'+Math.floor(m/1e3%60)).slice(-2)}tk();window._et=setInterval(tk,1000)}
function finishExam(){clearInterval(window._et);EX.done=true;var ok=0,byKp={},byD={};
 EX.ids.forEach(function(id){var q=qById(id),a=EX.ans[id]||[],r=a.length&&sameAns(a,q.answer);if(r)ok++;record(q,!!r);
  [[byKp,q.kp],[byD,q.domain]].forEach(function(p){var o=p[0][p[1]]=p[0][p[1]]||{n:0,ok:0};o.n++;if(r)o.ok++})});
 var n=EX.ids.length,score=Math.round(ok/n*1000),min=Math.round((Date.now()-EX.start)/6e4);var hist=S.get('exams',[]);var d=new Date();hist.push({t:(d.getMonth()+1)+'/'+d.getDate()+' '+d.getHours()+':'+('0'+d.getMinutes()).slice(-2),score:score,ok:ok,n:n,min:min,byD:byD});S.set('exams',hist);
 var weak=Object.keys(byKp).map(function(k){return [k,byKp[k]]}).filter(function(x){return x[1].ok<x[1].n}).sort(function(a,b){return a[1].ok/a[1].n-b[1].ok/b[1].n});
 var h='<div class="card"><h2>成绩：'+score+' / 1000</h2><p>答对 '+ok+'/'+n+'，用时 '+min+' 分钟。<span class="mut">（按题数折算，真实分值规则待核实）</span></p><table><tr><th>领域</th><th>正确率</th></tr>'+DOMAINS.map(function(d){var o=byD[d]||{n:0,ok:0};return '<tr><td>'+d+'</td><td>'+o.ok+'/'+o.n+'</td></tr>'}).join('')+'</table>';
 h+='<h3>📋 按知识点复习建议</h3>'+(weak.length?'<div class="tw"><table><tr><th>知识点</th><th>本次</th><th>建议</th><th></th></tr>'+weak.slice(0,15).map(function(x){var k=kpById(x[0]),r=x[1].ok/x[1].n,adv=r===0?'优先：先读讲义“通俗理解+图解+流程”，再做该知识点全部练习':(r<0.5?'重读“原理/流程”和“易错点”，再刷本知识点题':'看错题解析，用速记卡巩固数值');return '<tr><td>'+esc(k?k.title:x[0])+'</td><td>'+x[1].ok+'/'+x[1].n+'</td><td>'+adv+'</td><td><a href="#kp/'+x[0]+'">讲义</a> · <a href="#practice/kp-'+x[0]+'">练习</a></td></tr>'}).join('')+'</table></div>':'全对，太棒了！')+(function(){var wd=DOMAINS.filter(function(d){var o=byD[d];return o&&o.ok/o.n<0.6});return wd.length?'<p class="todo">正确率低于60%的领域：'+wd.join('、')+'。接下来1–2天优先安排这些领域的讲义复习。</p>':''})()+'<a class="btn" href="#redo">🔁 错题重做</a><a class="btn o" href="#cards">速记卡</a>'+'<br><a class="btn" href="#wrong">去错题本复盘</a><a class="btn o" href="#mock">返回</a></div><h3>答卷解析</h3><div id="ql"></div>';
 app.innerHTML=h;var ql=document.getElementById('ql');ql.innerHTML=EX.ids.map(function(id,i){var q=qById(id),a=EX.ans[id]||[];var r=a.length&&sameAns(a,q.answer);
  return '<div class="card"><div class="mut">第'+(i+1)+'题 <span class="tag">'+q.domain+'</span><span class="tag">'+q.type+'</span><span class="tag c-'+q.credibility+'">'+q.credibility+'</span></div><p><b>'+esc(q.stem)+'</b></p>'+q.options.map(function(o){var c=q.answer.indexOf(o.key)>=0?'right':(a.indexOf(o.key)>=0?'wrong':'');return '<div class="opt '+c+'">'+o.key+'. '+esc(o.text)+'</div>'}).join('')+'<div class="exp"><b style="color:var('+(r?'--ok':'--bad')+')">'+(r?'✔':'✘')+'</b> 你的答案：'+(a.join('')||'未作答')+'　正确答案：'+q.answer.join('')+'<br>'+esc(q.explanation)+'</div></div>'}).join('');EX=null}
P.stats=function(){var st=S.get('stat',{}),agg={},dom={};Object.keys(st).forEach(function(id){var q=qById(id);if(!q)return;[[agg,q.kp],[dom,q.domain]].forEach(function(p){var o=p[0][p[1]]=p[0][p[1]]||{n:0,ok:0};o.n+=st[id].n;o.ok+=st[id].ok})});
 var h='<div class="card"><h2>学习统计</h2><table><tr><th>领域</th><th>作答次数</th><th>正确率</th></tr>'+DOMAINS.map(function(d){var o=dom[d]||{n:0,ok:0};return '<tr><td>'+d+'</td><td>'+o.n+'</td><td>'+(o.n?Math.round(o.ok/o.n*100)+'%':'-')+'</td></tr>'}).join('')+'</table></div>';
 var w=Object.keys(agg).map(function(k){return [k,agg[k]]}).sort(function(a,b){return a[1].ok/a[1].n-b[1].ok/b[1].n});
 h+='<div class="card"><h3>薄弱知识点（正确率从低到高）</h3>'+(w.length?'<table><tr><th>知识点</th><th>正确/作答</th><th></th></tr>'+w.slice(0,15).map(function(x){var k=kpById(x[0]);return '<tr><td>'+esc(k?k.domain+'·'+k.title:x[0])+'</td><td>'+x[1].ok+'/'+x[1].n+'</td><td><a href="#kp/'+x[0]+'">复习</a> · <a href="#practice/kp-'+x[0]+'">再练</a></td></tr>'}).join('')+'</table>':'<p class="mut">还没有做题记录。</p>')+'</div>';
 var ex=S.get('exams',[]);h+='<div class="card"><h3>模拟考趋势</h3>'+(ex.length?ex.map(function(e){return '<div>'+e.t+' <div class="bar" style="display:inline-block;width:60%;vertical-align:middle"><i style="width:'+e.score/10+'%"></i></div> '+e.score+'</div>'}).join(''):'<p class="mut">暂无</p>')+'</div>';
 var ci=Object.keys(S.get('checkin',{})).sort();h+='<div class="card"><h3>打卡记录（'+ci.length+'天）</h3><p>'+(ci.join('　')||'暂无')+'</p><button class="btn o" id="clr">清空所有本地记录</button></div>';
 app.innerHTML=h;document.getElementById('clr').onclick=function(){if(confirm('确定清空进度、错题、收藏、成绩？'))
 {Object.keys(localStorage).forEach(function(k){if(k.indexOf('ict_')===0&&k!=='ict_theme')localStorage.removeItem(k)});route()}}};
P.guide=function(){app.innerHTML=window.GUIDE_HTML||'';};

// router
function route(){var h=(location.hash||'#home').slice(1).split('/');var f=P[h[0]]||P.home;
 if(EX&&!EX.done&&h[0]!=='mock'){if(!confirm('模拟考进行中，离开将保留答卷（计时继续）。确定离开？')){location.hash='#mock';return}}
 document.querySelectorAll('#nav a').forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+h[0])});f(h[1]);window.scrollTo(0,0)}
window.addEventListener('hashchange',route);
if(S.get('theme',null)==='dark'||(S.get('theme',null)===null&&window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.classList.add('dark');
document.getElementById('theme').onclick=function(){var d=document.documentElement.classList.toggle('dark');S.set('theme',d?'dark':'light')};
route();
})();
