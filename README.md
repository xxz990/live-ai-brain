# 电商直播AI大脑

目标：

建立公司专属AI助手。

功能：

1. 产品知识库
2. 直播复盘
3. 竞品分析
4. 成片审核
5. 千川素材分析

第一阶段：

实现知识库问答。

用户上传：

- PDF
- Word
- Excel

AI能够根据资料回答问题。

## 第一阶段 MVP

第一版功能：

- 本地上传直播数据表和千川数据表
- 登记飞书表格链接和百度网盘素材链接
- 生成直播复盘报告
- 生成主播话术、短视频脚本、贴片/KT板文案
- 检查常见合规风险表达

运行方式：

```powershell
D:\豆神\豆神\.tools\Python311\python.exe -m pip install -e ".[dev]"
D:\豆神\豆神\.tools\Python311\python.exe -m streamlit run src/live_ai_brain/app.py
```
