"""
快速测试脚本 - 测试 AI API 调用
使用前请确保已在 api_config.py 中配置好 API 密钥
"""

from api_config import get_config
import requests

def test_zhipu_api():
    """测试智谱 AI API"""
    print("="*60)
    print("测试智谱 AI API")
    print("="*60)
    
    try:
        config = get_config('zhipu')
        
        # 检查 API Key 是否配置
        if config['api_key'] == 'YOUR_ZHIPU_API_KEY_HERE':
            print("❌ 错误：请先在 api_config.py 中配置智谱 AI 的 API Key")
            print("\n📖 获取方法：")
            print("1. 访问 https://open.bigmodel.cn/")
            print("2. 注册账号并完成实名认证")
            print("3. 在'个人中心' -> 'API 密钥管理'创建 API Key")
            print("4. 将 API Key 填入 api_config.py 中的 ZHIPU_AI_CONFIG")
            return False
        
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": config['model'],
            "messages": [
                {"role": "user", "content": "你好，请用一句话介绍你自己。"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        print("正在发送请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        ai_response = result['choices'][0]['message']['content']
        print(f"\n✅ AI 响应：{ai_response}")
        print("\n✓ 智谱 AI API 调用成功！")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误，请检查网络连接")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误：{e}")
        if e.response.status_code == 401:
            print("原因：API Key 无效或过期")
        elif e.response.status_code == 429:
            print("原因：请求频率超限或额度不足")
        return False
    except Exception as e:
        print(f"❌ 未知错误：{e}")
        return False


def test_deepseek_api():
    """测试 DeepSeek API"""
    print("\n" + "="*60)
    print("测试 DeepSeek API")
    print("="*60)
    
    try:
        config = get_config('deepseek')
        
        # 检查 API Key 是否配置
        if config['api_key'] == 'YOUR_DEEPSEEK_API_KEY_HERE':
            print("❌ 错误：请先在 api_config.py 中配置 DeepSeek 的 API Key")
            print("\n📖 获取方法：")
            print("1. 访问 https://platform.deepseek.com/")
            print("2. 注册账号")
            print("3. 在'API Keys'页面创建密钥")
            print("4. 将 API Key 填入 api_config.py 中的 DEEPSEEK_CONFIG")
            return False
        
        url = f"{config['base_url']}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": config['model'],
            "messages": [
                {"role": "user", "content": "你好，请用一句话介绍你自己。"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        print("正在发送请求...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        ai_response = result['choices'][0]['message']['content']
        print(f"\n✅ AI 响应：{ai_response}")
        print("\n✓ DeepSeek API 调用成功！")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误，请检查网络连接")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误：{e}")
        if e.response.status_code == 401:
            print("原因：API Key 无效或过期")
        elif e.response.status_code == 429:
            print("原因：请求频率超限或额度不足")
        return False
    except Exception as e:
        print(f"❌ 未知错误：{e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print(" " * 25 + "AI API 快速测试")
    print("="*80)
    
    print("\n请选择要测试的 API：")
    print("1. 智谱 AI")
    print("2. DeepSeek")
    print("3. 全部测试")
    
    choice = input("\n请输入选项 (1-3，直接回车测试全部): ").strip()
    
    if choice == '1':
        test_zhipu_api()
    elif choice == '2':
        test_deepseek_api()
    else:
        print("\n开始测试所有 API...\n")
        result1 = test_zhipu_api()
        result2 = test_deepseek_api()
        
        print("\n" + "="*80)
        print("测试总结")
        print("="*80)
        print(f"智谱 AI: {'✓ 通过' if result1 else '✗ 失败'}")
        print(f"DeepSeek: {'✓ 通过' if result2 else '✗ 失败'}")
        
        if result1 or result2:
            print("\n✅ 至少有一个 API 可用，可以开始实验了！")
        else:
            print("\n⚠️  所有 API 测试失败，请检查配置后重试。")
    
    print("="*80 + "\n")
