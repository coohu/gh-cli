
import base64
from typing import Dict
from core.client import GitHubClient

class FileManager:
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def create(self, repo_name: str, file_path: str, content: str,
               message: str, branch: str = "main") -> Dict:
        """在仓库中创建文件"""
        content_encoded = base64.b64encode(content.encode()).decode()
        data = {
            "message": message,
            "content": content_encoded,
            "branch": branch
        }
        
        result = self.client._request(
            "PUT",
            f"/repos/{self.client.username}/{repo_name}/contents/{file_path}",
            json=data
        )
        print(f"✓ 文件创建成功: {file_path}")
        return result
    
    def update(self, repo_name: str, file_path: str, content: str,
               message: str, branch: str = "main") -> Dict:
        """更新仓库中的文件"""
        # 获取文件的 SHA
        file_info = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}/contents/{file_path}",
            params={"ref": branch}
        )
        sha = file_info["sha"]
        
        # 更新文件
        content_encoded = base64.b64encode(content.encode()).decode()
        data = {
            "message": message,
            "content": content_encoded,
            "sha": sha,
            "branch": branch
        }
        
        result = self.client._request(
            "PUT",
            f"/repos/{self.client.username}/{repo_name}/contents/{file_path}",
            json=data
        )
        print(f"✓ 文件更新成功: {file_path}")
        return result
    
    def get_content(self, repo_name: str, file_path: str,
                    branch: str = "main") -> str:
        """获取文件内容"""
        response = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}/contents/{file_path}",
            params={"ref": branch}
        )
        content_encoded = response["content"]
        return base64.b64decode(content_encoded).decode()
