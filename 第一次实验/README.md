# 人工智能第一次实验 - AI 大模型 API 调用实验

## 📋 实验概述

本实验旨在通过调用主流 AI 大模型的 API，了解人工智能技术的应用，掌握 API 调用的基本方法，并对比不同 AI 模型的特点。

## 📁 文件说明

```
第一次实验/
├── api_config.py              # API 配置文件（需要填写你的 API 密钥）
├── ai_experiment.py           # 主实验程序
├── 实验报告_人工智能第一次实验.md  # 实验报告模板
├── README.md                  # 使用说明（本文件）
└── requirements.txt           # Python 依赖包列表
```

## 🚀 快速开始

### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install requests
```

### 步骤 2：获取 API 密钥

**推荐使用以下平台（有免费额度）：**

#### 智谱 AI（推荐⭐）
1. 访问：https://open.bigmodel.cn/
2. 注册账号并完成实名认证
3. 进入"个人中心" → "API 密钥管理"
4. 创建 API Key

#### DeepSeek（推荐⭐）
1. 访问：https://platform.deepseek.com/
2. 注册账号
3. 在"API Keys"页面创建密钥

### 步骤 3：配置 API 密钥

编辑 `api_config.py` 文件，填入你的 API Key：

```python
# 智谱 AI 配置
ZHIPU_AI_CONFIG = {
    'api_key': '你的智谱 AI API Key',  # 替换这里
    'model': 'glm-4',
    'base_url': 'https://open.bigmodel.cn/api/paas/v4',
}

# DeepSeek 配置
DEEPSEEK_CONFIG = {
    'api_key': '你的 DeepSeek API Key',  # 替换这里
    'model': 'deepseek-chat',
    'base_url': 'https://api.deepseek.com',
}
```

### 步骤 4：运行实验

```bash
python ai_experiment.py
```

根据提示选择 AI 提供商，然后观察实验结果。

## 📝 实验内容

实验包含 5 个任务：

1. **智能对话** - 了解人工智能发展历程
2. **文本创作** - 以"人工智能与未来生活"为题创作文本
3. **逻辑推理** - 测试 AI 的逻辑推理能力
4. **代码生成** - 让 AI 生成 Python 代码
5. **知识问答** - 测试 AI 对专业概念的理解

## 🎯 实验要求

1. 成功配置至少一个 AI 平台的 API 密钥
2. 完成所有 5 个实验任务
3. 记录实验结果（程序会自动保存为 JSON 文件）
4. 填写实验报告
5. 分析不同 AI 模型的表现差异

## 📊 实验结果

实验完成后，结果会自动保存到 JSON 文件中，文件名格式：
```
experiment_result_YYYYMMDD_HHMMSS.json
```

## 🔧 常见问题

### Q1: API 调用失败怎么办？
**A:** 检查以下几点：
- API Key 是否正确填写
- 网络连接是否正常
- API 额度是否用完
- 查看错误信息，根据提示解决

### Q2: 没有 API Key 怎么办？
**A:** 推荐使用智谱 AI 或 DeepSeek，注册后即可获得免费额度用于实验。

### Q3: 如何切换不同的 AI 模型？
**A:** 运行程序后根据提示选择对应的数字即可。

### Q4: 实验结果保存在哪里？
**A:** 结果保存在当前目录下的 JSON 文件中，文件名包含时间戳。

## 📚 学习资源

- [智谱 AI 文档](https://open.bigmodel.cn/dev/api)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [Requests 库教程](https://requests.readthedocs.io/zh_CN/latest/)
- [Python 官方文档](https://docs.python.org/zh-cn/3/)

## 📄 实验报告

完成实验后，请填写《实验报告_人工智能第一次实验.md》文档，包括：
- 实验目的
- 实验环境
- 实验原理
- 实验步骤
- 实验结果与分析
- 实验总结

## ⚠️ 注意事项

1. 妥善保管 API Key，不要上传到公开代码仓库
2. 注意 API 的调用频率限制，避免超额使用
3. 实验完成后及时保存结果
4. 遵守各平台的 API 使用条款

## 📞 技术支持

如遇到问题，请检查：
1. Python 版本是否为 3.8 及以上
2. 依赖包是否正确安装
3. API Key 配置是否正确
4. 网络连接是否正常

---

**祝你实验顺利！** 🎉
