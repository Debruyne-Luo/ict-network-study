from svg import G,seq,flow
DEEP={}
def d(id,intro,steps=None,table=None,example=None,exam=None,figs=None):
    DEEP[id]=dict(intro=intro,steps=steps or [],table=table,example=example or '',exam=exam or [],figs=figs or [])
# ---------- 图 ----------
def f_osi():
    g=G(560,250,'OSI七层与TCP/IP五层对应、封装过程')
    L=['应用层','表示层','会话层','传输层','网络层','数据链路层','物理层']
    for i,t in enumerate(L): g.box(90,20+i*32,t,w=120,h=26)
    g.box(260,20+32,'应用层',w=120,h=90).box(260,20+3*32,'传输层',w=120,h=26).box(260,20+4*32,'网络层',w=120,h=26).box(260,20+5*32,'数据链路层',w=120,h=26).box(260,20+6*32,'物理层',w=120,h=26)
    for i,t in [(1,'数据 Data'),(3,'段 Segment (TCP/UDP头)'),(4,'包 Packet (IP头)'),(5,'帧 Frame (MAC头+FCS)'),(6,'比特 bit')]: g.text(345,25+i*32,t,anchor='start')
    g.text(90,245,'OSI 7层').text(260,245,'TCP/IP 5层').text(440,245,'发送方逐层加头 = 封装')
    return g.out()
def f_vlan():
    g=G(600,230,'VLAN与Trunk：同VLAN跨交换机互通，跨VLAN需三层')
    g.box(170,110,'SW1').box(430,110,'SW2').line(215,110,385,110,'Trunk 放行VLAN10,20（带802.1Q标签）')
    for x,v in [(90,'PC1 VLAN10'),(250,'PC2 VLAN20')]: g.box(x,200,v,w=110).line(x,183,170,127,'Access',lx=-20)
    for x,v in [(350,'PC3 VLAN10'),(510,'PC4 VLAN20')]: g.box(x,200,v,w=110).line(x,183,430,127,'Access',lx=20)
    g.box(300,30,'三层交换/路由器',w=140,sub='VLANIF10/VLANIF20').line(300,47,170,93,dash=True).line(300,47,430,93,dash=True)
    g.text(300,160,'PC1↔PC3：二层直通；PC1↔PC2：必须经过网关',c='#c7000b')
    return g.out()
def f_stp():
    g=G(560,250,'STP选举示例：优先级4096的SW1为根桥')
    g.box(280,40,'SW1 根桥',w=120,sub='4096').box(120,190,'SW2',w=100,sub='32768 MAC小').box(440,190,'SW3',w=100,sub='32768 MAC大')
    g.line(225,50,140,172,'DP ─── RP',lx=-30).line(335,50,420,172,'DP ─── RP',lx=30).line(170,190,390,190,'')
    g.text(185,180,'DP').text(375,180,'阻塞(AP)',c='#d93025').x(380,190)
    g.text(280,235,'①选根桥 ②非根桥选RP ③每段链路选DP ④其余端口阻塞')
    return g.out()
def f_trunk():
    g=G(520,140,'Eth-Trunk：多条物理链路捆绑成一条逻辑链路')
    g.box(90,70,'SW1').box(430,70,'SW2')
    for dy in (-20,0,20): g.line(135,70+dy,385,70+dy)
    g.text(260,40,'Eth-Trunk 1（LACP）').text(260,120,'带宽相加、一条坏了其余继续转发、按流哈希负载分担')
    return g.out()
def f_route():
    g=G(600,170,'路由查找：最长匹配 → 优先级 → 开销')
    g.box(80,80,'PC',w=70).box(250,80,'R1',sub='查路由表').box(450,40,'R2').box(450,130,'R3')
    g.line(115,80,205,80).line(295,72,405,45,'OSPF 10 cost 20').line(295,88,405,125,'静态 60',lx=10,ly=18)
    g.text(300,160,'同一目的网段：OSPF(10)比静态(60)优，选R2；静态路由当浮动备份')
    return g.out()
def f_vrrp():
    g=G(560,230,'VRRP：两台网关虚拟成一台 10.1.1.254')
    g.box(280,30,'核心/上行',w=110)
    g.box(160,110,'R1 Master',w=110,sub='优先级120').box(400,110,'R2 Backup',w=110,sub='优先级100')
    g.line(160,93,250,47).line(400,93,310,47).line(215,110,345,110,'VRRP通告 224.0.0.18 每1秒',dash=True)
    g.box(280,200,'PC 网关=10.1.1.254',w=170).line(280,183,160,127).line(280,183,400,127,dash=True)
    g.text(280,160,'R1故障 → R2收不到通告(3倍间隔+偏移) → R2成为Master，发免费ARP',c='#c7000b')
    return g.out()
def f_nat():
    g=G(600,170,'NAPT：私网地址+端口 换成 公网地址+端口')
    g.box(80,80,'PC 192.168.1.10',w=130).box(300,80,'出口路由器',w=120,sub='NAT表').box(520,80,'Internet服务器',w=130)
    g.line(145,80,240,80).line(360,80,455,80)
    g.text(190,60,'源 192.168.1.10:3000').text(410,60,'源 202.1.1.1:10001')
    g.text(300,140,'回程：202.1.1.1:10001 → 查NAT表 → 192.168.1.10:3000',c='#c7000b')
    return g.out()
def f_dhcp(): return seq('DHCP获取地址四步（前期为广播）','客户端 UDP68','服务器 UDP67',[('>','① Discover 广播找服务器'),('<','② Offer 提供地址'),('>','③ Request 请求使用'),('<','④ ACK 确认，开始计租期'),('>','50%租期 单播Request续约')])
def f_ospf(): return flow('OSPF邻居状态机（Full才算邻接完成）',['Down','Init','2-Way','ExStart','Exchange','Loading','Full'],w=680)
def f_ospfarea():
    g=G(600,190,'OSPF多区域：非骨干区域必须连到Area 0')
    g.box(300,40,'Area 0 骨干',w=160)
    g.box(130,150,'Area 1',w=110).box(470,150,'Area 2 (Stub)',w=130)
    g.box(200,95,'ABR1',w=70).box(400,95,'ABR2',w=70).line(200,78,260,57).line(400,78,340,57).line(200,112,150,133).line(400,112,450,133)
    g.box(40,95,'ASBR',w=60,sub='引入外部').line(40,112,100,133)
    g.text(300,180,'1/2类LSA区域内；ABR生成3类；ASBR的外部路由是5类；Stub区域内不出现5类')
    return g.out()
def f_bgp():
    g=G(600,190,'IBGP与EBGP；IBGP水平分割')
    g.box(110,60,'R1 AS100').box(300,60,'R2 AS200').box(490,60,'R3 AS200').box(400,150,'R4 AS200')
    g.line(155,60,255,60,'EBGP(直连,TTL=1)').line(345,60,445,60,'IBGP').line(320,77,385,133,'IBGP',lx=-10).line(470,77,415,133,'?',dash=True)
    g.text(300,185,'R2从R1学到的路由发给IBGP邻居R3，R3不会再转给IBGP邻居R4 → 全互联或部署RR')
    return g.out()
def f_bgpsel(): return flow('华为BGP选路顺序（前7步最常考）',['PrefVal 大','LocalPref 大','本地始发','AS_PATH 短','Origin I>E>?','MED 小','EBGP>IBGP'],w=760)
def f_ipv6(): return seq('IPv6 NDP：地址解析与无状态自动配置','主机','路由器/邻居',[('>','RS(133) 请求前缀'),('<','RA(134) 通告前缀2001:db8:1::/64'),('>','NS(135) DAD：这个地址有人用吗?'),('>','NS(135) 解析邻居MAC(组播)'),('<','NA(136) 回复MAC')])
def f_mpls():
    g=G(660,190,'MPLS VPN：CE-PE-P-PE-CE 与两层标签')
    for x,t,s in [(60,'CE1',None),(190,'PE1','VRF A'),(330,'P','只交换外层标签'),(470,'PE2','VRF A'),(600,'CE2',None)]: g.box(x,60,t,w=80 if not s else 110,sub=s)
    g.line(100,60,135,60).line(245,60,275,60).line(385,60,415,60).line(525,60,560,60)
    g.line(190,100,470,100,'MP-BGP 传 VPNv4路由(RD+IPv4) + RT + 私网标签',dash=True,ly=-6)
    g.text(330,140,'转发：[外层LDP公网标签][内层VPN私网标签][IP报文]')
    g.text(330,170,'RD：让重叠地址唯一；RT：export/import 决定路由进哪个VRF',c='#c7000b')
    return g.out()
FIG={'f_osi':f_osi,'f_vlan':f_vlan,'f_stp':f_stp,'f_trunk':f_trunk,'f_route':f_route,'f_vrrp':f_vrrp,'f_nat':f_nat,'f_dhcp':f_dhcp,'f_ospf':f_ospf,'f_ospfarea':f_ospfarea,'f_bgp':f_bgp,'f_bgpsel':f_bgpsel,'f_ipv6':f_ipv6,'f_mpls':f_mpls}
T=lambda h,*r: dict(head=h,rows=list(r))
# ---------- 讲义详解 ----------
d('dt-osi','把寄快递想成网络通信：你写信（应用层数据），装进信封写上收件人房间号（传输层端口），再写上城市街道（网络层IP），快递员按最近一站的地址送（数据链路层MAC），最后靠车和路（物理层）跑起来。每一层只关心自己的那张"标签"，这就是分层。发送时从上往下一层层加头（封装），接收时从下往上一层层拆头（解封装）。',
 ['发送方：应用产生数据 → 传输层加TCP/UDP头(端口) → 网络层加IP头(源/目的IP) → 数据链路层加以太网头和FCS(源/目的MAC) → 物理层变成电/光信号。','中间的交换机只看到第2层（MAC），路由器拆到第3层（IP）查路由，然后重新封装二层头。','接收方从下往上逐层校验、拆头，最后交给对应端口的应用。'],
 T(['层','作用','数据单元','典型协议/设备'],['应用层','给应用提供服务','数据','HTTP、DNS、FTP、Telnet'],['传输层','端到端、端口区分应用','段','TCP、UDP'],['网络层','逻辑寻址、选路','包','IP、ICMP、OSPF；路由器'],['数据链路层','同一链路内传帧','帧','Ethernet、PPP；交换机'],['物理层','比特传输','比特','网线、光纤、集线器']),
 '',['问"某设备/协议工作在哪一层"（交换机二层、路由器三层、ICMP网络层）。','问"传输层/网络层的数据单元叫什么"。','给出封装顺序让你排序。'],['f_osi'])
d('dt-tcpudp','TCP像打电话：先拨通（三次握手），说一句对方回一句"收到"，没回就重说（重传），说完再挂断（四次挥手），可靠但慢一点。UDP像发短信：直接发，不管对方收没收到，快、开销小，适合视频、语音、DNS查询这种"丢一点也没关系、要快"的场景。',
 ['三次握手：客户端SYN(seq=x) → 服务器SYN+ACK(seq=y, ack=x+1) → 客户端ACK(ack=y+1)，连接建立。','数据传输：按序号排序，收到就确认(ACK)，超时重传；用窗口大小做流量控制。','四次挥手：FIN → ACK → FIN → ACK（因为两个方向要分别关闭）。'],
 T(['对比','TCP','UDP'],['连接','面向连接','无连接'],['可靠性','确认+重传+排序','不保证'],['头部','≥20字节','8字节'],['典型应用','HTTP/HTTPS、FTP、Telnet、SSH、BGP(179)','DNS查询、DHCP、TFTP、SNMP、RIP(520)、VXLAN(4789)、CAPWAP(5246/5247)']),
 '',['端口号对应协议（大赛常把端口号和WLAN/VXLAN结合考）。','"BGP基于TCP"，"OSPF直接封装在IP里（协议号89），不用TCP/UDP"。'])
d('dt-ip','IP地址像"城市+门牌号"：掩码告诉你哪部分是城市（网络位），哪部分是门牌（主机位）。同一网段的主机可以直接通信，不同网段要找网关（路由器）。子网划分就是把一个大城市划成几个小区：从主机位借几位给网络位。',
 ['写出掩码：/26 = 255.255.255.192（最后一个字节借了2位：128+64）。','算块大小：256−192=64，所以网段是 .0 .64 .128 .192。','找所在网段：地址最后一字节 ÷ 块大小取整 × 块大小。例 .77 → 64。','网络地址=该段起点(.64)，广播地址=下一段起点−1(.127)，可用主机 .65–.126，共62个。','汇总：把地址写成二进制，找共同的前缀位数。'],
 T(['前缀','掩码最后字节','块大小','可用主机'],['/24','0','256','254'],['/25','128','128','126'],['/26','192','64','62'],['/27','224','32','30'],['/28','240','16','14'],['/29','248','8','6'],['/30','252','4','2']),
 '# 例：192.168.1.0/24 划分给4个部门，每部门≤50台\n# 需要主机位≥6（2^6-2=62），借2位 → /26\n192.168.1.0/26    可用 .1-.62    广播 .63\n192.168.1.64/26   可用 .65-.126  广播 .127\n192.168.1.128/26  可用 .129-.190 广播 .191\n192.168.1.192/26  可用 .193-.254 广播 .255',
 ['给IP和掩码求网络地址/广播地址/可用范围。','给主机数求最合适的掩码。','求能划分多少子网、路由汇总（如ip-prefix计算题的基础）。'])
d('dt-arp','你知道同事的名字(IP)，但要把文件递到他手里需要知道他的座位(MAC)。ARP就是在办公室里喊一声"谁是10.1.1.2？"（广播），对方回答"是我，座位在这"（单播），然后你记到小本子上（ARP缓存）。',
 ['主机A查ARP缓存，没有对方MAC。','A广播ARP请求：目的MAC全F，内容"谁是10.1.1.2？我是10.1.1.1/MAC-A"。','同网段所有主机收到，只有10.1.1.2回复单播ARP应答。','A把IP-MAC写入ARP表，开始发数据帧。','跨网段时，A请求的是网关的MAC，数据帧目的MAC是网关。'],
 T(['类型','用途'],['ARP请求/应答','IP→MAC解析'],['免费ARP','检测IP冲突、通告自己MAC变化（VRRP切换）'],['代理ARP','路由器替其他网段主机回复'],['ARP欺骗','伪造应答，靠DAI等防御']),'',['ARP请求是广播还是单播。','跨网段时请求谁的MAC。','交换机收到未知单播怎么处理（泛洪）。'])
d('dt-vrp','华为设备的命令行叫VRP。记住"视图"就像游戏里的不同房间：在大厅(用户视图)只能看，进到控制室(系统视图)才能改全局配置，再进到某个接口房间才能配接口。',
 ['<Huawei> 用户视图：display查看、save保存、reboot。','system-view 进入 [Huawei] 系统视图：改设备名、建VLAN、开协议。','interface GigabitEthernet0/0/1 进入接口视图：配IP、端口类型。','quit 退回上一层，return（或Ctrl+Z）直接回用户视图。','配错了用 undo + 原命令 删除。'],
 T(['思科','华为'],['show','display'],['no','undo'],['configure terminal','system-view'],['write','save'],['exit','quit'],['hostname','sysname']),
 '<Huawei> system-view\n[Huawei] sysname R1\n[R1] interface GigabitEthernet0/0/1\n[R1-GigabitEthernet0/0/1] ip address 10.1.1.1 24\n[R1-GigabitEthernet0/0/1] quit\n[R1] user-interface vty 0 4\n[R1-ui-vty0-4] authentication-mode aaa\n[R1] aaa\n[R1-aaa] local-user admin password irreversible-cipher Huawei@123\n[R1-aaa] local-user admin service-type ssh telnet\n[R1-aaa] local-user admin privilege level 15\n[R1] return\n<R1> save',
 ['命令关键字辨析（undo、display、system-view）。','current-configuration 与 saved-configuration 区别。'])
d('dt-vlan','一台交换机默认所有口在一个广播域里，人一多广播就满天飞、也不安全。VLAN就是在交换机里砌"隔墙"：VLAN10的人和VLAN20的人互相听不到广播。墙的那边要来往，必须走"大门"（三层网关）。跨交换机时，用Trunk链路把多个VLAN的帧带上"标签"一起传。',
 ['终端发出的帧不带标签 → 进入Access口时打上PVID对应的VLAN标签（交换机内部）。','从Trunk口出去：放行的VLAN帧保留标签；VLAN=PVID的帧剥掉标签。','对端Trunk口收到带标签帧按标签转发；收到不带标签帧归入自己的PVID。','从Access口出去给终端：剥掉标签。','跨VLAN通信：三层交换机为每个VLAN建VLANIF接口作网关，查路由转发。'],
 T(['端口类型','收到不带标签帧','发送时','典型用途'],['Access','打PVID标签','剥标签','接PC/打印机'],['Trunk','打PVID标签','PVID的VLAN剥标签，其他保留','交换机互联'],['Hybrid','打PVID标签','按配置untagged/tagged','灵活场景、接AP等']),
 '[SW1] vlan batch 10 20\n[SW1] interface GigabitEthernet0/0/1\n[SW1-GigabitEthernet0/0/1] port link-type access\n[SW1-GigabitEthernet0/0/1] port default vlan 10\n[SW1] interface GigabitEthernet0/0/24\n[SW1-GigabitEthernet0/0/24] port link-type trunk\n[SW1-GigabitEthernet0/0/24] port trunk allow-pass vlan 10 20\n# 三层网关\n[SW1] interface Vlanif10\n[SW1-Vlanif10] ip address 192.168.10.254 24\n[SW1] display port vlan',
 ['VID位数、可用范围。','Access/Trunk/Hybrid收发规则（尤其PVID）。','给出配置问两台PC能否通信。'],['f_vlan'])
d('dt-stp','交换机为了可靠会连成环，但二层帧没有TTL，一旦有环，广播会无限转圈（广播风暴），MAC表也会乱跳。STP的办法是：选一个"老大"（根桥），每台交换机只保留通往老大的最佳路径，多余的口"堵上"（阻塞）。主路断了，再把堵住的口打开。',
 ['选根桥：所有交换机比桥ID（优先级+MAC），最小的当根桥。','选根端口(RP)：每台非根桥选一个到根桥开销最小的端口；开销相同比对端桥ID，再比对端端口ID。','选指定端口(DP)：每条链路上选一个离根最近的端口负责转发；根桥的端口都是DP。','剩下既不是RP也不是DP的端口 → 阻塞（不转发数据，但接收BPDU）。','拓扑变化时：发TCN，MAC表加速老化，阻塞口经过Listening(15s)→Learning(15s)才转发。'],
 T(['计时器','缺省值','作用'],['Hello Time','2秒','根桥发BPDU的间隔'],['Forward Delay','15秒','Listening、Learning各停留时间'],['Max Age','20秒','BPDU老化时间']),
 '[SW1] stp mode stp\n[SW1] stp priority 4096      # 或 stp root primary\n[SW2] interface GigabitEthernet0/0/1\n[SW2-GigabitEthernet0/0/1] stp cost 2000\n[SW1] display stp brief',
 ['给拓扑和优先级/MAC，判断根桥、根端口、阻塞端口。','端口状态顺序和计时器数值。','优先级取值必须是4096倍数。'],['f_stp'])
d('dt-rstp','STP收敛太慢（30–50秒），RSTP加了"快速通道"：提前准备好备份口（Alternate），主路断了直接切；交换机之间用"提议/同意"(P/A)握手马上转发；接电脑的口设成边缘端口，插上就能用。MSTP再进一步：不同VLAN可以走不同的树，两条链路都能用上。',
 ['RSTP端口角色：根端口、指定端口、Alternate（RP的备份）、Backup（DP的备份）、边缘端口。','根端口故障 → Alternate端口立即变为根端口并转发，无需等待。','P/A机制：上游指定端口发Proposal，下游阻塞其他非边缘端口后回Agreement，上游立刻转发。','MSTP：配置MST域（域名、修订级别、VLAN映射一致）→ 每个实例独立选根 → 不同实例阻塞不同端口。'],
 T(['对比','STP(802.1D)','RSTP(802.1w)','MSTP(802.1s)'],['端口状态','5种','3种(Discarding/Learning/Forwarding)','同RSTP'],['收敛','30–50秒','秒级','秒级'],['多实例负载分担','否','否','是'],['华为缺省','','','是（缺省模式）']),
 '[SW1] stp mode mstp\n[SW1] stp region-configuration\n[SW1-mst-region] region-name RG1\n[SW1-mst-region] instance 1 vlan 10 20\n[SW1-mst-region] instance 2 vlan 30 40\n[SW1-mst-region] active region-configuration\n[SW1] stp instance 1 root primary\n[SW1] stp instance 2 root secondary\n[SW1] interface GigabitEthernet0/0/10\n[SW1-GigabitEthernet0/0/10] stp edged-port enable\n[SW1] stp bpdu-protection',
 ['Alternate与Backup端口区别。','边缘端口收到BPDU会怎样、BPDU保护作用。','MSTP同域条件。'])
d('dt-trunk','两台交换机间一根线不够用、坏了又断网，于是并几根线。但STP会把多出来的线堵掉，所以要把它们"捆"成一条逻辑链路（Eth-Trunk），STP只看到一条，带宽却是几根之和。',
 ['创建Eth-Trunk接口，选择模式（手工/LACP）。','把成员物理口加入（速率、双工要一致）。','LACP模式下双方交换LACPDU：系统优先级小的一端为主动端，由主动端按接口优先级选活动成员。','流量按流哈希（源/目MAC、IP等）分配到成员链路。'],
 T(['对比','手工模式','LACP模式'],['协商','无','有LACPDU'],['备份链路','不支持，全部活动','支持（最大活动数之外的成员备份）'],['检测对端误连','不能','能']),
 '[SW1] interface Eth-Trunk1\n[SW1-Eth-Trunk1] mode lacp\n[SW1-Eth-Trunk1] trunkport GigabitEthernet0/0/1 to 0/0/3\n[SW1-Eth-Trunk1] max active-linknumber 2\n[SW1] lacp priority 100\n[SW1] display eth-trunk 1',
 ['LACP优先级默认值与比较规则。','手工与LACP区别。'],['f_trunk'])
d('dt-route','路由器像快递分拣中心：看包裹的目的地址，查"路由表"决定从哪个口送出去。路由表可以手工写（静态路由），也可以让路由器之间自己学（动态路由协议）。',
 ['报文到达，取目的IP。','在路由表里找所有能匹配的条目，选掩码最长的那个。','如果有多条同样长的来自不同协议，比较优先级(Preference)，小的进路由表。','同协议多条，比开销(Cost)，小的优；相同则等价负载分担。','按选中路由的出接口/下一跳转发；都匹配不到就丢弃（除非有默认路由）。'],
 T(['路由来源','华为缺省优先级'],['直连 Direct','0'],['OSPF 内部','10'],['IS-IS','15'],['静态 Static','60'],['RIP','100'],['OSPF ASE/NSSA（外部）','150'],['IBGP / EBGP','255']),
 '# 主备出口：主走10.1.1.2，备走10.2.2.2（浮动静态）\n[R1] ip route-static 0.0.0.0 0 10.1.1.2\n[R1] ip route-static 0.0.0.0 0 10.2.2.2 preference 100\n[R1] display ip routing-table protocol static',
 ['默认优先级数值。','最长匹配判断。','浮动静态路由的preference要大还是小。'],['f_route'])
d('dt-ospf1','OSPF像每个路由器都画一张全网地图：先和邻居打招呼(Hello)，再交换地图目录(DD)，缺哪页要哪页(LSR/LSU/LSAck)，地图一致后各自用"最短路径算法"(SPF)算路线。因为每台都有完整地图，所以收敛快、无环。',
 ['发Hello(组播224.0.0.5)发现邻居 → Init；在对方Hello里看到自己的Router ID → 2-Way。','广播网络在2-Way后选DR/BDR，DRother之间停在2-Way。','ExStart：选主从，确定DD序号（Router ID大者为主）。','Exchange：交换DD（LSA摘要）。','Loading：发LSR请求缺的LSA，对方回LSU，再回LSAck。','Full：数据库同步完成，运行SPF算路由。'],
 T(['报文','作用'],['Hello','发现、维持邻居，选DR'],['DD','LSDB摘要'],['LSR','请求具体LSA'],['LSU','发送LSA'],['LSAck','确认']),
 '[R1] ospf 1 router-id 1.1.1.1\n[R1-ospf-1] area 0\n[R1-ospf-1-area-0.0.0.0] network 10.1.12.0 0.0.0.255\n[R1-ospf-1-area-0.0.0.0] network 1.1.1.1 0.0.0.0\n[R1] interface GigabitEthernet0/0/1\n[R1-GigabitEthernet0/0/1] ospf dr-priority 0   # 不参选DR\n[R1-GigabitEthernet0/0/1] ospf cost 10\n[R1] display ospf peer brief',
 ['邻居状态顺序、停在哪个状态说明什么问题。','DR/BDR选举规则及非抢占。','建邻居需要一致的参数。'],['f_ospf'])
d('dt-ospf2','整个公司只有一张地图太大了，OSPF把网络切成"区域"：区域内部画详细地图，区域之间只交换"摘要"。Area 0 是中央枢纽，其他区域都要挂在它上面。',
 ['区域内：路由器产生1类LSA；DR产生2类LSA；区域内泛洪。','ABR：把一个区域的路由汇成3类LSA发到其他区域。','ASBR：import-route引入外部路由，生成5类LSA全网泛洪；ABR为其他区域生成4类LSA告诉大家ASBR在哪。','Stub区域：ABR不放5类进来，发一条3类默认路由；Totally Stub连3类也挡，只留默认路由。','NSSA：区域里有ASBR又想挡5类，就用7类LSA，出区域时ABR转成5类。'],
 T(['LSA','产生者','范围','内容'],['1 Router','所有路由器','本区域','自己的链路'],['2 Network','DR','本区域','广播网段成员'],['3 Summary','ABR','区域间','其他区域网段'],['4 ASBR-Summary','ABR','区域间','ASBR位置'],['5 External','ASBR','整个AS(除特殊区域)','外部路由'],['7 NSSA','NSSA内ASBR','NSSA区域','外部路由']),
 '[R2] ospf 1\n[R2-ospf-1] area 1\n[R2-ospf-1-area-0.0.0.1] stub no-summary   # Totally Stub，只在ABR加no-summary\n[R3] ospf 1\n[R3-ospf-1] import-route static\n[R3-ospf-1] area 2\n[R3-ospf-1-area-0.0.0.2] nssa\n[R1] display ospf lsdb',
 ['某类LSA由谁产生、在哪出现。','Stub/Totally Stub/NSSA区别。'],['f_ospfarea'])
d('dt-bgp1','OSPF是公司内部的地图，BGP是"国与国之间的外交"：每个自治系统(AS)是一个国家，BGP不关心最短路，而是按"政策"决定把哪些路由告诉谁、选哪条。因为路由条目极多，BGP基于可靠的TCP，只发增量更新。',
 ['建立TCP连接(179)：Idle → Connect/Active。','互发Open协商AS号、Router ID、保持时间 → OpenSent → OpenConfirm。','收到Keepalive → Established。','通过Update发布/撤销路由；出错发Notification断开。','路由来源：network命令（路由表里要有该路由）或import-route引入。'],
 T(['对比','IBGP','EBGP'],['AS关系','同一AS','不同AS'],['默认TTL','255','1（非直连需ebgp-max-hop）'],['下一跳','默认不改','改为自己'],['防环','水平分割(不转发给IBGP)','AS_PATH']),
 '[R1] bgp 100\n[R1-bgp] router-id 1.1.1.1\n[R1-bgp] peer 10.1.12.2 as-number 200          # EBGP\n[R1-bgp] peer 3.3.3.3 as-number 100            # IBGP用环回口\n[R1-bgp] peer 3.3.3.3 connect-interface LoopBack0\n[R1-bgp] peer 3.3.3.3 next-hop-local\n[R1-bgp] network 192.168.1.0 24\n[R1] display bgp peer',
 ['BGP端口/状态。','IBGP水平分割与RR。','IBGP下一跳不可达的处理。'],['f_bgp'])
d('dt-bgp2','同一个目的网段可能从多个邻居学到，BGP像"按顺序比条件"的面试：第一项分出高下就录用，平了才比下一项。考试最爱考前几项和每个属性"大好还是小好"。',
 ['先排除下一跳不可达的路由。','比Preferred-Value（华为私有，只在本机有效，大优）。','比Local_Preference（AS内传递，大优，缺省100）。','本地始发的路由优先（network/import/聚合）。','比AS_PATH长度（短优）。','比Origin（IGP > EGP > Incomplete）。','比MED（小优，默认只比来自同一相邻AS的）。','EBGP路由优于IBGP；再比到下一跳的IGP开销；再比Cluster_List、Router ID等。'],
 T(['属性','类别','优选','传播范围'],['Preferred-Value','华为私有','大','本设备'],['Local_Pref','公认任意','大','本AS内'],['AS_PATH','公认必遵','短','全局'],['Origin','公认必遵','IGP>EGP>?','全局'],['MED','可选非过渡','小','相邻AS'],['Community','可选过渡','—','打标签']),
 '# 让AS内路由器优选经R2出去的路径\n[R2] route-policy LP permit node 10\n[R2-route-policy] apply local-preference 200\n[R2] bgp 100\n[R2-bgp] peer 10.2.2.2 route-policy LP import\n# 让外部AS从R3进来：向邻居出方向调小MED\n[R3] route-policy MED permit node 10\n[R3-route-policy] apply cost 10\n[R3-bgp] peer 10.3.3.3 route-policy MED export',
 ['给场景问"哪些方法能改变选路"（真题多选）。','属性传播范围（Local_Pref不跨AS）。'],['f_bgpsel'])
d('dt-policy','路由策略=先"挑"(匹配)再"处理"(允许/拒绝/改属性)。挑的工具里，前缀列表(ip-prefix)最精确，能同时匹配网络号和掩码长度。',
 ['确定基准：前N位（掩码长度）必须和给定网络相同。','确定掩码范围：不写ge/le→只匹配掩码=N；写了→掩码在[ge, le]之间（要求 N ≤ ge ≤ le ≤ 32）。','计数：掩码m时可匹配2^(m−N)条，各m相加。','route-policy按node号顺序：命中node后，permit则执行apply，deny则拒绝；都不命中则拒绝。'],
 T(['写法','匹配'],['10.0.0.0 8','只有10.0.0.0/8'],['10.0.0.0 8 le 32','10开头的所有路由'],['0.0.0.0 0 le 32','所有路由'],['0.0.0.0 0','只有默认路由'],['172.16.16.0 20 ge 21 le 24','2+4+8+16=30条']),
 '[R1] ip ip-prefix DENY24 index 10 permit 192.168.0.0 16 greater-equal 24 less-equal 24\n[R1] route-policy RP deny node 10\n[R1-route-policy] if-match ip-prefix DENY24\n[R1] route-policy RP permit node 20      # 放行其余，否则全部被拒\n[R1] ospf 1\n[R1-ospf-1] import-route static route-policy RP',
 ['ip-prefix能匹配多少条路由的计算题（真题）。','route-policy隐含拒绝。'])
d('dt-vrrp','PC只能写一个网关，网关坏了全员断网。VRRP让两台路由器"合伙"用一个虚拟IP和虚拟MAC，平时Master干活，Backup盯着；Master停止发通告，Backup就接管，PC完全无感知。',
 ['同一VRID的路由器互发VRRP通告，比较优先级，高者成为Master（相同比接口IP，大者优）。','Master回应虚拟IP的ARP（用虚拟MAC），转发流量；每1秒发通告。','Backup在约3倍通告间隔内没收到通告 → 切换为Master，发免费ARP刷新交换机MAC表。','原Master恢复：抢占模式下（华为缺省）重新抢回，可设抢占延时；非抢占则不抢。','上行接口故障：track监视上行接口，降低优先级，使Backup接管。'],
 T(['参数','缺省/取值'],['优先级','100（1–254可配，255给IP拥有者，0表示放弃）'],['通告间隔','1秒'],['抢占','开启，延时0'],['虚拟MAC','0000-5E00-01{VRID}'],['报文','IP协议号112，组播224.0.0.18']),
 '[R1] interface GigabitEthernet0/0/1\n[R1-GigabitEthernet0/0/1] ip address 10.1.1.1 24\n[R1-GigabitEthernet0/0/1] vrrp vrid 1 virtual-ip 10.1.1.254\n[R1-GigabitEthernet0/0/1] vrrp vrid 1 priority 120\n[R1-GigabitEthernet0/0/1] vrrp vrid 1 preempt-mode timer delay 20\n[R1-GigabitEthernet0/0/1] vrrp vrid 1 track interface GigabitEthernet0/0/2 reduced 30\n[R2] interface GigabitEthernet0/0/1\n[R2-GigabitEthernet0/0/1] ip address 10.1.1.2 24\n[R2-GigabitEthernet0/0/1] vrrp vrid 1 virtual-ip 10.1.1.254\n[R1] display vrrp brief',
 ['抢占/非抢占场景题（真题）。','虚拟MAC计算、优先级取值。','联动上行接口。'],['f_vrrp'])
d('dt-acl','ACL是一张"条件清单"，本身不做事，被谁调用就为谁服务：接口过滤（traffic-filter）用它决定放行/丢弃，NAT用它选哪些地址要转换，路由策略用它挑路由。',
 ['确定要匹配什么：只看源IP用基本ACL；还要看目的、协议、端口用高级ACL。','写规则：rule编号 permit/deny 条件（地址用通配符）。','按编号从小到大匹配，命中即停。','应用：接口下 traffic-filter inbound/outbound acl N。','traffic-filter缺省放行未匹配报文 → 想白名单要在最后加 rule deny ip。'],
 T(['类型','编号','可匹配'],['基本ACL','2000–2999','源IP'],['高级ACL','3000–3999','源/目的IP、协议、端口、TCP标志等'],['二层ACL','4000–4999','MAC、VLAN、以太类型'],['用户ACL','6000–6999','UCL组等']),
 '# 禁止192.168.1.0/24访问服务器10.1.1.10的Web，其他放行\n[R1] acl 3000\n[R1-acl-adv-3000] rule 5 deny tcp source 192.168.1.0 0.0.0.255 destination 10.1.1.10 0 destination-port eq 80\n[R1] interface GigabitEthernet0/0/0\n[R1-GigabitEthernet0/0/0] traffic-filter inbound acl 3000\n# 未匹配的报文缺省放行，因此不需要rule permit ip',
 ['编号范围、通配符含义。','按顺序匹配的结果判断。','华为traffic-filter缺省动作（已核实：permit）。'])
d('dt-nat','公网IPv4地址很少，公司内部用私网地址。NAT在出口把"内部地址"换成"公网地址"，并把对应关系记在NAT表里，回来的报文再换回去。NAPT连端口一起换，一个公网IP就能让上千台电脑上网。',
 ['内网报文到达出口，匹配ACL确定需要转换。','从地址池（或出接口地址）选公网IP，NAPT还分配一个新的源端口。','记录NAT表项：私网IP:端口 ↔ 公网IP:端口。','回程报文查NAT表还原目的地址和端口，转发给内网主机。','NAT Server反过来：外网访问公网IP:端口时，静态映射到内网服务器。'],
 T(['方式','转换内容','特点'],['静态NAT','一对一地址','固定'],['动态NAT(No-PAT)','地址池一对一','不转端口，公网地址用完即不能上网'],['NAPT','地址+端口','多对一'],['Easy IP','出接口地址+端口','拨号/动态公网IP'],['NAT Server','公网IP:端口→内网服务器','外网主动访问内网']),
 '[R1] acl 2000\n[R1-acl-basic-2000] rule 5 permit source 192.168.1.0 0.0.0.255\n[R1] interface GigabitEthernet0/0/1\n[R1-GigabitEthernet0/0/1] nat outbound 2000          # Easy IP\n[R1-GigabitEthernet0/0/1] nat server protocol tcp global current-interface 8080 inside 192.168.1.10 80\n[R1] display nat session all',
 ['根据场景选NAT方式。','no-pat含义。','NAT Server用途。'],['f_nat'])
d('dt-dhcp','新电脑接入网络什么都不知道，DHCP像前台："你好，我需要一个地址"(Discover) → "给你这个可以吗"(Offer) → "好，就要这个"(Request) → "登记好了，租期1天"(ACK)。',
 ['客户端广播Discover（源IP 0.0.0.0，目的255.255.255.255）。','服务器从地址池挑一个地址，Offer给客户端（多台服务器都会回）。','客户端选第一个Offer，广播Request（让其他服务器知道没选它们）。','服务器回ACK，客户端可做免费ARP检测冲突，冲突则发Decline。','租期50%单播续约，87.5%广播续约，到期释放。跨网段由中继(dhcp select relay)转发。'],
 T(['报文','方向','作用'],['Discover','C→S广播','寻找服务器'],['Offer','S→C','提供地址'],['Request','C→S','请求/续约'],['ACK/NAK','S→C','确认/拒绝'],['Release','C→S','释放'],['Decline','C→S','地址冲突']),
 '[SW1] dhcp enable\n[SW1] ip pool vlan10\n[SW1-ip-pool-vlan10] network 192.168.10.0 mask 24\n[SW1-ip-pool-vlan10] gateway-list 192.168.10.254\n[SW1-ip-pool-vlan10] dns-list 114.114.114.114\n[SW1-ip-pool-vlan10] excluded-ip-address 192.168.10.200 192.168.10.253\n[SW1] interface Vlanif10\n[SW1-Vlanif10] dhcp select global\n# 中继：\n[SW2-Vlanif20] dhcp select relay\n[SW2-Vlanif20] dhcp relay server-ip 10.1.1.1',
 ['四步报文顺序、端口号。','续约时间点。','中继场景、Option 43（WLAN）。'],['f_dhcp'])
d('dt-ipv6','IPv6把地址从32位扩到128位，多到可以给地球上每粒沙子分地址。它取消了广播，用组播和ND协议来做ARP、发现网关和自动配置；主机可以只靠路由器的RA自己"拼"出地址（SLAAC）。',
 ['接口启用IPv6后自动生成链路本地地址FE80::/64+接口ID。','做DAD：发NS询问该地址是否被占用。','发RS请求前缀，路由器回RA（含前缀、是否用DHCPv6的M/O标志）。','用前缀+接口ID（EUI-64或随机）生成全球单播地址。','通信时用NS/NA解析邻居链路层地址。'],
 T(['类型','前缀','说明'],['全球单播GUA','2000::/3','公网'],['链路本地LLA','FE80::/10','只在本链路，路由协议下一跳常用'],['唯一本地ULA','FC00::/7','类似私网'],['组播','FF00::/8','FF02::1所有节点、FF02::2所有路由器'],['环回','::1/128','—'],['未指定','::/128','—']),
 '[R1] ipv6\n[R1] interface GigabitEthernet0/0/1\n[R1-GigabitEthernet0/0/1] ipv6 enable\n[R1-GigabitEthernet0/0/1] ipv6 address 2001:DB8:1::1 64\n[R1-GigabitEthernet0/0/1] undo ipv6 nd ra halt     # 允许发RA\n[R1] ospfv3 1\n[R1-ospfv3-1] router-id 1.1.1.1\n[R1-GigabitEthernet0/0/1] ospfv3 1 area 0\n[R1] display ipv6 interface brief',
 ['地址缩写合法性判断。','地址类型前缀。','ICMPv6报文类型号及作用。','EUI-64计算。'],['f_ipv6'])
d('dt-mplsvpn','运营商要给很多企业建"专线"，不同企业的私网地址可能都用10.0.0.0，混在一起会冲突。MPLS VPN在PE上给每家企业一张独立路由表(VRF)；路由在运营商网络里传播时，前面加上RD变得独一无二，再贴上RT"收件标签"决定被哪家企业的VRF接收；转发时用两层标签，外层负责在运营商网里送到对端PE，内层告诉PE交给哪个VRF。',
 ['CE把路由通过静态/OSPF/BGP给PE，PE存进对应VRF。','PE给路由加RD变成VPNv4路由，附加export RT和私网标签，通过MP-BGP发给对端PE。','对端PE检查RT：与本地VRF的import RT匹配才导入。','PE把路由发给CE2。','数据转发：PE1压入内层私网标签+外层LDP标签，P只交换外层，PE2（或倒数第二跳弹出外层后）按内层标签找到VRF转发。'],
 T(['跨域方案','ASBR之间','ASBR上VRF','扩展性'],['Option A','普通IP，互为CE（每VPN一个子接口）','需要','差，最简单'],['Option B','MP-EBGP传VPNv4，接口使能MPLS','不需要（undo policy vpn-target）','较好'],['Option C','PE之间多跳MP-EBGP传VPNv4','不需要','最好，较复杂']),
 '[PE1] ip vpn-instance A\n[PE1-vpn-instance-A] ipv4-family\n[PE1-vpn-instance-A-af-ipv4] route-distinguisher 100:1\n[PE1-vpn-instance-A-af-ipv4] vpn-target 100:1 export-extcommunity\n[PE1-vpn-instance-A-af-ipv4] vpn-target 100:1 import-extcommunity\n[PE1] interface GigabitEthernet0/0/2\n[PE1-GigabitEthernet0/0/2] ip binding vpn-instance A\n[PE1-GigabitEthernet0/0/2] ip address 192.168.1.1 24\n[PE1] bgp 100\n[PE1-bgp] peer 3.3.3.3 as-number 100\n[PE1-bgp] peer 3.3.3.3 connect-interface LoopBack0\n[PE1-bgp] ipv4-family vpnv4\n[PE1-bgp-af-vpnv4] peer 3.3.3.3 enable',
 ['RD与RT的作用区别（真题必考）。','跨域Option A/B/C中ASBR要配什么（真题）。','标签头各字段位数。'],['f_mpls'])
d('dt-ext','这三个是进阶话题，零基础先抓"概念+一个结论"：SRv6=用IPv6地址写路径；组播=一份流量发给一组人；IP FRR=提前算好备胎路径。',
 ['SRv6：头节点把路径写成一串SID放进SRH，每到一个节点执行对应指令（End、End.X），SL指针减1。','PIM-SM：接收者经IGMP加入 → 最后一跳路由器向RP建立共享树(RPT) → 源的第一跳路由器向RP注册 → 可切换到最短路径树(SPT)。','LFA：对每个目的预先找满足不等式的邻居作为备份下一跳，主链路故障时直接切换，再等IGP收敛。'],
 T(['技术','一句话'],['SRv6 End SID','表示节点，执行SL-1并更新目的地址'],['End.X SID','从指定三层链路转发'],['Binding SID','代表一段SR Policy，缩短Segment List'],['IGMP','主机与路由器之间的组成员管理'],['PIM-SM','需RP，适合接收者稀疏'],['BFD','毫秒级检测故障']),
 '',['Segment List里能放什么（真题）。','RP选举规则（真题：组范围掩码最长 → 优先级小 → Hash大 → 地址大）。','LFA不等式计算（真题）。'])
