
import requests
from typing import Optional, Dict, Any
from .exceptions import AuthenticationError, APIError
from config import Config

class GitHubClient:
    def __init__(self, token: str, username: Optional[str] = None):
        self.token = token
        self.base_url = Config.BASE_URL
        self.headers = Config.get_headers(token)
        self.username = username or self._get_authenticated_user()
    
    def _get_authenticated_user(self) -> str:
        """获取当前认证用户信息"""
        response = self._request("GET", "/user")
        return response["login"]
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        发送 HTTP 请求的通用方法
        
        Args:
            method: HTTP 方法 (GET, POST, PUT, DELETE)
            endpoint: API 端点
            **kwargs: 其他请求参数
        
        Returns:
            响应数据
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            
            # 处理不同的响应状态码
            if response.status_code in [200, 201, 202]:
                return response.json() if response.content else None
            elif response.status_code == 204:
                return None
            elif response.status_code == 401:
                raise AuthenticationError("认证失败，请检查 Token")
            elif response.status_code == 404:
                raise APIError("资源未找到", status_code=404)
            else:
                error_data = response.json() if response.content else {}
                raise APIError(
                    f"API 请求失败: {error_data}",
                    status_code=response.status_code,
                    response=error_data
                )
        except requests.exceptions.RequestException as e:
            raise APIError(f"网络请求错误: {str(e)}")
