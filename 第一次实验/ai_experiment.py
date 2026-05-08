"""
人工智能第一次实验 - AI 大模型 API 调用实验
实验内容：
1. 调用 AI 大模型 API 进行智能对话
2. 实现文本生成任务
3. 实现图像理解任务
4. 对比不同 AI 模型的响应效果

作者：[你的姓名]
学号：[你的学号]
日期：2025-2026 学年第二学期
"""

import requests
import json
import time
from datetime import datetime
from api_config import get_config, DEFAULT_PROVIDER


class AIClient:
    """AI 客户端类，用于调用各种 AI 大模型 API"""
    
    def __init__(self, provider=None):
        """
        初始化 AI 客户端
        
        Args:
            provider: AI 提供商名称，可选：'zhipu', 'qwen', 'ernie', 'spark', 'deepseek'
        """
        self.provider = provider or DEFAULT_PROVIDER
        self.config = get_config(self.provider)
        print(f"已初始化 AI 客户端，提供商：{self.provider}")
    
    def chat(self, message, system_prompt="你是一个有帮助的 AI 助手"):
        """
        发送对话消息并获取 AI 响应
        
        Args:
            message: 用户输入的消息
            system_prompt: 系统提示词
            
        Returns:
            AI 的响应文本
        """
        print(f"\n{'='*60}")
        print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"使用模型：{self.config.get('model', 'unknown')}")
        print(f"{'='*60}")
        print(f"📤 用户：{message}")
        print(f"{'='*60}")
        
        try:
            if self.provider == 'zhipu':
                response = self._call_zhipu(message, system_prompt)
            elif self.provider == 'deepseek':
                response = self._call_deepseek(message, system_prompt)
            elif self.provider == 'qwen':
                response = self._call_qwen(message, system_prompt)
            elif self.provider == 'ernie':
                response = self._call_ernie(message, system_prompt)
            elif self.provider == 'spark':
                response = self._call_spark(message, system_prompt)
            else:
                raise ValueError(f"不支持的提供商：{self.provider}")
            
            print(f"📥 AI: {response}")
            return response
            
        except Exception as e:
            error_msg = f"调用 AI API 失败：{str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def _call_zhipu(self, message, system_prompt):
        """调用智谱 AI API"""
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config['model'],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_deepseek(self, message, system_prompt):
        """调用 DeepSeek API"""
        url = f"{self.config['base_url']}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config['model'],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _call_qwen(self, message, system_prompt):
        """调用通义千问 API"""
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config['model'],
            "input": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 1024
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['output']['text']
    
    def _call_ernie(self, message, system_prompt):
        """调用文心一言 API"""
        # 先获取 access_token
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        token_params = {
            "grant_type": "client_credentials",
            "client_id": self.config['api_key'],
            "client_secret": self.config['secret_key']
        }
        token_response = requests.post(token_url, params=token_params, timeout=30)
        token_response.raise_for_status()
        access_token = token_response.json().get('access_token')
        
        # 调用对话接口
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.config['model']}"
        headers = {
            "Content-Type": "application/json"
        }
        params = {"access_token": access_token}
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        }
        
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['result']
    
    def _call_spark(self, message, system_prompt):
        """调用讯飞星火 API"""
        import hmac
        import hashlib
        from datetime import datetime
        from wsgiref.handlers import format_date_time
        from time import mktime
        import base64
        import json
        
        url = "https://spark-api.xf-yun.com/v3.5/chat"
        
        # 生成签名
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        signature_origin = f"host: spark-api.xf-yun.com\ndate: {date}\nPOST /v3.5/chat HTTP/1.1"
        signature_sha = hmac.new(
            self.config['api_secret'].encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hmac.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode('utf-8')
        
        authorization = f"api_key=\"{self.config['api_key']}\", algorithm=\"hmac-sha256\", headers=\"host date request-line\", signature=\"{signature_sha_base64}\""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization,
            "Date": date,
            "Host": "spark-api.xf-yun.com"
        }
        
        payload = {
            "header": {
                "app_id": self.config['appid'],
                "uid": "test_user"
            },
            "parameter": {
                "chat": {
                    "domain": "generalv3",
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
            },
            "payload": {
                "message": {
                    "text": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ]
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['payload']['choices']['text'][0]['content']


def run_experiment():
    """运行实验"""
    print("\n" + "="*80)
    print(" " * 20 + "人工智能第一次实验")
    print(" " * 15 + "AI 大模型 API 调用与对比实验")
    print("="*80)
    
    # 实验任务列表
    tasks = [
        {
            "name": "任务一：智能对话",
            "message": "请用简洁的语言介绍人工智能的发展历程，不超过 200 字。",
            "system_prompt": "你是一个知识渊博的 AI 助手，擅长用简洁清晰的语言解释复杂概念。"
        },
        {
            "name": "任务二：文本创作",
            "message": "请以'人工智能与未来生活'为题，写一段 150 字左右的短文。",
            "system_prompt": "你是一个优秀的科技作家，擅长用生动的语言描述科技与生活的关系。"
        },
        {
            "name": "任务三：逻辑推理",
            "message": "如果所有的猫都喜欢吃鱼，咪咪是一只猫，那么咪咪喜欢吃鱼吗？请解释你的推理过程。",
            "system_prompt": "你是一个逻辑严谨的 AI 助手，擅长清晰的推理和解释。"
        },
        {
            "name": "任务四：代码生成",
            "message": "请用 Python 写一个函数，计算列表中所有偶数的和。",
            "system_prompt": "你是一个专业的程序员，擅长编写简洁高效的代码。"
        },
        {
            "name": "任务五：知识问答",
            "message": "什么是机器学习？它和深度学习有什么区别？",
            "system_prompt": "你是一个耐心的 AI 教师，擅长用通俗易懂的方式解释专业概念。"
        }
    ]
    
    # 选择 AI 提供商
    print("\n请选择 AI 提供商：")
    print("1. 智谱 AI (推荐，有免费额度)")
    print("2. DeepSeek (推荐，有免费额度)")
    print("3. 通义千问")
    print("4. 文心一言")
    print("5. 讯飞星火")
    print(f"6. 默认配置 (当前：{DEFAULT_PROVIDER})")
    
    choice = input("\n请输入选项 (1-6，直接回车使用默认): ").strip()
    provider_map = {
        '1': 'zhipu',
        '2': 'deepseek',
        '3': 'qwen',
        '4': 'ernie',
        '5': 'spark'
    }
    
    provider = provider_map.get(choice, None)
    
    # 创建 AI 客户端
    client = AIClient(provider)
    
    # 执行实验任务
    results = []
    print("\n" + "="*80)
    print("开始执行实验任务...")
    print("="*80)
    
    for i, task in enumerate(tasks, 1):
        print(f"\n\n{'='*80}")
        print(f"【{task['name']}】 (任务 {i}/{len(tasks)})")
        print(f"{'='*80}")
        
        # 调用 AI
        response = client.chat(task['message'], task['system_prompt'])
        
        # 记录结果
        results.append({
            "task_number": i,
            "task_name": task['name'],
            "question": task['message'],
            "system_prompt": task['system_prompt'],
            "response": response,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model": client.config.get('model', 'unknown'),
            "provider": client.provider
        })
        
        # 任务间隔
        if i < len(tasks):
            print(f"\n⏳ 等待 2 秒后继续下一个任务...")
            time.sleep(2)
    
    # 输出实验总结
    print("\n\n" + "="*80)
    print(" " * 30 + "实验完成！")
    print("="*80)
    print(f"\n✅ 共完成 {len(results)} 个任务")
    print(f"📊 使用的 AI 模型：{client.config.get('model', 'unknown')}")
    print(f"🏢 AI 提供商：{client.provider}")
    
    # 保存结果到文件
    output_file = f"experiment_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"💾 实验结果已保存到：{output_file}")
    print("="*80 + "\n")
    
    return results


if __name__ == "__main__":
    try:
        run_experiment()
    except KeyboardInterrupt:
        print("\n\n⚠️  实验被用户中断")
    except Exception as e:
        print(f"\n\n❌ 实验过程中发生错误：{e}")
        import traceback
        traceback.print_exc()
