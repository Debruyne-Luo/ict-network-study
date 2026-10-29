import json
def t(title,head,rows,note=''):
    h=f'<div class="card"><h3>{title}</h3><div class="tw"><table><tr>'+''.join(f'<th>{x}</th>' for x in head)+'</tr>'
    h+=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table></div>'
    return h+(f'<p class="mut">{note}</p>' if note else '')+'</div>'
H='<div class="card"><h2>⚡ 速记卡 / 公式</h2><p class="mut">考前最后一天通读。数值均为标准协议值或华为文档缺省值；版本不同可能有差异，以设备文档为准。</p></div>'
H+=t('子网划分速算',['前缀','掩码','块大小','可用主机'],[[f'/{p}',f'255.255.255.{256-2**(32-p)}',2**(32-p),2**(32-p)-2] for p in range(24,31)],'公式：可用主机=2^主机位−2；子网数=2^借位；网络地址=块大小整数倍；广播=下一网段−1；/31点到点可用2个（RFC 3021）。')
H+=t('华为路由协议缺省优先级（越小越优）',['协议','优先级'],[['直连','0'],['OSPF内部','10'],['IS-IS','15'],['静态','60'],['RIP','100'],['OSPF ASE/NSSA','150'],['IBGP/EBGP','255']])
H+=t('常见端口号',['协议','端口'],[['FTP','TCP 20/21'],['SSH / Telnet','TCP 22 / 23'],['SMTP','TCP 25'],['DNS','UDP/TCP 53'],['DHCP 服务器/客户端','UDP 67 / 68'],['TFTP','UDP 69'],['HTTP / HTTPS','TCP 80 / 443'],['SNMP / Trap','UDP 161 / 162'],['BGP','TCP 179'],['IKE / NAT-T','UDP 500 / 4500'],['RIP','UDP 520'],['RADIUS 认证/计费','UDP 1812 / 1813'],['VXLAN','UDP 4789'],['CAPWAP 控制/数据','UDP 5246 / 5247'],['BFD 单跳','UDP 3784']])
H+=t('IP协议号',['协议','号'],[['ICMP','1'],['IGMP','2'],['TCP','6'],['UDP','17'],['GRE','47'],['ESP','50'],['AH','51'],['ICMPv6','58'],['OSPF','89'],['PIM','103'],['VRRP','112']])
H+=t('华为常用缺省值',['参数','缺省'],[['STP桥优先级','32768（步长4096）'],['STP Hello/FwdDelay/MaxAge','2s / 15s / 20s'],['VRRP优先级 / 通告间隔','100 / 1s（抢占开启）'],['LACP系统/接口优先级','32768（小优）'],['iStack优先级','100（1–255，大优）'],['OSPF DR优先级','1（0不参选）'],['OSPF Hello/Dead（广播）','10s / 40s'],['BGP Local_Pref','100（大优）'],['BGP Keepalive/Hold','60s / 180s'],['C-RP优先级(IPv4)','0（小优）'],['traffic-filter未匹配','permit']])
H+=t('组播/特殊地址',['地址','含义'],[['224.0.0.5 / .6','OSPF所有路由器 / DR'],['224.0.0.18','VRRP'],['224.0.0.9','RIPv2'],['FF02::1 / FF02::2','IPv6所有节点 / 所有路由器'],['FE80::/10','IPv6链路本地'],['0000-5E00-01xx','VRRP虚拟MAC（xx=VRID）']])
H+=t('一句话对比',['A','B'],[['TCP可靠有连接','UDP快无连接'],['RD让路由唯一','RT控制导入导出'],['AH只认证(51)','ESP加密+认证(50)'],['IKE SA双向','IPSec SA单向'],['URPF严格：入口一致','URPF松散：有路由即可'],['直接转发：业务不经AC','隧道转发：业务经AC'],['M-LAG控制面独立','堆叠控制面合一'],['PFC逐跳按优先级暂停','ECN端到端通知降速']])
open('../js/cards.js','w').write('// 自动生成：python3 tools/cards.py\nwindow.CARDS_HTML='+json.dumps(H,ensure_ascii=False)+';\n')
