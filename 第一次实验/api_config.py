"""
API 配置文件
用于存储所有 AI 服务的 API 密钥和配置信息

获取 API 密钥的方法：
1. 智谱 AI (chatglm): https://open.bigmodel.cn/
   - 注册账号后，在"个人中心" -> "API 密钥管理"中创建 API Key
   - API Key 格式：xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx

2. 通义千问 (qwen): https://dashscope.aliyun.com/
   - 注册阿里云账号，在"访问控制" -> "API Key 管理"中创建
   - API Key 格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

3. 文心一言 (ernie): https://cloud.baidu.com/product/wenxinworkshop
   - 注册百度智能云账号，在"控制台" -> "应用接入"中创建应用获取
   - API Key 和 Secret Key 格式：xxxxxxxxxxxxxxxxxxxxxxxxxxx

4. 讯飞星火 (spark): https://www.xfyun.cn/
   - 注册讯飞开放平台账号，在"控制台" -> "我的应用"中创建
   - 需要 APPID、APISecret、APIKey 三个参数

5. DeepSeek: https://platform.deepseek.com/
   - 注册账号后，在"API Keys"页面创建
   - API Key 格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

# 智谱 AI 配置 (推荐，有免费额度)
ZHIPU_AI_CONFIG = {
    'api_key': 'bc707e6b382e47fa81efbab081a4c89b.f1GyejHS4P6rdZnE',  # 替换为你的智谱 AI API Key
    'model': 'glm-4',  # 可选模型：glm-4, glm-3-turbo, glm-4v(视觉)
    'base_url': 'https://open.bigmodel.cn/api/paas/v4',
}

# 通义千问配置
QWEN_CONFIG = {
    'api_key': 'YOUR_QWEN_API_KEY_HERE',  # 替换为你的通义千问 API Key
    'model': 'qwen-max',  # 可选模型：qwen-max, qwen-plus, qwen-turbo
}

# 文心一言配置
ERNIE_CONFIG = {
    'api_key': 'YOUR_ERNIE_API_KEY_HERE',  # 替换为你的文心一言 API Key
    'secret_key': 'YOUR_ERNIE_SECRET_KEY_HERE',  # 替换为 Secret Key
    'model': 'ernie-bot-4',  # 可选模型：ernie-bot-4, ernie-bot, ernie-bot-turbo
}

# 讯飞星火配置
SPARK_CONFIG = {
    'appid': 'YOUR_SPARK_APPID_HERE',
    'api_key': 'YOUR_SPARK_API_KEY_HERE',
    'api_secret': 'YOUR_SPARK_API_SECRET_HERE',
    'model': 'generalv3',  # 可选模型：general, generalv2, generalv3
}

# DeepSeek 配置（推荐，有免费额度）
DEEPSEEK_CONFIG = {
    'api_key': 'sk-25396a80e4c14f939b29a06a0fe5eb32',  # 替换为你的 DeepSeek API Key
    'model': 'deepseek-chat',  # 可选模型：deepseek-chat, deepseek-coder
    'base_url': 'https://api.deepseek.com',
}

# Ollama 本地模型配置（推荐用于本地部署）
# 使用 Ollama 运行本地大模型，无需 API Key，完全免费
# 安装 Ollama: https://ollama.ai/
# 可用模型：ollama list 查看已安装的模型
OLLAMA_CONFIG = {
    'base_url': 'http://localhost:11434',  # Ollama 默认地址
    'model': 'deepseek-r1:1.5b',  # 可选模型：deepseek-r1:1.5b, qwen2.5vl:3b 等
    'api_key': 'ollama',  # Ollama 不需要 API Key，可以填任意值
}

# 默认使用的配置
DEFAULT_PROVIDER = 'ollama'  # 可选：'zhipu', 'qwen', 'ernie', 'spark', 'deepseek', 'ollama'

# 获取配置的辅助函数
def get_config(provider=None):
    """获取指定 AI 提供商的配置"""
    if provider is None:
        provider = DEFAULT_PROVIDER
    
    config_map = {
        'zhipu': ZHIPU_AI_CONFIG,
        'qwen': QWEN_CONFIG,
        'ernie': ERNIE_CONFIG,
        'spark': SPARK_CONFIG,
        'deepseek': DEEPSEEK_CONFIG,
        'ollama': OLLAMA_CONFIG,
    }
    
    if provider not in config_map:
        raise ValueError(f"不支持的 AI 提供商：{provider}，可选值：{list(config_map.keys())}")
    
    return config_map[provider]
