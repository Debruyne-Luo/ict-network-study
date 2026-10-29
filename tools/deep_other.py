from svg import G,seq,flow
from deep_dt import d,DEEP,FIG,T
def f_spine():
    g=G(600,190,'Spine-Leaf：任意两台Leaf之间都是"Leaf-Spine-Leaf"两跳')
    S=[200,400]; L=[90,230,370,510]
    for x in S: g.box(x,35,'Spine',w=80)
    for x in L: g.box(x,120,'Leaf',w=70)
    for s in S:
        for l in L: g.line(s,52,l,103,c='#bbb')
    for l in L: g.box(l,170,'服务器',w=70,h=26).line(l,137,l,157)
    return g.out()
def f_vxlan():
    g=G(640,210,'VXLAN：VTEP把二层帧装进UDP(4789)，穿越三层网络')
    g.box(90,60,'VM1 10.1.1.1',w=120).box(550,60,'VM2 10.1.1.2',w=120)
    g.box(190,140,'VTEP1 Leaf1',w=120).box(450,140,'VTEP2 Leaf2',w=120)
    g.line(90,77,170,123).line(550,77,470,123).line(250,140,390,140,'VXLAN隧道 VNI 5010',dash=True,c='#c7000b')
    g.text(320,190,'外层MAC | 外层IP(VTEP间) | UDP 4789 | VXLAN头(VNI 24位) | 原始以太帧')
    return g.out()
def f_evpn():
    g=G(600,170,'BGP EVPN：用BGP在VTEP之间自动学习MAC/IP、建隧道')
    g.box(300,40,'Spine (RR)',w=110).box(130,130,'Leaf1 VTEP',w=110).box(470,130,'Leaf2 VTEP',w=110)
    g.line(160,113,270,57,'IBGP EVPN',lx=-30).line(440,113,330,57,'',)
    g.line(185,130,415,130,'VXLAN隧道(由3类路由自动建立)',dash=True,c='#c7000b')
    g.text(300,165,'2类=MAC/IP  3类=建隧道/BUM复制列表  5类=IP前缀')
    return g.out()
def f_mlag():
    g=G(600,200,'M-LAG：两台设备对下"假装"成一台')
    g.box(170,50,'Leaf-A',w=100).box(430,50,'Leaf-B',w=100)
    g.line(220,45,380,45,'peer-link(Eth-Trunk)',c='#c7000b').line(220,60,380,60,'心跳(管理口/三层)',dash=True,ly=15)
    g.box(300,160,'服务器(双网卡bond)',w=150).line(170,67,260,143,'M-LAG成员口',lx=-30).line(430,67,340,143)
    return g.out()
def f_stack():
    g=G(560,150,'iStack：多台交换机用堆叠线连成一台逻辑设备')
    g.box(100,60,'SW1 Master',w=110).box(280,60,'SW2 Standby',w=110).box(460,60,'SW3 Slave',w=110)
    g.line(155,60,225,60,'堆叠线').line(335,60,405,60,'堆叠线')
    g.text(280,120,'一个管理IP、一份配置；Master故障时Standby接替')
    return g.out()
def f_zone():
    g=G(600,200,'USG安全区域与安全级别：跨区域流量必须过安全策略')
    g.box(300,100,'USG防火墙',w=120,sub='Local 100')
    g.box(90,100,'Trust 85',w=100,sub='内网').box(510,100,'Untrust 5',w=100,sub='Internet').box(300,180,'DMZ 50',w=100,sub='服务器')
    g.line(140,100,240,100).line(360,100,460,100).line(300,117,300,163)
    g.text(300,30,'区域间默认禁止；按需配置 源区域→目的区域 的允许策略',c='#c7000b')
    return g.out()
def f_ipsec():
    g=G(640,220,'IPSec IKEv1：阶段1建IKE SA（保护协商），阶段2建IPSec SA（保护数据）')
    g.box(90,30,'总部FW',w=110).box(550,30,'分支FW',w=110)
    g.line(90,48,90,215,dash=True).line(550,48,550,215,dash=True)
    y=70
    for t,c in [('阶段1 主模式6个包：协商策略→DH交换→身份认证','#c7000b'),('→ 得到 IKE SA (双向一个)','#c7000b'),('阶段2 快速模式3个包：协商ESP/AH、加密算法','#1a73e8'),('→ 得到 IPSec SA (单向，每方向一个)','#1a73e8'),('感兴趣流(ACL) 经ESP加密传输','#188038')]:
        g.line(150,y,490,y,t,c=c,arrow=True); y+=30
    return g.out()
def f_ssl(): return seq('SSL VPN用户接入过程','远程用户浏览器','虚拟网关(USG)',[('>','HTTPS访问 https://网关:443'),('<','返回证书，建立SSL加密通道'),('>','输入用户名/密码认证'),('<','按角色下发资源(Web代理/网络扩展)'),('>','访问内网资源(经加密隧道)')])
def f_capwap(): return seq('AP上线流程（CAPWAP，控制5246/数据5247）','FIT AP','AC',[('>','DHCP获取IP+AC地址(Option43)'),('>','Discovery Request (发现AC)'),('<','Discovery Response'),('>','Join Request (认证、建立DTLS可选)'),('<','Join Response'),('<','下发版本/配置 (Image Data/Configuration)'),('>','Echo/Keepalive 维持隧道')])
def f_wlnet():
    g=G(640,200,'直接转发 vs 隧道转发')
    g.box(110,40,'AC',w=80).box(110,120,'接入交换机',w=110).box(110,180,'AP',w=60).line(110,137,110,165).line(110,57,110,103)
    g.text(110,100,'业务数据从AP直接到交换机',c='#188038',anchor='start')
    g.box(450,40,'AC',w=80).box(450,120,'接入交换机',w=110).box(450,180,'AP',w=60).line(450,137,450,165).line(450,57,450,103,c='#c7000b')
    g.text(470,80,'业务数据封装在CAPWAP里先到AC',c='#c7000b',anchor='start')
    g.text(110,15,'直接转发').text(450,15,'隧道转发')
    return g.out()
def f_profile():
    g=G(660,190,'WLAN模板引用关系：VAP模板把SSID、安全、VLAN绑在一起')
    g.box(330,40,'AP组 ap-group',w=140)
    g.box(180,105,'VAP模板',w=110).box(480,105,'域管理模板',w=120,sub='国家码')
    g.box(80,170,'SSID模板',w=100).box(220,170,'安全模板',w=100).box(360,170,'业务VLAN',w=100)
    g.line(330,57,180,88).line(330,57,480,88).line(180,122,80,153).line(180,122,220,153).line(180,122,360,153)
    return g.out()
def f_8021x(): return seq('802.1X认证（EAP）','终端(Supplicant)','接入设备→RADIUS',[('>','EAPOL-Start'),('<','EAP-Request/Identity'),('>','EAP-Response/Identity(用户名)'),('<','挑战/凭证交换(经RADIUS转发)'),('<','EAP-Success，端口授权'),('>','开始访问网络')])
def f_roam():
    g=G(600,170,'漫游：二层漫游不换VLAN；三层漫游跨VLAN由家乡AP/AC转发')
    g.box(150,50,'AP1 VLAN10',w=110).box(450,50,'AP2 VLAN10',w=110).line(205,50,395,50,'同VLAN → 二层漫游')
    g.box(300,130,'STA',w=70).line(300,113,170,67,dash=True).line(300,113,430,67,arrow=True)
    g.text(300,165,'STA由AP1移到AP2，IP不变，业务不中断')
    return g.out()
def f_backup():
    g=G(600,170,'AC备份：主备AC，AP与两台AC保持联系')
    g.box(170,40,'主AC',w=90).box(430,40,'备AC',w=90).line(215,40,385,40,'HSB通道同步(热备)',dash=True)
    for x in (150,300,450): g.box(x,140,'AP',w=60).line(x,123,170,57).line(x,123,430,57,dash=True)
    g.text(300,95,'双链路热备/VRRP热备/N+1冷备')
    return g.out()
FIG.update({'f_spine':f_spine,'f_vxlan':f_vxlan,'f_evpn':f_evpn,'f_mlag':f_mlag,'f_stack':f_stack,'f_zone':f_zone,'f_ipsec':f_ipsec,'f_ssl':f_ssl,'f_capwap':f_capwap,'f_wlnet':f_wlnet,'f_profile':f_profile,'f_8021x':f_8021x,'f_roam':f_roam,'f_backup':f_backup})
# ---------- DCN ----------
d('dc-arch','数据中心里服务器之间的"东西向"流量远大于进出外网的"南北向"流量。传统三层树形（接入-汇聚-核心）靠STP阻塞链路，路径长又浪费带宽；Spine-Leaf是扁平的两层结构，每台Leaf连所有Spine，任何两台服务器之间跳数相同，链路全部用ECMP负载分担，要扩容就加Spine或Leaf。',
 ['Leaf（叶）：接服务器、防火墙、出口，是VTEP所在。','Spine（脊）：只负责高速转发，彼此不相连。','Underlay：用OSPF/BGP打通所有设备的环回口（三层网络，无STP）。','Overlay：在Underlay上用VXLAN建虚拟二层网络，给虚拟机迁移用。','Border Leaf：连接外网/防火墙的Leaf。'],
 T(['对比','传统三层架构','Spine-Leaf'],['主要流量','南北向','东西向'],['环路处理','STP阻塞','三层路由+ECMP'],['跳数','不固定','固定（Leaf-Spine-Leaf）'],['扩展','纵向升级核心','横向加设备']),
 '',['Spine-Leaf特点判断题。','Underlay/Overlay概念区分。'],['f_spine'])
d('dc-vxlan','虚拟机迁移要求"IP不变"，也就是要一个很大的二层网络；但大二层有环路、VLAN只有4094个不够租户用。VXLAN的办法：底下用三层IP网络（稳定无环），把二层帧装进UDP里"隧道"传过去，用24位VNI区分约1600万个网段。',
 ['VM发出以太帧到Leaf（VTEP），Leaf根据接入的VLAN/接口映射到BD和VNI。','VTEP查MAC表得知目的VM在远端VTEP2。','封装：原始帧 + VXLAN头(VNI) + UDP(目的端口4789) + 外层IP(源VTEP1→目的VTEP2) + 外层MAC。','Underlay按外层IP路由转发到VTEP2。','VTEP2解封装，按VNI找到BD，转发给VM2。','BUM流量：头端复制（发给VNI内所有VTEP）或组播。'],
 T(['概念','说明'],['VTEP','VXLAN隧道端点，封装/解封装'],['VNI','24位网段标识，类似VLAN ID'],['BD','桥域，二层广播域，与VNI一一映射'],['VBDIF','BD的三层接口，作分布式网关'],['UDP 4789','VXLAN目的端口'],['额外开销','约50字节，Underlay MTU需调大']),
 '[Leaf1] bridge-domain 10\n[Leaf1-bd10] vxlan vni 5010\n[Leaf1] interface 10GE1/0/1.10 mode l2\n[Leaf1-10GE1/0/1.10] encapsulation dot1q vid 10\n[Leaf1-10GE1/0/1.10] bridge-domain 10\n[Leaf1] interface Nve1\n[Leaf1-Nve1] source 1.1.1.1\n[Leaf1-Nve1] vni 5010 head-end peer-list 2.2.2.2   # 静态方式\n[Leaf1] display vxlan tunnel',
 ['VNI位数、UDP端口。','VXLAN封装顺序。','为什么要调大MTU。'],['f_vxlan'])
d('dc-evpn','静态VXLAN要手工写每个对端，几十台Leaf就配不过来了。BGP EVPN让VTEP之间用BGP"广播"自己有哪些MAC/IP、属于哪些VNI，隧道和转发表都自动建立，还能减少ARP泛洪。',
 ['Underlay打通各VTEP环回口。','Leaf与Spine建IBGP EVPN邻居（Spine作RR）。','每个BD配置RD/RT（EVPN实例）。','3类路由（Inclusive Multicast）：通告"我在这个VNI里"→ 自动建隧道、生成BUM头端复制列表。','2类路由：VM上线后通告MAC/IP → 远端VTEP直接学习。','5类路由：通告IP前缀（如外部路由、网段路由）。','分布式网关：每个Leaf都有相同的VBDIF网关IP和MAC，三层转发用L3 VNI。'],
 T(['EVPN路由','名称','用途'],['Type 2','MAC/IP Advertisement','主机MAC、IP（ARP）'],['Type 3','Inclusive Multicast','建隧道、BUM复制'],['Type 5','IP Prefix','网段路由'],['Type 1/4','Ethernet A-D / ES','多活接入（ESI）']),
 '[Leaf1] evpn-overlay enable\n[Leaf1] bridge-domain 10\n[Leaf1-bd10] vxlan vni 5010\n[Leaf1-bd10] evpn\n[Leaf1-bd10-evpn] route-distinguisher 10:1\n[Leaf1-bd10-evpn] vpn-target 10:1\n[Leaf1] interface Nve1\n[Leaf1-Nve1] source 1.1.1.1\n[Leaf1-Nve1] vni 5010 head-end peer-list protocol bgp\n[Leaf1] bgp 100\n[Leaf1-bgp] peer 3.3.3.3 as-number 100\n[Leaf1-bgp] l2vpn-family evpn\n[Leaf1-bgp-af-evpn] peer 3.3.3.3 enable',
 ['各类EVPN路由作用。','分布式网关的好处。'],['f_evpn'])
d('dc-mlag','服务器双网卡想同时连两台Leaf并且两条链路都用上，普通链路聚合要求对端是同一台设备。M-LAG让两台Leaf通过peer-link同步状态，对服务器表现得像一台设备，任何一台坏了另一台继续工作；与堆叠不同，两台设备控制面独立，可以分别升级。',
 ['两台设备配置相同的DFS Group，通过心跳链路协商主备（优先级）。','建立peer-link（一般是Eth-Trunk），同步MAC/ARP表，并在故障时转发流量。','双方把连接服务器的Eth-Trunk配置相同的m-lag ID。','正常时流量各走本地成员口；peer-link上一般只过少量流量。','peer-link故障而心跳正常：备设备把除peer-link、管理口等之外的业务口Error-Down，避免双主（已核实）。'],
 T(['对比','iStack/CSS堆叠','M-LAG'],['控制面','合一','独立'],['升级','整体，影响大','可逐台升级'],['配置','一份','两台各自配置并保持一致'],['可靠性','软件故障影响全部','故障隔离更好']),
 '[LeafA] dfs-group 1\n[LeafA-dfs-group-1] source ip 10.1.1.1\n[LeafA-dfs-group-1] priority 150\n[LeafA] interface Eth-Trunk0\n[LeafA-Eth-Trunk0] trunkport 10GE1/0/47 to 1/0/48\n[LeafA-Eth-Trunk0] peer-link 1\n[LeafA] interface Eth-Trunk10\n[LeafA-Eth-Trunk10] mode lacp-static\n[LeafA-Eth-Trunk10] dfs-group 1 m-lag 1\n[LeafA] display dfs-group 1 m-lag',
 ['peer-link与心跳故障场景（已核实）。','M-LAG与堆叠对比。'],['f_mlag'])
d('dc-stack','把几台交换机"合体"成一台：管理上只有一个IP、一份配置；链路上可以跨设备做Eth-Trunk。合体后要选一个"大脑"（Master）。',
 ['连接堆叠线缆，配置堆叠端口和成员ID（stack slot ... renumber），重启生效。','选主（已核实）：先启动完成的优先 → 若同时启动，比Master端数量 → 比堆叠优先级（大优，缺省100） → MAC小优。','选Standby，其余为Slave。','分配成员编号，Master同步配置给所有成员。','堆叠分裂：用MAD检测双主，保留一方，另一方端口Error-Down。'],
 T(['角色','作用'],['Master','管理整个堆叠'],['Standby','Master的备份'],['Slave','普通成员转发']),
 '[SW1] stack slot 0 priority 200\n[SW1] interface stack-port 0/1\n[SW1-stack-port0/1] port interface GigabitEthernet0/0/27 enable\n[SW2] stack slot 0 renumber 1\n<SW1> display stack',
 ['选主规则顺序（已核实）。','优先级修改不会抢占。','MAD作用。'],['f_stack'])
d('dc-ecmp','到同一目的有多条开销相同的路径时，路由器把流量分散到多条路径上，就是ECMP。为了不打乱同一个连接的报文顺序，一般按"流"做哈希：同一个五元组永远走同一条链路。',
 ['路由协议算出多条等价路由，全部装进路由表（受最大等价条数限制）。','对每个报文计算哈希（源/目IP、协议、源/目端口）。','哈希值决定出接口；同一流始终走同一路径。'],
 T(['方式','优点','缺点'],['逐流','不乱序','流量大小不均时可能不均衡'],['逐包','最均衡','可能乱序']),
 '[R1] ospf 1\n[R1-ospf-1] maximum load-balancing 8\n[R1] display ip routing-table 10.1.1.0',
 ['ECMP要求开销完全相同。','逐流与逐包对比。'])
d('dc-lossless','AI训练、分布式存储用RDMA（RoCEv2），极怕丢包——丢一个包性能就大跌。普通以太网缓冲满了就丢，无损以太网的做法是：快满时让对方"暂停"（PFC），或者更早地让发送方"慢一点"（ECN）。',
 ['对RoCE流量用DSCP/802.1p标记到特定队列（如优先级3）。','PFC：针对这个优先级，入口缓存超过阈值时向上游发PAUSE帧，只暂停该优先级，其他队列不受影响。','ECN：队列超过阈值时在IP头打ECN标记，接收端回CNP，发送端降速（DCQCN）。','PFC死锁检测、Headroom缓存规划保证暂停期间在途报文不丢。'],
 T(['技术','作用层面','作用'],['PFC','逐跳、按优先级','暂停上游，零丢包'],['ECN','端到端','提前通知降速'],['ETS','带宽分配','按队列分配带宽'],['DCBX','协商','LLDP协商DCB参数']),
 '[CE1] dcb pfc\n[CE1-dcb-pfc-default] priority 3\n[CE1] interface 100GE1/0/1\n[CE1-100GE1/0/1] dcb pfc enable mode manual\n[CE1] commit     # CE系列需commit（已核实，V200R024）',
 ['PFC与普通PAUSE区别（按优先级）。','ECN与PFC配合。'])
# ---------- 安全 ----------
d('sec-zone','防火墙用"区域"把网络分成不同信任程度的地带，像大楼里的普通区、办公区、机房。跨区域的流量必须过"门禁"（安全策略）；同区域默认放行。防火墙本身也是一个区域Local，访问防火墙自己（如Ping、登录）也要策略。',
 ['把接口加入区域（接口必须加入区域才能转发）。','报文进入接口 → 确定源区域；查路由找出接口 → 确定目的区域。','查会话表：命中直接转发（状态检测，后续包不再查策略）。','未命中则查安全策略：允许则建会话，拒绝则丢弃。'],
 T(['区域','缺省安全级别'],['Local','100'],['Trust','85'],['DMZ','50'],['Untrust','5']),
 '[FW] firewall zone trust\n[FW-zone-trust] add interface GigabitEthernet1/0/1\n[FW] firewall zone untrust\n[FW-zone-untrust] add interface GigabitEthernet1/0/2\n[FW] display zone',
 ['各区域级别数值。','Local区域含义。','状态检测与会话表。'],['f_zone'])
d('sec-policy','安全策略就是门禁规则：从哪个区域到哪个区域、什么源、什么目的、什么服务 → 允许还是拒绝。规则从上往下匹配，第一条命中就执行；都不命中走缺省策略（拒绝）。',
 ['确定流量的源区域、目的区域、地址、服务、用户、应用。','从上往下匹配规则，命中即执行动作。','允许的流量可再引用安全配置文件（反病毒、IPS、URL过滤）做内容检测。','都不匹配：缺省动作deny。'],
 T(['匹配条件','示例'],['source-zone/destination-zone','trust → untrust'],['source/destination-address','10.1.1.0 24'],['service','http、https、icmp'],['application','微信、P2P'],['user','用户/用户组'],['time-range','上班时间']),
 '[FW] security-policy\n[FW-policy-security] rule name trust_to_untrust\n[FW-policy-security-rule-trust_to_untrust] source-zone trust\n[FW-policy-security-rule-trust_to_untrust] destination-zone untrust\n[FW-policy-security-rule-trust_to_untrust] source-address 10.1.1.0 24\n[FW-policy-security-rule-trust_to_untrust] action permit\n[FW-policy-security] rule move trust_to_untrust before rule_x',
 ['规则顺序题：给几条规则判断某流量结果。','缺省动作。'])
d('sec-nat','防火墙的NAT和路由器原理相同，但多了"NAT策略"和"处理顺序"问题。记住处理顺序：目的NAT（NAT Server）在查安全策略之前，源NAT在安全策略之后（已核实）。',
 ['报文进入：先匹配NAT Server/目的NAT，目的地址变成内网服务器地址。','查路由确定出接口和目的区域。','查安全策略（此时目的地址已是私网地址）。','源NAT：匹配NAT策略，转换源地址。','建立会话，回程按会话反向转换。','注意配置黑洞路由，防止地址池/NAT Server公网地址的路由环路。'],
 T(['类型','用途'],['源NAT（地址池NAPT/Easy-IP）','内网上外网'],['NAT Server','外网访问内网服务器'],['双向NAT','同时转换源和目的'],['NAT ALG','FTP等多通道协议']),
 '[FW] nat address-group pool1\n[FW-address-group-pool1] section 0 202.1.1.10 202.1.1.20\n[FW] nat-policy\n[FW-policy-nat] rule name snat\n[FW-policy-nat-rule-snat] source-zone trust\n[FW-policy-nat-rule-snat] destination-zone untrust\n[FW-policy-nat-rule-snat] action source-nat address-group pool1\n[FW] nat server web protocol tcp global 202.1.1.100 80 inside 10.2.2.10 80\n[FW] ip route-static 202.1.1.10 32 NULL0   # 黑洞路由',
 ['安全策略里写转换前还是转换后地址（已核实：私网目的地址）。','黑洞路由作用。'])
d('sec-ipsec','总部和分支通过Internet连接，数据在公网上"裸奔"。IPSec在两端防火墙之间建立加密隧道：先用IKE谈好"用什么锁、钥匙是什么"，再用这把钥匙加密真正的数据。',
 ['定义感兴趣流（ACL）：哪些流量需要加密。','IKE阶段1：协商加密/认证算法、DH组、身份认证（预共享密钥/证书）→ 建立IKE SA。主模式6个报文，野蛮模式3个。','IKE阶段2（快速模式3个报文）：协商ESP/AH、封装模式 → 建立一对IPSec SA（每方向一个，SPI标识）。','数据用IPSec SA加密传输。','NAT穿越：检测到NAT后ESP封装到UDP 4500。'],
 T(['对比','AH(协议51)','ESP(协议50)'],['加密','不支持','支持'],['完整性','支持（含外层IP头）','支持'],['过NAT','不能','能（NAT-T）']),
 '[FW] acl 3000\n[FW-acl-adv-3000] rule 5 permit ip source 10.1.1.0 0.0.0.255 destination 10.2.2.0 0.0.0.255\n[FW] ipsec proposal p1\n[FW-ipsec-proposal-p1] esp authentication-algorithm sha2-256\n[FW-ipsec-proposal-p1] esp encryption-algorithm aes-256\n[FW] ike proposal 10\n[FW] ike peer branch\n[FW-ike-peer-branch] pre-shared-key Huawei@123\n[FW-ike-peer-branch] remote-address 202.2.2.2\n[FW] ipsec policy map1 10 isakmp\n[FW-ipsec-policy-isakmp-map1-10] security acl 3000\n[FW-ipsec-policy-isakmp-map1-10] proposal p1\n[FW-ipsec-policy-isakmp-map1-10] ike-peer branch\n[FW] interface GigabitEthernet1/0/2\n[FW-GigabitEthernet1/0/2] ipsec policy map1',
 ['两阶段报文数和SA特点。','AH/ESP区别和协议号。','传输/隧道模式。'],['f_ipsec'])
d('sec-ssl','出差员工没有固定IP，也不想装复杂客户端，用浏览器登录SSL VPN网关就能访问内网。它用HTTPS（TLS）加密，按用户角色开放不同资源。',
 ['配置虚拟网关（绑定接口、端口443、域名）。','配置用户与认证方式（本地/RADIUS/AD）。','配置资源：Web代理、文件共享、端口转发、网络扩展（分配内网IP，最像IPSec的全隧道）。','用户与角色关联，角色授权资源。','安全策略放行到网关及网关到内网的流量。'],
 T(['业务','说明'],['Web代理','通过网关访问内网网页'],['文件共享','访问内网共享'],['端口转发','TCP应用'],['网络扩展','虚拟网卡获得内网IP，访问所有IP业务']),
 '[FW] v-gateway test interface GigabitEthernet1/0/1 port 443 private www.test.com   # USG V500示例（已核实）',
 ['SSL VPN四种业务区别。','与IPSec VPN场景对比。'],['f_ssl'])
d('sec-vsys','一台大防火墙"切"成多台小防火墙给不同部门/租户，每台有自己的接口、路由、策略和管理员，就是虚拟系统(vsys)。根系统(public)负责管理并可连接各vsys。',
 ['开启虚拟系统功能，创建vsys并分配资源（带宽、会话数）。','把接口或VLAN分配给vsys。','进入vsys配置区域、策略、路由。','vsys访问Internet：vsys内配缺省路由指向public（已核实写法），在根系统中配回程路由指向vpn-instance。'],
 T(['概念','说明'],['根系统public','缺省存在，管理全部'],['虚拟系统','独立路由表(VPN实例)、策略'],['虚拟接口','vsys之间互访的逻辑接口']),
 '[FW] vsys enable\n[FW] vsys name vsysa\n[FW-vsys-vsysa] assign interface GigabitEthernet1/0/3\n[FW] switch vsys vsysa\n<FW-vsysa> system-view\n[FW-vsysa] ip route-static 0.0.0.0 0.0.0.0 public\n# 根系统回程\n[FW] ip route-static vpn-instance vsysa 10.3.3.0 24 ...',
 ['vsys的独立性。','vsys上网路由配置。'])
d('sec-urpf','攻击者常伪造源IP。URPF反着查路由：收到报文时检查"源地址如果当作目的地址，路由能不能找到、是不是从这个口进来"，不合理就丢弃。',
 ['接口开启URPF。','收到报文，用源IP查FIB。','严格模式：要求有路由且出接口=入接口。','松散模式：只要有路由即可（适合非对称路由）。','allow-default-route：允许匹配缺省路由；若检查失败再匹配ACL，permit的放行（已核实：ACL仅在拒绝时匹配）。'],
 T(['模式','检查','适用'],['严格strict','路由存在且入接口一致','对称路由的边缘'],['松散loose','路由存在','非对称路由、多出口']),
 '[R1] interface GigabitEthernet0/0/1\n[R1-GigabitEthernet0/0/1] ip urpf strict allow-default-route   # AR V600写法（已核实）；V300为 urpf strict',
 ['严格与松散区别。','适用场景。'])
d('sec-attack','网络攻击分几类：泛洪耗尽资源（SYN Flood、UDP Flood）、畸形报文（Land、Teardrop）、扫描探测、欺骗（ARP、IP、DHCP）。防火墙有攻击防范，交换机有DHCP Snooping、DAI、IPSG。',
 ['SYN Flood：大量半连接占满服务器 → 防御：TCP代理/源认证、限速。','ARP欺骗：伪造网关MAC → DAI依据DHCP Snooping绑定表检查ARP。','DHCP仿冒服务器：DHCP Snooping把连接合法服务器的端口设为信任，其他口的Offer丢弃。','IP/MAC仿冒：IPSG按绑定表过滤源IP。'],
 T(['攻击','防御'],['SYN Flood','TCP代理/源认证'],['DHCP仿冒','DHCP Snooping 信任端口'],['ARP欺骗','DAI'],['源IP仿冒','IPSG、URPF'],['MAC泛洪','端口安全、MAC限制']),
 '[SW] dhcp enable\n[SW] dhcp snooping enable\n[SW] interface GigabitEthernet0/0/24\n[SW-GigabitEthernet0/0/24] dhcp snooping trusted\n[SW] vlan 10\n[SW-vlan10] arp anti-attack check user-bind enable\n[SW] interface GigabitEthernet0/0/1\n[SW-GigabitEthernet0/0/1] ip source check user-bind enable',
 ['攻击与防御对应。','DHCP Snooping信任端口位置。'])
d('sec-cloud','云上没有自己的防火墙机柜，华为云提供：安全组（像虚拟机的贴身防火墙）、网络ACL（子网的门卫）、云防火墙、WAF、DDoS防护等。',
 ['安全组作用于云服务器网卡，有状态（回包自动放行）。','规则含方向、协议端口、源/目的、动作（允许/拒绝，已核实支持拒绝）、优先级1–100（数字小优先，同优先级拒绝优先）。','未匹配任何规则的流量拒绝；默认安全组允许组内互访和出方向。','网络ACL作用于子网，无状态。'],
 T(['对比','安全组','网络ACL'],['作用对象','云服务器网卡','子网'],['状态','有状态','无状态'],['规则动作','允许/拒绝','允许/拒绝']),
 '',['安全组与网络ACL对比。','注意：回忆真题中"安全组没有黑名单"与当前华为云文档（支持拒绝规则）冲突，按最新文档理解。'])
# ---------- WLAN ----------
d('wl-basic','WLAN就是把网线换成无线电波。AP是"无线基站"，STA是终端，SSID是网络名称。2.4GHz穿墙好但信道少、干扰多；5GHz信道多速度快但覆盖小。',
 ['AP在信道上周期发送Beacon（携带SSID）。','STA扫描（被动听Beacon或主动发Probe Request）。','链路认证（开放系统）→ 关联（Association）。','接入认证（PSK/802.1X）→ 四次握手生成密钥 → 获取IP开始上网。'],
 T(['频段','非重叠信道','特点'],['2.4GHz','1、6、11（20MHz）','穿透好、干扰多'],['5GHz','较多（国内常用36–64、149–165）','速度快、干扰少'],['6GHz(Wi-Fi 6E/7)','更多','国内部分开放']),
 '',['非重叠信道。','BSSID/SSID/ESS概念区分。','802.11标准与频段。'])
d('wl-capwap','企业里几百个AP不可能逐台配置，于是让"瘦AP"(FIT AP)只负责收发无线，所有配置、管理由AC集中下发。AP与AC之间的通信协议就是CAPWAP：控制隧道UDP 5246、数据隧道UDP 5247。',
 ['AP上电，通过DHCP获取IP，Option 43携带AC地址（或用广播/DNS发现）。','AP发Discovery Request，AC回Response。','AP发Join Request，AC校验（MAC/SN白名单或认证方式）后回Join Response。','AC检查版本，必要时升级（Image Data）。','AC下发配置（Configuration Status），AP进入Run状态。','双方定期Echo（控制隧道）和Keepalive（数据隧道）保活。'],
 T(['项目','值'],['控制隧道','UDP 5246'],['数据隧道','UDP 5247'],['发现AC','静态、DHCP Option 43、DNS、广播'],['AP认证方式','mac-auth、sn-auth、no-auth']),
 '[AC] capwap source interface Vlanif100\n[AC] wlan\n[AC-wlan-view] ap auth-mode mac-auth\n[AC-wlan-view] ap-id 0 ap-mac 00e0-fc12-3456\n[AC-wlan-ap-0] ap-name AP1\n[AC-wlan-ap-0] ap-group default\n# DHCP Option 43（AC地址10.1.100.1）\n[AC-ip-pool-ap] option 43 sub-option 3 ascii 10.1.100.1\n[AC] display ap all',
 ['CAPWAP端口号（真题常考）。','AP上线流程顺序。','Option 43作用。'],['f_capwap'])
d('wl-net','AC放在哪里、业务数据走哪里，是WLAN组网的两个选择：AC可以和AP二层直连或跨三层；AC可以"串"在业务路径中（直连式）或"挂"在旁边（旁挂式）；数据可以直接从AP出去（直接转发）或先送到AC（隧道转发）。',
 ['二层组网：AP与AC同网段，可用广播发现AC。','三层组网：跨网段，需要Option 43或DNS告诉AP AC地址。','直连式：AC同时作为汇聚交换机，数据必经AC。','旁挂式：AC挂在汇聚旁，只有管理流量（隧道转发时业务也会）经过AC。'],
 T(['转发方式','管理流量','业务流量','特点'],['直接转发','CAPWAP到AC','AP直接进有线网','AC压力小，常与旁挂配合'],['隧道转发','CAPWAP到AC','封装到AC再转发','集中控制，AC压力大']),
 '[AC-wlan-view] vap-profile name office\n[AC-wlan-vap-prof-office] forward-mode tunnel     # 或 direct-forward\n[AC-wlan-vap-prof-office] service-vlan vlan-id 101',
 ['直连/旁挂与直接/隧道转发组合判断。','管理VLAN与业务VLAN放通要求。'],['f_wlnet'])
d('wl-profile','华为AC用"模板"层层引用：先建小模板（SSID名、安全方式），再装进VAP模板（再加业务VLAN、转发方式），最后把VAP模板绑定到AP组的射频上。AP组里的AP就都放出这个WLAN。',
 ['创建域管理模板，设国家码CN，在AP组引用。','创建安全模板（如WPA2-PSK AES）。','创建SSID模板（SSID名）。','创建VAP模板，引用SSID模板、安全模板，配业务VLAN、转发方式。','在AP组下 vap-profile xxx wlan 1 radio all 引用。'],
 T(['模板','内容'],['regulatory-domain-profile','国家码、信道/功率范围'],['security-profile','认证加密方式'],['ssid-profile','SSID名称、隐藏等'],['vap-profile','引用上述+业务VLAN+转发'],['radio-2g/5g-profile','射频参数']),
 '[AC-wlan-view] regulatory-domain-profile name domain1\n[AC-wlan-regulate-domain-domain1] country-code cn\n[AC-wlan-view] security-profile name sec1\n[AC-wlan-sec-prof-sec1] security wpa2 psk pass-phrase Huawei@123 aes\n[AC-wlan-view] ssid-profile name ssid1\n[AC-wlan-ssid-prof-ssid1] ssid Office\n[AC-wlan-view] vap-profile name vap1\n[AC-wlan-vap-prof-vap1] forward-mode direct-forward\n[AC-wlan-vap-prof-vap1] service-vlan vlan-id 101\n[AC-wlan-vap-prof-vap1] security-profile sec1\n[AC-wlan-vap-prof-vap1] ssid-profile ssid1\n[AC-wlan-view] ap-group name default\n[AC-wlan-ap-group-default] regulatory-domain-profile domain1\n[AC-wlan-ap-group-default] vap-profile vap1 wlan 1 radio all',
 ['模板引用关系。','配置步骤排序。'],['f_profile'])
d('wl-backup','AC坏了全楼AP掉线，所以AC要备份。常见三种：VRRP热备（两台AC虚拟成一个IP）、双链路备份（AP同时与主备AC建链）、N+1备份（多台主AC共用一台备AC）。',
 ['双链路热备：AP同时与主、备AC建立CAPWAP链路，配合HSB同步用户信息，切换快。','VRRP热备：两台AC通过VRRP对AP呈现一个虚拟IP，HSB同步业务。','N+1：备AC平时不与AP建链，主AC故障后AP重新上线到备AC，切换慢、成本低。','配置主备AC优先级（ac protect enable等，已核实）。'],
 T(['方式','切换速度','成本'],['VRRP热备','快','两台同型号'],['双链路热备','快','可异地'],['N+1冷备','慢（AP需重新上线）','最低']),
 '[AC1-wlan-view] ac protect enable\n[AC1-wlan-view] ap-reset all   # 使配置生效（已核实）',
 ['三种方式对比（场景选择）。'],['f_backup'])
d('wl-auth','WLAN认证决定"谁能连上"。家里用一个共享密码（PSK），企业用每人自己的账号（802.1X，后端RADIUS），访客用网页登录（Portal），哑终端（打印机）用MAC认证。',
 ['链路认证（开放）→ 关联。','接入认证：PSK直接四次握手；802.1X通过EAP与RADIUS认证后再四次握手。','Portal：先连上无认证SSID，HTTP访问被重定向到认证页面，登录后放行。'],
 T(['方式','适用','安全性'],['WPA2/WPA3-PSK','家庭小型','中'],['802.1X(WPA2/3-Enterprise)','企业员工','高'],['Portal','访客','依赖网页'],['MAC认证','哑终端','低']),
 '[AC-wlan-view] security-profile name sec-ent\n[AC-wlan-sec-prof-sec-ent] security wpa2 dot1x aes\n[AC] radius-server template rd1\n[AC-radius-rd1] radius-server authentication 10.1.1.10 1812\n[AC-radius-rd1] radius-server shared-key cipher Huawei@123',
 ['认证方式场景选择。','802.1X三个角色、EAP。','RADIUS端口1812/1813。'],['f_8021x'])
d('wl-roam','人拿着手机走动，从一个AP覆盖区到另一个AP，保持IP不变、业务不断就是漫游。同VLAN叫二层漫游；跨VLAN叫三层漫游，需要把流量绕回原来的"家乡"转发。',
 ['STA检测信号变弱，扫描到更好AP。','重新关联到新AP（802.11r快速漫游可减少认证时间）。','AC同步用户信息（同AC内或AC间通过漫游组）。','三层漫游：流量经隧道回家乡AP/家乡AC转发，保持IP不变。'],
 T(['漫游类型','说明'],['AC内漫游','同一AC管理的AP之间'],['AC间漫游','不同AC，需漫游组、AC间隧道'],['二层漫游','前后VLAN相同'],['三层漫游','VLAN不同，需家乡代理转发']),
 '',['二层/三层漫游区别。','802.11k/v/r作用。'],['f_roam'])
d('wl-wifi6','Wi-Fi 6（802.11ax）重点不是单个设备更快，而是"人多时更好用"：OFDMA把一个信道切成小块同时给多个用户，上下行MU-MIMO同时服务多个用户，BSS着色减少同频干扰，TWT让物联网终端省电。',
 ['OFDMA：信道划分为RU（资源单元），一次传输服务多个STA。','MU-MIMO：多空间流同时给多个用户（Wi-Fi 6支持上下行，8×8）。','1024-QAM：每个符号10比特，速率提升约25%。','BSS Color：区分不同BSS的同频信号，提高空间复用。','TWT：终端与AP约定唤醒时间。'],
 T(['代际','标准','频段','最高调制'],['Wi-Fi 4','802.11n','2.4/5','64-QAM'],['Wi-Fi 5','802.11ac','5','256-QAM'],['Wi-Fi 6','802.11ax','2.4/5','1024-QAM'],['Wi-Fi 6E','802.11ax','+6GHz','1024-QAM'],['Wi-Fi 7','802.11be','2.4/5/6','4096-QAM']),
 '',['各代标准对应。','OFDMA与MU-MIMO区别。','空间流数量与MU-MIMO用户数（真题待核实点）。'])
d('wl-rf','AP越多不一定越好：相邻AP用同一信道会互相干扰。射频调优让AC自动给AP分配信道和功率；规划时还要看场强和重叠。',
 ['勘测：确定覆盖区域、终端数量、墙体衰减。','规划：2.4G用1/6/11蜂窝式交错，5G选更多信道。','场强目标（已核实）：重点办公区边缘-65～-40dBm，一般区域>-75dBm；相邻AP重叠约10%–15%。','部署后开启射频调优（定时或手动），AC根据邻居AP信号调整信道/功率。'],
 T(['参数','建议'],['边缘场强','重点区域≥-65dBm'],['同频干扰','相邻AP不同信道'],['调优时间','业务低峰如凌晨']),
 '[AC-wlan-view] calibrate enable auto interval 1440 start-time 03:00:00\n[AC-wlan-view] calibrate manual startup   # 手动立即调优（已核实）',
 ['非重叠信道规划。','场强/重叠数值。'])
