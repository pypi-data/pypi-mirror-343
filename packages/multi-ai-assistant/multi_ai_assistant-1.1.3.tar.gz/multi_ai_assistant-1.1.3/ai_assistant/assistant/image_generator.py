import os
import platform
import subprocess
import pyclip
import keyboard
import time
import requests

def clear_possible_char():
    """清除可能由快捷键输入的字符"""
    # 模拟按下退格键删除可能输入的字符
    keyboard.send('backspace')
    time.sleep(0.1)  # 短暂延迟确保退格键生效

def get_clipboard_content():
    """从剪贴板获取内容"""
    try:
        clipboard_data = pyclip.paste()
        if isinstance(clipboard_data, bytes):
            clipboard_content = clipboard_data.decode('utf-8', errors='replace')
        else:
            clipboard_content = str(clipboard_data)
        try:
            if '\\u' in clipboard_content:
                clipboard_content = clipboard_content.encode('utf-8').decode('unicode_escape')
        except Exception as e:
            print(f"无法还原unicode转义字符串: {e}")
            return None
        if not clipboard_content:
            print("剪贴板内容为空！")
            return None
        return clipboard_content
    except Exception as e:
        print(f"无法从剪贴板获取内容: {e}")
        return None

def send_system_notification(title, message):    
    """    
    跨平台桌面通知，优先支持Linux，自动处理root和非root用户。    
    """    
    system = platform.system()    
    if system == "Linux":        
        try:            
            if hasattr(os, "geteuid") and os.geteuid() == 0:                
                current_user = os.environ.get('SUDO_USER')                
                if current_user:                    
                    user_home = f"/home/{current_user}"                    
                    display = os.environ.get('DISPLAY', ':0')                    
                    xauthority = os.environ.get('XAUTHORITY', f"{user_home}/.Xauthority")                    
                    cmd = f"DISPLAY={display} XAUTHORITY={xauthority} notify-send '{title}' '{message}'"                    
                    subprocess.run(['su', current_user, '-c', cmd], check=True)                
                else:                    
                    print("[通知] 无法确定实际用户，通知可能无法显示")            
            else:                
                subprocess.run(['notify-send', title, message], check=True)        
        except Exception as e:            
            print(f"[通知] 发送系统通知失败: {e}")    
    else:        
        print(f"[通知] {title}: {message}")

class ImageGenerator:
    """
    通用图片生成类，兼容OpenAI和Grok（x.ai），可配置API KEY、模型名、base_url。
    优先使用Grok（XAI_API_KEY、XAI_API_URL、XAI_IMAGE_MODEL）
    若无则自动尝试OpenAI相关环境变量（OPENAI_API_KEY、OPENAI_API_BASE、OPENAI_IMAGE_MODEL）。
    支持实例化时手动传参覆盖。
    """
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None, provider: str = 'xai'):
        """
        provider: 可选 xai、openai、gemini、aliyun
        """
        provider = (provider or 'xai').lower()
        self.provider = provider
        # 各平台环境变量和默认值
        provider_config = {
            'xai': {
                'api_key_env': 'XAI_API_KEY',
                'base_url_env': 'XAI_API_URL',
                'model_env': 'XAI_IMAGE_MODEL',
                'default_url': 'https://api.xai.com/v1',
                'default_model': 'grok-2-image',
            },
            'new_api': {
                'api_key_env': 'NEW_API_KEY',
                'base_url_env': 'NEW_API_URL',
                'model_env': 'NEW_IMAGE_MODEL',
                'default_url': 'https://new.aibix.top/v1',
                'default_model': 'grok-2-image',
            },
            'openai': {
                'api_key_env': 'OPENAI_API_KEY',
                'base_url_env': 'OPENAI_API_BASE',
                'model_env': 'OPENAI_IMAGE_MODEL',
                'default_url': 'https://api.openai.com/v1',
                'default_model': 'gpt-image-1',
            },
            'gemini': {
                'api_key_env': 'GEMINI_API_KEY',
                'base_url_env': 'GEMINI_IMAGE_API_URL',
                'model_env': 'GEMINI_IMAGE_MODEL',
                'default_url': 'https://generativelanguage.googleapis.com/v1beta',
                'default_model': 'gemini-2.0-flash-exp-image-generation',
            },
            'aliyun_image': {
                'api_key_env': 'ALIYUN_API_KEY',
                'base_url_env': 'ALIYUN_IMAGE_API_URL',
                'model_env': 'ALIYUN_IMAGE_MODEL',
                'default_url': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis',
                'default_model': 'wanx2.1-t2i-turbo',
            },
        }
        conf = provider_config.get(provider, provider_config['xai'])
        self.api_key = (
            api_key or
            os.environ.get(conf['api_key_env']) or
            os.environ.get('XAI_API_KEY') 
        )
        if not self.api_key:
            raise ValueError(f'未检测到 API Key，请设置 {conf["api_key_env"]} 或 XAI_API_KEY')
        self.base_url = (
            base_url or
            os.environ.get(conf['base_url_env']) or
            conf['default_url']
        )
        self.model = (
            model or
            os.environ.get(conf['model_env']) or
            conf['default_model']
        )
        print(f"[调试] ImageGenerator 初始化: provider={self.provider}, model={self.model}, base_url={self.base_url}")
        print(f"[调试] 使用的API KEY前6位: {self.api_key[:6] if self.api_key else '无'}")

    def _check_prompt_length(self, prompt: str, max_len=1024) -> bool:
        if not prompt or not isinstance(prompt, str):
            send_system_notification("[警告]", "prompt 不能为空且必须为字符串")
            print("[错误] prompt 不能为空且必须为字符串")
            return False
        if len(prompt.encode('utf-8')) > max_len:
            warn_msg = f"描述内容过长，无法生成图片（{len(prompt.encode('utf-8'))} > {max_len}），请缩短后重试。"
            send_system_notification("[警告]", warn_msg)
            print(f"[警告] {warn_msg}")
            return False
        return True

    def _to_markdown(self, url: str) -> str:
        if not url.strip().startswith('!['):
            return f"![]({url})"
        return url

    def __call__(self):
        """
        使实例可直接作为回调用于快捷键，自动读取剪贴板并生成图片。
        """
        clear_possible_char()
        prompt = get_clipboard_content()
        if not self._check_prompt_length(prompt):
            return
        send_system_notification(f"AI绘画模型：{self.model}", f"正在生成图片: {prompt[:20]}...")
        try:
            md_url = self.generate_image(prompt, markdown=True)
            if md_url:
                pyclip.copy(md_url)
                print(f"[调试] 图片链接已复制到剪贴板: {md_url}")
                send_system_notification(f"AI绘画模型：{self.model}", "图片生成成功，链接已复制到剪贴板！")
        except Exception as e:
            err_str = str(e)
            print(f"[调试] 图片生成失败: {err_str}")
            send_system_notification(f"AI绘画模型：{self.model}", err_str)

    def generate_image(self, prompt: str, response_format: str = 'url', markdown: bool = True) -> str:
        """
        通用图片生成，自动适配 openai/xai/gemini/aliyun 等主流API，返回图片URL或base64字符串。
        response_format: 'url' 或 'b64_json'
        markdown: 返回的图片链接是否用Markdown格式包裹
        """
        if not self._check_prompt_length(prompt):
            return None
        print(f"[调试] 开始生成图片，prompt前30字: {prompt[:30]}...，response_format={response_format}")
        headers = {}
        data = {}
        url = self.base_url
        provider = self.provider
        # 注意：xai目前还不支持quality、size、style参数
        if provider in ['openai', 'xai', 'new_api']:
            url = url.rstrip('/') + "/images/generations"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }
            data = {
                'model': self.model,
                'prompt': prompt,
                'n': 1,
                'response_format': response_format
            }
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            resp_json = resp.json()
            if 'data' not in resp_json or not resp_json['data']:
                raise Exception(f"API未返回图片: {resp_json}")
            img_info = resp_json['data'][0]
            val = img_info.get('b64_json') if response_format == 'b64_json' else img_info.get('url')
            if not val:
                raise Exception(f"API未返回图片字段: {img_info}")
            print(f"[调试] 返回图片: {str(val)[:60]}...")
            return self._to_markdown(val) if markdown else val
        elif provider == 'gemini':
            # Gemini 官方API
            import base64, tempfile
            from .piclab_uploader import PiclabUploader
            url = url.rstrip('/') + f"/models/{self.model}:generateContent"
            headers = {
                'Content-Type': 'application/json',
            }
            # Gemini API参数，如需修改图片尺寸，需使用模型imagen-3.0-generate-002，同时在generationConfig中修改aspectRatio，支持1:1, 3:4, 4:3, 9:16, 16:9
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["TEXT", "IMAGE"]
                }
            }
            params = {'key': self.api_key}
            resp = requests.post(url, headers=headers, params=params, json=data, timeout=60)
            resp.raise_for_status()
            resp_json = resp.json()
            # parts 结构，图片一般在parts[1]，需遍历查找inlineData
            try:
                parts = resp_json['candidates'][0]['content']['parts']
                img_b64 = None
                for part in parts:
                    if 'inlineData' in part and 'data' in part['inlineData']:
                        img_b64 = part['inlineData']['data']
                        break
                if not img_b64:
                    raise Exception("Gemini未返回图片数据")
                print(f"[调试] Gemini返回b64前60字: {img_b64[:60]}...")
                # === 自动上传到Piclab图床 ===
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    tmp.write(base64.b64decode(img_b64))
                    tmp_path = tmp.name
                api_url = os.getenv("PICLAB_API_URL", "http://localhost:3000/api/upload")
                api_key = os.getenv("PICLAB_API_KEY", "your_api_key1")
                uploader = PiclabUploader(api_url, api_key)
                try:
                    markdown_link = uploader.upload_image(tmp_path)
                except Exception as e:
                    print(f"[调试] PiclabUploader上传失败: {e}")
                    markdown_link = None
                if markdown_link:
                    return markdown_link
                else:
                    return img_b64
            except Exception as e:
                print(f"[调试] Gemini API返回异常: {resp_json}")
                raise
        elif provider in ['aliyun', 'aliyun_image']:
            # 阿里云 DashScope 千问图片生成API，自动处理异步任务
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'X-DashScope-Async': 'enable', # 如需异步可解开
            }
            # 阿里云 API参数，如需修改图片尺寸，请修改size，默认值是1024*1024。
            #图像宽高边长的像素范围为：[512, 1440]，单位像素。可任意组合以设置不同的图像分辨率，最高可达200万像素。
            data = {
                "model": self.model,
                "input": {"prompt": prompt},
                "parameters": {"size": "1024*1024", "n": 1}
            }
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            resp_json = resp.json()
            # 先尝试直接返回图片（同步）
            if 'output' in resp_json and 'results' in resp_json['output']:
                try:
                    img_url = resp_json['output']['results'][0]['url']
                    print(f"[调试] Aliyun返回图片url: {img_url}")
                    return self._to_markdown(img_url) if markdown else img_url
                except Exception as e:
                    print(f"[调试] Aliyun API返回异常: {resp_json}")
                    raise
            # 如果是异步，自动轮询获取结果
            elif 'output' in resp_json and 'task_id' in resp_json['output']:
                task_id = resp_json['output']['task_id']
                print(f"[调试] Aliyun异步任务 task_id: {task_id}")
                query_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
                import time
                max_wait = 60  # 最长等待秒数
                interval = 2   # 轮询间隔
                waited = 0
                while waited < max_wait:
                    query_resp = requests.get(query_url, headers={'Authorization': f'Bearer {self.api_key}'}, timeout=30)
                    query_json = query_resp.json()
                    status = query_json.get('output', {}).get('task_status')
                    print(f"[调试] 轮询任务状态: {status}")
                    if status == 'SUCCEEDED':
                        try:
                            img_url = query_json['output']['results'][0]['url']
                            print(f"[调试] Aliyun异步图片url: {img_url}")
                            return self._to_markdown(img_url) if markdown else img_url
                        except Exception as e:
                            print(f"[调试] Aliyun异步API返回异常: {query_json}")
                            raise
                    elif status in ('FAILED', 'CANCELLED'):
                        raise Exception(f"Aliyun图片生成失败，状态: {status}")
                    time.sleep(interval)
                    waited += interval
                raise Exception("Aliyun图片生成超时，请稍后重试")
            else:
                print(f"[调试] Aliyun API返回异常: {resp_json}")
                raise Exception(f"Aliyun API返回异常: {resp_json}")
        else:
            raise Exception(f"不支持的provider: {provider}")

    
if __name__ == "__main__":
    import keyboard
    

    aliyun_img_gen = ImageGenerator(provider='aliyun_image', model='wanx2.1-t2i-turbo')
    gemini_img_gen = ImageGenerator(provider='gemini', model='gemini-2.0-flash-exp-image-generation')
    xai_img_gen = ImageGenerator(provider='xai', model='grok-2-image')

    keyboard.add_hotkey('f8+a', aliyun_img_gen)
    keyboard.add_hotkey('f8+g', gemini_img_gen)
    keyboard.add_hotkey('f8+x', xai_img_gen)

    print("[AI绘画] 按下 f8+a 即可使用阿里云生成图片")
    print("[AI绘画] 按下 f8+g 即可使用 Gemini 生成图片")
    print("[AI绘画] 按下 f8+x 即可使用 XAI 生成图片")
    print("[调试] 进入热键监听主循环... (Ctrl+C退出)")
    keyboard.wait()
