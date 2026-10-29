# 华为ICT大赛·网络赛道 17天备考站（离线版）

## 使用
- 直接双击 `index.html` 即可（数据已内联在 `js/data.js`，无需联网/后端）。
- 或在本目录运行 `python3 -m http.server 8000`，浏览器打开 http://localhost:8000 。
- 进度、错题、收藏、成绩、打卡都保存在本浏览器 localStorage（换浏览器/清缓存会丢失）。“统计”页可一键清空。
- 右上角 🌓 切换深色模式。

## 目录
- `index.html` / `css/style.css` / `js/app.js`（界面与逻辑）/ `js/guide.js`（备考指南）
- `js/data.js`：自动生成，包含 `window.KPS`（讲义）和 `window.QUESTIONS`（题库）
- `data/knowledge.json`、`data/questions.json`：同样的数据（JSON版）
- `tools/`：数据源与脚本：`kp_dt.py`（数通讲义+自编题）、`kp_other.py`（DCN/安全/WLAN）、`real.py`（技术栈回忆题）、`build.py`（生成JSON和data.js）、`validate.py`（校验）

## 新增题目
推荐方式（改源再生成）：
1. 自编题：在 `tools/kp_*.py` 对应知识点的题目列表里加一行，例如
   `S('题干',['选项A','选项B','选项C','选项D'],'B','解析')`；判断题 `J('题干',True,'解析')`；多选 `M('题干',[...],'ACD','解析')`。
2. 外部来源题：仿照 `tools/real.py` 的 `r(...)`，写明 `source_url`、edition、stage、credibility（官方|回忆|题库|自编）和所属知识点 `kp`。
3. 运行 `cd tools && python3 build.py && cd .. && python3 tools/validate.py`。

直接编辑 JSON 也可以，但改完要同步生成 `js/data.js`（`build.py` 会覆盖 JSON，所以二选一，建议以 `tools/` 为准）。

题目字段：`id, source_url, edition, stage, domain(数通|DCN|安全|WLAN), type(判断|单选|多选), stem, options[{key,text}], answer[], explanation, tags[], credibility, kp`。

## 模拟考规则
60题/60分钟，按 数通24/DCN12/安全12/WLAN12 随机抽题，某领域题不够时有多少出多少并提示“题库待扩充”。多选题全对才得分，按题数折合1000分（真实计分规则未公开）。

## 数据说明
- 回忆题19道：技术栈 https://jishuzhan.net/article/1951482261190258690（2024-2025全国总决赛高职组，网友回忆）。原文DCN第2题只有回忆概要，没有收录。部分原题有图但没保存，题干里已注明。
- 自编题153道：根据讲义编写，**不是真题**。
- 讲义里标“待核实”的地方以华为官方文档为准。
