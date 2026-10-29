# 2026-10-28 联网核实结果：覆盖原讲义中"待核实"的条目
from h import KPS
def g(i): return [k for k in KPS if k['id']==i][0]
def rep(lst,old,new):
    for i,x in enumerate(lst):
        if old in x: lst[i]=new; return
    raise Exception('not found '+old)
H='（华为官方文档）'
k=g('dt-ospf1'); rep(k['pitfalls'],'MTU','华为缺省不检查MTU：发送DD报文时MTU字段填0，也不检查邻居的MTU，所以两端MTU不一致也能到Full；接口下配ospf mtu-enable后才检查，不一致会卡在ExStart/Exchange。出处：华为S系列V200R023 命令参考 ospf mtu-enable。')
k=g('dt-acl'); rep(k['pitfalls'],'traffic-filter','已核实：接口traffic-filter引用ACL时，未匹配任何规则的报文缺省放行（华为与思科相反）；想"只放行指定流量"要在末尾加 rule deny ip。出处：华为AR300/AR700 V300R022 配置指南《ACL应用模块的ACL默认动作和处理机制》。注意Telnet/VTY等其他模块的缺省动作不同，以该文档的表格为准。')
k=g('dt-ext'); rep(k['pitfalls'],'C-RP','已核实：C-RP优先级数值越小越优先；IPv4 C-RP全局缺省优先级在S7700/AC V200R025文档中是0，IPv6 C-RP缺省是192（技术栈真题题干给的是192，以题干为准）。RP竞选顺序：组范围掩码最长 → 优先级 → Hash值大 → C-RP地址大。出处：华为 c-rp priority 命令参考。'); k['todo']=[]
k=g('dc-mlag'); rep(k['pitfalls'],'Error-Down','已核实：peer-link故障但双主检测心跳正常时，状态为备的设备会把除管理口、peer-link口、堆叠口等之外的业务接口置为Error-Down，防止双主；可用 m-lag unpaired-port reserved 保留指定接口。出处：CloudEngine V200R023C00 配置指南《M-LAG故障场景流量转发》。')
k=g('dc-stack'); k['points'][2]='主交换机选举（iStack，按顺序比）：①最先完成启动的设备 ②（专用堆叠线缆时）Master端多的 ③堆叠优先级高者（1–255，缺省100）④系统MAC小者。出处：华为S5700/S6700 V600R025 配置指南《堆叠建立》、V200R022《Stack Priority》。'; k['todo']=['框式CSS与盒式iStack的细节差异以具体型号文档为准']
k['pitfalls'].append('修改优先级后会立即生效，但不会抢占当前主交换机；要等主交换机或整个堆叠重启后才重新选举。堆叠ID范围0–8，缺省0。')
k=g('dc-lossless'); k['commands']=['dcb pfc','priority 3','quit','interface 100GE1/0/1','dcb pfc enable mode manual','commit']; k['todo']=['命令已按CloudEngine V200R024 配置指南《使能PFC优先级流量控制》核对；其他版本的语法可能不同']
k=g('sec-nat'); rep(k['points'],'处理顺序','已核实：USG先做NAT Server的目的地址转换，再查安全策略，所以安全策略的目的地址和端口要写转换后的私网地址和端口（配置public-ip destination match enable后可以按公网地址匹配）。源NAT在安全策略之后，所以安全策略的源地址写转换前的私网地址。出处：USG6000/USG9500 维护宝典《配置NAT Server时，安全策略中指定的目的地址是转换前还是转换后的地址》。'); k['todo']=[]
k=g('sec-ssl'); k['commands']=['v-gateway test interface GigabitEthernet0/0/1 port 443 private www.test.com','max-user 100','service','network-extension enable','network-extension netpool 192.168.0.2 192.168.0.254 255.255.255.0']; k['todo']=['v-gateway命令来自USG6000 V500的配置示例；V600/USG6000F等版本的配置方式不同，以对应版本的典型配置案例为准']
k=g('sec-vsys'); k['todo']=[]; k['commands']=['vsys enable','vsys name vsysa','assign interface GigabitEthernet1/0/2','switch vsys vsysa','ip route-static 0.0.0.0 0.0.0.0 public','# 根系统回程：ip route-static 10.3.0.0 255.255.255.0 vpn-instance vsysa']
k['points'].append('已核实：在vsysa里配 ip route-static 0.0.0.0 0.0.0.0 public 可以把流量引到根系统；根系统要配回程路由（vpn-instance vsysa）。出处：HiSecEngine USG12000 典型配置案例《配置虚拟系统与根系统通过路由表互访》。')
k=g('sec-urpf'); k['commands']=['interface GigabitEthernet0/0/1','ip urpf strict allow-default-route acl 2000','ip urpf loose','# V300版本AR：urpf { loose | strict } [ allow-default-route ] [ acl acl-number ]']; k['todo']=[]
k['points'].append('已核实处理流程：源地址在FIB里能查到时，严格模式还要求出接口和入接口一致，松散模式不要求；查不到时，只有配置了缺省路由并且带allow-default-route才可能通过（严格模式还要求缺省路由的出接口一致）；只有报文被URPF拒绝后才去匹配ACL，ACL允许就转发。出处：NetEngine AR V600R023 命令参考 ip urpf。')
k=g('sec-cloud'); rep(k['points'],'安全组：','已核实：安全组是实例级的有状态访问控制，规则可以选"允许"或"拒绝"，优先级1–100（数字越小越优先），同一优先级时拒绝优先于允许，没匹配到任何规则就拒绝。默认规则：入方向只允许同一安全组内的实例访问，出方向全部允许。出处：华为云VPC用户指南《安全组和安全组规则概述》。')
rep(k['pitfalls'],'黑名单','注意：技术栈网友回忆题（第九届国赛）把"安全组可以设置白名单和黑名单"判为错误；但华为云现行文档写明安全组支持"拒绝"策略。现在出这道题，答案取决于命题时依据的版本，以官方题解为准。'); k['todo']=[]
k=g('wl-backup'); k['commands']=['wlan','ac protect enable   # 双链路备份，在线AP要重启(ap-reset all)才生效','hsb-service 0','service-ip-port local-ip 10.23.102.1 peer-ip 10.23.102.2 local-data-port 10241 peer-data-port 10241','hsb-service-type ap hsb-service 0','hsb-service-type access-user hsb-service 0']; k['todo']=['命令按AC V200R025/V200R010 配置指南核对；不同版本的完整步骤以文档为准']
k=g('wl-rf'); rep(k['points'],'RSSI','已核实：华为园区WLAN设计建议重点办公区边缘场强-65～-40dBm，一般区域大于-75dBm；相邻AP的覆盖重叠约10%～15%，方便漫游。出处：华为智简园区《WLAN设计》、AC配置指南《场景模板》。'); k['commands']=['wlan','calibrate enable auto interval 1440 start-time 03:00:00','calibrate manual startup','display radio all']; k['todo']=[]
k=g('wl-roam'); rep(k['pitfalls'],'ABD','技术栈回忆题的答案是ABD（包括"修改SSID和加密方式"）。这次没有找到官方题解，D选项是否合理仍待核实。')
