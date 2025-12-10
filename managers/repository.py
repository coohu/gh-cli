
from typing import Dict, List, Optional
from ..core.client import GitHubClient

class RepositoryManager:
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def create(self, name: str, description: str = "", 
               private: bool = False, auto_init: bool = True) -> Dict:
        """创建新仓库"""
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init
        }
        
        result = self.client._request("POST", "/user/repos", json=data)
        print(f"✓ 仓库创建成功: {result['html_url']}")
        return result
    
    def delete(self, repo_name: str) -> bool:
        """删除仓库"""
        self.client._request(
            "DELETE", 
            f"/repos/{self.client.username}/{repo_name}"
        )
        print(f"✓ 仓库删除成功: {repo_name}")
        return True
    
    def fork(self, owner: str, repo_name: str) -> Dict:
        """Fork 仓库"""
        result = self.client._request(
            "POST",
            f"/repos/{owner}/{repo_name}/forks"
        )
        print(f"✓ 仓库 Fork 成功: {result['html_url']}")
        print("请注意: Forking 是异步操作，可能需要一点时间才能完全可用。")
        return result
    
    def list(self, visibility: str = "all") -> List[Dict]:
        """列出用户的所有仓库"""
        params = {"visibility": visibility, "per_page": 100}
        repos = self.client._request("GET", "/user/repos", params=params)
        
        print(f"\n找到 {len(repos)} 个仓库:")
        for repo in repos:
            print(f"  - {repo['name']} ({repo['html_url']})")
        return repos
    
    def get_info(self, repo_name: str) -> Dict:
        """获取仓库详细信息"""
        repo = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}"
        )
        
        print(f"\n仓库信息:")
        print(f"  名称: {repo['name']}")
        print(f"  描述: {repo['description']}")
        print(f"  URL: {repo['html_url']}")
        print(f"  Stars: {repo['stargazers_count']}")
        print(f"  Forks: {repo['forks_count']}")
        print(f"  语言: {repo['language']}")
        print(f"  创建时间: {repo['created_at']}")
        print(f"  更新时间: {repo['updated_at']}")
        return repo

