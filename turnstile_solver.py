import requests
import time
from typing import Dict, Optional, Any, Union
import json

class TurnstileSolverError(Exception):
    """Turnstile 解决器错误基类"""
    pass

class TurnstileSolver:
    """
    Turnstile 验证码解决工具
    
    使用 CloudFreed API 解决 Turnstile 验证码，获取验证令牌
    """
    
    def __init__(
        self, 
        api_base_url: str,
        client_key: str,
        max_retries: int = 20,
        retry_interval: int = 6,
        timeout: int = 60
    ):
        """
        初始化 Turnstile 验证码解决器
        
        参数:
            api_base_url: API 基础 URL
            client_key: API 客户端密钥
            max_retries: 最大重试次数
            retry_interval: 重试间隔(秒)
            timeout: 请求超时时间(秒)
        """
        self.create_task_url = f"{api_base_url}/createTask"
        self.get_result_url = f"{api_base_url}/getTaskResult"
        self.client_key = client_key
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.timeout = timeout
    
    def solve(
        self,
        url: str,
        sitekey: str,
        action: Optional[str] = None,
        user_agent: Optional[str] = None,
        proxy: Optional[Dict[str, Union[str, int]]] = None,
        verbose: bool = False
    ) -> str:
        """
        解决 Turnstile 验证并返回令牌
        
        参数:
            url: 目标网站 URL
            sitekey: Turnstile sitekey
            action: 可选的 action 参数
            user_agent: 自定义 User-Agent
            proxy: 代理配置 {"scheme": "http", "host": "127.0.0.1", "port": 8080}
            verbose: 是否打印详细日志
            
        返回:
            验证令牌字符串
            
        异常:
            TurnstileSolverError: 解决验证码时出错
        """
        if verbose:
            print("正在创建 Turnstile 验证任务...")
            
        payload_dict = {
            "clientKey": self.client_key,
            "type": "Turnstile",
            "url": url,
            "siteKey": sitekey 
        }
        
        if proxy:
            payload_dict["proxy"] = proxy
            
        payload = json.dumps(payload_dict)
            
        try:
            # 创建任务
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.create_task_url, 
                data=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            if verbose:
                print(f"创建任务状态码: {response.status_code}")
                print(f"创建任务响应内容: {response.json()}")
                
            result = response.json()
            task_id = result.get('taskId')
            
            if not task_id:
                raise TurnstileSolverError("未能获取到taskId")
                
            # 准备获取结果参数
            result_payload_dict = {
                "clientKey": self.client_key,
                "taskId": task_id
            }

            # 转换为字符串形式的JSON
            result_payload = json.dumps(result_payload_dict)

            # 轮询获取结果
            for attempt in range(1, self.max_retries + 1):
                if verbose:
                    print(f"\n正在获取 Turnstile 验证结果，尝试 {attempt}/{self.max_retries}...")
                
                result_response = requests.post(
                    self.get_result_url, 
                    data=result_payload,
                    headers=headers,
                    timeout=self.timeout
                )
                result_response.raise_for_status()
                
                if verbose:
                    print(f"获取结果状态码: {result_response.status_code}")
                    
                result_data = result_response.json()
                
                if verbose and not result_data.get('status') == 'completed':
                    print(f"获取结果响应内容: {result_data}")
                    
                # 检查任务是否完成
                if result_data.get('status') == 'completed':
                    if verbose:
                        print("Turnstile 验证成功完成!")
                        
                    # 调整令牌获取方式，处理嵌套结构
                    result_obj = result_data.get('result', {})
                    response_obj = result_obj.get('response', {})
                    
                    # 检查响应结构
                    if isinstance(response_obj, dict) and 'token' in response_obj:
                        # 新的响应格式
                        token = response_obj.get('token')
                    else:
                        # 兼容旧响应格式
                        token = response_obj
                    
                    if not token:
                        raise TurnstileSolverError("未找到验证令牌")
                    
                    if verbose:
                        print(f"验证令牌: {token[:30]}...{token[-10:]}")
                        #print(token)
                        
                    return token
                
                # 如果未完成且不是最后一次尝试，等待后重试
                if attempt < self.max_retries:
                    if verbose:
                        print(f"等待 {self.retry_interval} 秒后重试...")
                    time.sleep(self.retry_interval)
            
            raise TurnstileSolverError(f"达到最大重试次数 ({self.max_retries})，验证失败")
            
        except requests.exceptions.RequestException as e:
            raise TurnstileSolverError(f"请求错误: {e}")


""" # 简单使用示例
if __name__ == "__main__":
    # 示例用法
    api_base_url = "http://127.0.0.1:3000"
    client_key = "yowiv"
    
    solver = TurnstileSolver(
        api_base_url=api_base_url,
        client_key=client_key,
        verbose=True
    )
    try:
        token = solver.solve(
            url="https://www.nodeseek.com/signIn.html",
            sitekey="0x4AAAAAAAaNy7leGjewpVyR",
            action="login"
        )
        print("成功获取令牌！")
        print(f"令牌: {token[:30]}...{token[-10:]}")
    except TurnstileSolverError as e:
        print(f"解决 Turnstile 验证码失败: {e}") """