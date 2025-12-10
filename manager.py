#!/usr/bin/env python3
"""
GitHub Manager Script - 使用GitHub API操作仓库
功能：创建仓库、提交代码、管理分支、创建Issue/PR、Fork仓库等
"""

import os
import sys
import json
import base64
import argparse
from typing import Optional, Dict, List
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv() 

class GitHubManager:
    """GitHub API管理类"""
    
    def __init__(self, token: str, username: Optional[str] = None):
        """
        初始化GitHub管理器
        
        Args:
            token: GitHub Personal Access Token
            username: GitHub用户名（可选，会自动获取）
        """
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.username = username or self._get_authenticated_user()
    
    def _get_authenticated_user(self) -> str:
        """获取当前认证用户信息"""
        response = requests.get(f"{self.base_url}/user", headers=self.headers)
        if response.status_code == 200:
            return response.json()["login"]
        else:
            raise Exception(f"认证失败: {response.json()}")
    
    def create_repository(self, repo_name: str, description: str = "", 
                         private: bool = False, auto_init: bool = True) -> Dict:
        """
        创建新仓库
        
        Args:
            repo_name: 仓库名称
            description: 仓库描述
            private: 是否私有仓库
            auto_init: 是否自动初始化（创建README）
        
        Returns:
            创建的仓库信息
        """
        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": auto_init
        }
        
        response = requests.post(
            f"{self.base_url}/user/repos",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            repo_info = response.json()
            print(f"✓ 仓库创建成功: {repo_info['html_url']}")
            return repo_info
        else:
            raise Exception(f"创建仓库失败: {response.json()}")
    
    def delete_repository(self, repo_name: str) -> bool:
        """
        删除仓库
        
        Args:
            repo_name: 仓库名称
        
        Returns:
            是否删除成功
        """
        response = requests.delete(
            f"{self.base_url}/repos/{self.username}/{repo_name}",
            headers=self.headers
        )
        
        if response.status_code == 204:
            print(f"✓ 仓库删除成功: {repo_name}")
            return True
        else:
            raise Exception(f"删除仓库失败: {response.json()}")
    
    def fork_repository(self, owner: str, repo_name: str) -> Dict:
        """
        Fork一个仓库到当前认证用户
        
        Args:
            owner: 仓库的拥有者
            repo_name: 仓库名称
        
        Returns:
            创建的fork仓库信息
        """
        url = f"{self.base_url}/repos/{owner}/{repo_name}/forks"
        
        response = requests.post(
            url,
            headers=self.headers
        )
        
        # 202 Accepted 是 forking 时的正确响应
        if response.status_code == 202:
            fork_info = response.json()
            print(f"✓ 仓库Fork成功: {fork_info['html_url']}")
            print("请注意: Forking是异步操作，可能需要一点时间才能完全可用。")
            return fork_info
        else:
            raise Exception(f"Fork仓库失败: {response.json()}")
            
    def list_repositories(self, visibility: str = "all") -> List[Dict]:
        """
        列出用户的所有仓库
        
        Args:
            visibility: 可见性 (all, public, private)
        
        Returns:
            仓库列表
        """
        params = {"visibility": visibility, "per_page": 100}
        response = requests.get(
            f"{self.base_url}/user/repos",
            headers=self.headers,
            params=params
        )
        
        if response.status_code == 200:
            repos = response.json()
            print(f"\n找到 {len(repos)} 个仓库:")
            for repo in repos:
                print(f"  - {repo['name']} ({repo['html_url']})")
            return repos
        else:
            raise Exception(f"获取仓库列表失败: {response.json()}")
    
    def create_file(self, repo_name: str, file_path: str, content: str, 
                   message: str, branch: str = "main") -> Dict:
        """
        在仓库中创建文件
        
        Args:
            repo_name: 仓库名称
            file_path: 文件路径
            content: 文件内容
            message: 提交信息
            branch: 分支名称
        
        Returns:
            提交信息
        """
        # 将内容编码为base64
        content_encoded = base64.b64encode(content.encode()).decode()
        
        data = {
            "message": message,
            "content": content_encoded,
            "branch": branch
        }
        
        response = requests.put(
            f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{file_path}",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            commit_info = response.json()
            print(f"✓ 文件创建成功: {file_path}")
            return commit_info
        else:
            raise Exception(f"创建文件失败: {response.json()}")
    
    def update_file(self, repo_name: str, file_path: str, content: str, 
                   message: str, branch: str = "main") -> Dict:
        """
        更新仓库中的文件
        
        Args:
            repo_name: 仓库名称
            file_path: 文件路径
            content: 新的文件内容
            message: 提交信息
            branch: 分支名称
        
        Returns:
            提交信息
        """
        # 首先获取文件的SHA
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{file_path}",
            headers=self.headers,
            params={"ref": branch}
        )
        
        if response.status_code != 200:
            raise Exception(f"获取文件信息失败: {response.json()}")
        
        sha = response.json()["sha"]
        
        # 更新文件
        content_encoded = base64.b64encode(content.encode()).decode()
        data = {
            "message": message,
            "content": content_encoded,
            "sha": sha,
            "branch": branch
        }
        
        response = requests.put(
            f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{file_path}",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 200:
            commit_info = response.json()
            print(f"✓ 文件更新成功: {file_path}")
            return commit_info
        else:
            raise Exception(f"更新文件失败: {response.json()}")
    
    def get_file_content(self, repo_name: str, file_path: str, 
                        branch: str = "main") -> str:
        """
        获取文件内容
        
        Args:
            repo_name: 仓库名称
            file_path: 文件路径
            branch: 分支名称
        
        Returns:
            文件内容
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/contents/{file_path}",
            headers=self.headers,
            params={"ref": branch}
        )
        
        if response.status_code == 200:
            content_encoded = response.json()["content"]
            content = base64.b64decode(content_encoded).decode()
            return content
        else:
            raise Exception(f"获取文件内容失败: {response.json()}")
    
    def create_branch(self, repo_name: str, new_branch: str, 
                     from_branch: str = "main") -> Dict:
        """
        创建新分支
        
        Args:
            repo_name: 仓库名称
            new_branch: 新分支名称
            from_branch: 基于哪个分支创建
        
        Returns:
            分支信息
        """
        # 获取源分支的SHA
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/git/refs/heads/{from_branch}",
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"获取源分支失败: {response.json()}")
        
        sha = response.json()["object"]["sha"]
        
        # 创建新分支
        data = {
            "ref": f"refs/heads/{new_branch}",
            "sha": sha
        }
        
        response = requests.post(
            f"{self.base_url}/repos/{self.username}/{repo_name}/git/refs",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            branch_info = response.json()
            print(f"✓ 分支创建成功: {new_branch}")
            return branch_info
        else:
            raise Exception(f"创建分支失败: {response.json()}")
    
    def list_branches(self, repo_name: str) -> List[Dict]:
        """
        列出所有分支
        
        Args:
            repo_name: 仓库名称
        
        Returns:
            分支列表
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/branches",
            headers=self.headers
        )
        
        if response.status_code == 200:
            branches = response.json()
            print(f"\n找到 {len(branches)} 个分支:")
            for branch in branches:
                print(f"  - {branch['name']}")
            return branches
        else:
            raise Exception(f"获取分支列表失败: {response.json()}")
    
    def create_issue(self, repo_name: str, title: str, body: str = "", 
                    labels: List[str] = None) -> Dict:
        """
        创建Issue
        
        Args:
            repo_name: 仓库名称
            title: Issue标题
            body: Issue内容
            labels: 标签列表
        
        Returns:
            Issue信息
        """
        data = {
            "title": title,
            "body": body
        }
        
        if labels:
            data["labels"] = labels
        
        response = requests.post(
            f"{self.base_url}/repos/{self.username}/{repo_name}/issues",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            issue_info = response.json()
            print(f"✓ Issue创建成功: {issue_info['html_url']}")
            return issue_info
        else:
            raise Exception(f"创建Issue失败: {response.json()}")
    
    def create_pull_request(self, repo_name: str, title: str, head: str, 
                           base: str = "main", body: str = "") -> Dict:
        """
        创建Pull Request
        
        Args:
            repo_name: 仓库名称
            title: PR标题
            head: 源分支
            base: 目标分支
            body: PR描述
        
        Returns:
            PR信息
        """
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        
        response = requests.post(
            f"{self.base_url}/repos/{self.username}/{repo_name}/pulls",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            pr_info = response.json()
            print(f"✓ Pull Request创建成功: {pr_info['html_url']}")
            return pr_info
        else:
            raise Exception(f"创建Pull Request失败: {response.json()}")
    
    def list_commits(self, repo_name: str, branch: str = "main", 
                    limit: int = 10) -> List[Dict]:
        """
        列出提交历史
        
        Args:
            repo_name: 仓库名称
            branch: 分支名称
            limit: 返回数量限制
        
        Returns:
            提交列表
        """
        params = {"sha": branch, "per_page": limit}
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/commits",
            headers=self.headers,
            params=params
        )
        
        if response.status_code == 200:
            commits = response.json()
            print(f"\n最近 {len(commits)} 次提交:")
            for commit in commits:
                sha = commit["sha"][:7]
                message = commit["commit"]["message"].split('\n')[0]
                author = commit["commit"]["author"]["name"]
                date = commit["commit"]["author"]["date"]
                print(f"  {sha} - {message} ({author}, {date})")
            return commits
        else:
            raise Exception(f"获取提交历史失败: {response.json()}")
    
    def get_repository_info(self, repo_name: str) -> Dict:
        """
        获取仓库详细信息
        
        Args:
            repo_name: 仓库名称
        
        Returns:
            仓库信息
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            repo_info = response.json()
            print(f"\n仓库信息:")
            print(f"  名称: {repo_info['name']}")
            print(f"  描述: {repo_info['description']}")
            print(f"  URL: {repo_info['html_url']}")
            print(f"  Stars: {repo_info['stargazers_count']}")
            print(f"  Forks: {repo_info['forks_count']}")
            print(f"  语言: {repo_info['language']}")
            print(f"  创建时间: {repo_info['created_at']}")
            print(f"  更新时间: {repo_info['updated_at']}")
            return repo_info
        else:
            raise Exception(f"获取仓库信息失败: {response.json()}")
    
    def add_collaborator(self, repo_name: str, username: str, 
                        permission: str = "push") -> Dict:
        """
        向仓库添加协作者
        
        Args:
            repo_name: 仓库名称
            username: 要添加的GitHub用户名
            permission: 权限级别 (pull, push, admin, maintain, triage)
        
        Returns:
            操作结果信息
        """
        valid_permissions = ["pull", "push", "admin", "maintain", "triage"]
        if permission not in valid_permissions:
            raise ValueError(f"无效的权限级别。有效值: {', '.join(valid_permissions)}")
        
        data = {
            "permission": permission
        }
        
        response = requests.put(
            f"{self.base_url}/repos/{self.username}/{repo_name}/collaborators/{username}",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 201:
            print(f"✓ 成功添加协作者: {username} (权限: {permission})")
            print(f"  用户将收到邀请邮件，需要接受邀请后才能访问仓库")
            return {"status": "invited", "username": username, "permission": permission}
        elif response.status_code == 204:
            print(f"✓ 成功更新协作者权限: {username} (权限: {permission})")
            return {"status": "updated", "username": username, "permission": permission}
        else:
            error_msg = response.json()
            raise Exception(f"添加协作者失败: {error_msg}")
    
    def list_collaborators(self, repo_name: str) -> List[Dict]:
        """
        列出仓库的所有协作者
        
        Args:
            repo_name: 仓库名称
        
        Returns:
            协作者列表
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/collaborators",
            headers=self.headers
        )
        
        if response.status_code == 200:
            collaborators = response.json()
            print(f"\n找到 {len(collaborators)} 个协作者:")
            for collab in collaborators:
                print(f"  - {collab['login']} (权限: {collab.get('permissions', {})})")
            return collaborators
        else:
            raise Exception(f"获取协作者列表失败: {response.json()}")
    
    def remove_collaborator(self, repo_name: str, username: str) -> bool:
        """
        从仓库移除协作者
        
        Args:
            repo_name: 仓库名称
            username: 要移除的GitHub用户名
        
        Returns:
            是否移除成功
        """
        response = requests.delete(
            f"{self.base_url}/repos/{self.username}/{repo_name}/collaborators/{username}",
            headers=self.headers
        )
        
        if response.status_code == 204:
            print(f"✓ 成功移除协作者: {username}")
            return True
        else:
            raise Exception(f"移除协作者失败: {response.json()}")
    
    # ==================== Workflow 管理功能 ====================
    
    def list_workflows(self, repo_name: str) -> List[Dict]:
        """
        列出仓库的所有 workflows
        
        Args:
            repo_name: 仓库名称
        
        Returns:
            workflow 列表
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/workflows",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            workflows = data.get("workflows", [])
            print(f"\n找到 {len(workflows)} 个 Workflow:")
            for wf in workflows:
                state_icon = "✓" if wf["state"] == "active" else "○"
                print(f"  {state_icon} [{wf['id']}] {wf['name']}")
                print(f"      路径: {wf['path']}")
                print(f"      状态: {wf['state']}")
            return workflows
        else:
            raise Exception(f"获取 Workflow 列表失败: {response.json()}")
    
    def get_workflow(self, repo_name: str, workflow_id: str) -> Dict:
        """
        获取特定 workflow 的详细信息
        
        Args:
            repo_name: 仓库名称
            workflow_id: Workflow ID 或文件名
        
        Returns:
            workflow 信息
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/workflows/{workflow_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            wf = response.json()
            print(f"\nWorkflow 详情:")
            print(f"  ID: {wf['id']}")
            print(f"  名称: {wf['name']}")
            print(f"  路径: {wf['path']}")
            print(f"  状态: {wf['state']}")
            print(f"  创建时间: {wf['created_at']}")
            print(f"  更新时间: {wf['updated_at']}")
            print(f"  URL: {wf['html_url']}")
            return wf
        else:
            raise Exception(f"获取 Workflow 信息失败: {response.json()}")
    
    def list_workflow_runs(self, repo_name: str, workflow_id: Optional[str] = None,
                          status: Optional[str] = None, branch: Optional[str] = None,
                          limit: int = 10) -> List[Dict]:
        """
        列出 workflow 运行记录
        
        Args:
            repo_name: 仓库名称
            workflow_id: Workflow ID（可选，不指定则列出所有）
            status: 过滤状态 (queued, in_progress, completed)
            branch: 过滤分支
            limit: 返回数量限制
        
        Returns:
            运行记录列表
        """
        params = {"per_page": limit}
        if status:
            params["status"] = status
        if branch:
            params["branch"] = branch
        
        if workflow_id:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/actions/workflows/{workflow_id}/runs"
        else:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs"
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get("workflow_runs", [])
            print(f"\n找到 {data.get('total_count', len(runs))} 个运行记录 (显示 {len(runs)} 个):")
            for run in runs:
                status_icons = {
                    "completed": "✓" if run["conclusion"] == "success" else "✗",
                    "in_progress": "⟳",
                    "queued": "○"
                }
                icon = status_icons.get(run["status"], "?")
                conclusion = f" ({run['conclusion']})" if run.get("conclusion") else ""
                print(f"  {icon} [{run['id']}] {run['name']}")
                print(f"      状态: {run['status']}{conclusion}")
                print(f"      分支: {run['head_branch']}")
                print(f"      触发: {run['event']}")
                print(f"      时间: {run['created_at']}")
            return runs
        else:
            raise Exception(f"获取运行记录失败: {response.json()}")
    
    def get_workflow_run(self, repo_name: str, run_id: int) -> Dict:
        """
        获取特定运行的详细信息
        
        Args:
            repo_name: 仓库名称
            run_id: 运行 ID
        
        Returns:
            运行详情
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            run = response.json()
            print(f"\n运行详情:")
            print(f"  ID: {run['id']}")
            print(f"  名称: {run['name']}")
            print(f"  状态: {run['status']}")
            print(f"  结论: {run.get('conclusion', 'N/A')}")
            print(f"  分支: {run['head_branch']}")
            print(f"  SHA: {run['head_sha'][:7]}")
            print(f"  触发事件: {run['event']}")
            print(f"  触发者: {run['actor']['login']}")
            print(f"  创建时间: {run['created_at']}")
            print(f"  更新时间: {run['updated_at']}")
            print(f"  URL: {run['html_url']}")
            return run
        else:
            raise Exception(f"获取运行详情失败: {response.json()}")
    
    def trigger_workflow(self, repo_name: str, workflow_id: str, 
                        ref: str = "main", inputs: Optional[Dict] = None) -> bool:
        """
        手动触发 workflow 运行
        
        Args:
            repo_name: 仓库名称
            workflow_id: Workflow ID 或文件名
            ref: 分支或标签名
            inputs: workflow 输入参数
        
        Returns:
            是否触发成功
        """
        data = {"ref": ref}
        if inputs:
            data["inputs"] = inputs
        
        response = requests.post(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/workflows/{workflow_id}/dispatches",
            headers=self.headers,
            json=data
        )
        
        if response.status_code == 204:
            print(f"✓ Workflow 触发成功")
            print(f"  Workflow: {workflow_id}")
            print(f"  分支: {ref}")
            if inputs:
                print(f"  输入参数: {json.dumps(inputs, ensure_ascii=False)}")
            return True
        else:
            raise Exception(f"触发 Workflow 失败: {response.json()}")
    
    def cancel_workflow_run(self, repo_name: str, run_id: int) -> bool:
        """
        取消正在运行的 workflow
        
        Args:
            repo_name: 仓库名称
            run_id: 运行 ID
        
        Returns:
            是否取消成功
        """
        response = requests.post(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}/cancel",
            headers=self.headers
        )
        
        if response.status_code == 202:
            print(f"✓ 已请求取消运行: {run_id}")
            return True
        else:
            raise Exception(f"取消运行失败: {response.json()}")
    
    def rerun_workflow(self, repo_name: str, run_id: int, 
                      failed_only: bool = False) -> bool:
        """
        重新运行 workflow
        
        Args:
            repo_name: 仓库名称
            run_id: 运行 ID
            failed_only: 是否只重新运行失败的 jobs
        
        Returns:
            是否成功
        """
        if failed_only:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}/rerun-failed-jobs"
        else:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}/rerun"
        
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 201:
            mode = "失败的 jobs" if failed_only else "全部"
            print(f"✓ 已触发重新运行 ({mode}): {run_id}")
            return True
        else:
            raise Exception(f"重新运行失败: {response.json()}")
    
    def get_workflow_run_logs(self, repo_name: str, run_id: int, 
                             output_file: Optional[str] = None) -> str:
        """
        下载 workflow 运行日志
        
        Args:
            repo_name: 仓库名称
            run_id: 运行 ID
            output_file: 输出文件路径（可选）
        
        Returns:
            日志下载 URL 或保存路径
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}/logs",
            headers=self.headers,
            allow_redirects=False
        )
        
        if response.status_code == 302:
            download_url = response.headers.get("Location")
            
            if output_file:
                # 下载并保存日志
                log_response = requests.get(download_url)
                with open(output_file, "wb") as f:
                    f.write(log_response.content)
                print(f"✓ 日志已保存到: {output_file}")
                return output_file
            else:
                print(f"✓ 日志下载链接:")
                print(f"  {download_url}")
                return download_url
        else:
            raise Exception(f"获取日志失败: {response.json()}")
    
    def list_workflow_jobs(self, repo_name: str, run_id: int) -> List[Dict]:
        """
        列出 workflow 运行中的所有 jobs
        
        Args:
            repo_name: 仓库名称
            run_id: 运行 ID
        
        Returns:
            jobs 列表
        """
        response = requests.get(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}/jobs",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"\n运行 {run_id} 包含 {len(jobs)} 个 Job:")
            for job in jobs:
                status_icons = {
                    "completed": "✓" if job["conclusion"] == "success" else "✗",
                    "in_progress": "⟳",
                    "queued": "○"
                }
                icon = status_icons.get(job["status"], "?")
                conclusion = f" ({job['conclusion']})" if job.get("conclusion") else ""
                print(f"  {icon} [{job['id']}] {job['name']}")
                print(f"      状态: {job['status']}{conclusion}")
                if job.get("started_at"):
                    print(f"      开始: {job['started_at']}")
                if job.get("completed_at"):
                    print(f"      完成: {job['completed_at']}")
                
                # 显示步骤
                steps = job.get("steps", [])
                if steps:
                    print(f"      步骤:")
                    for step in steps:
                        step_icon = "✓" if step["conclusion"] == "success" else ("✗" if step["conclusion"] == "failure" else "○")
                        print(f"        {step_icon} {step['name']}")
            return jobs
        else:
            raise Exception(f"获取 Jobs 列表失败: {response.json()}")
    
    def delete_workflow_run(self, repo_name: str, run_id: int) -> bool:
        """
        删除 workflow 运行记录
        
        Args:
            repo_name: 仓库名称
            run_id: 运行 ID
        
        Returns:
            是否删除成功
        """
        response = requests.delete(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/runs/{run_id}",
            headers=self.headers
        )
        
        if response.status_code == 204:
            print(f"✓ 运行记录已删除: {run_id}")
            return True
        else:
            raise Exception(f"删除运行记录失败: {response.json()}")
    
    def enable_workflow(self, repo_name: str, workflow_id: str) -> bool:
        """
        启用 workflow
        
        Args:
            repo_name: 仓库名称
            workflow_id: Workflow ID 或文件名
        
        Returns:
            是否成功
        """
        response = requests.put(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/workflows/{workflow_id}/enable",
            headers=self.headers
        )
        
        if response.status_code == 204:
            print(f"✓ Workflow 已启用: {workflow_id}")
            return True
        else:
            raise Exception(f"启用 Workflow 失败: {response.json()}")
    
    def disable_workflow(self, repo_name: str, workflow_id: str) -> bool:
        """
        禁用 workflow
        
        Args:
            repo_name: 仓库名称
            workflow_id: Workflow ID 或文件名
        
        Returns:
            是否成功
        """
        response = requests.put(
            f"{self.base_url}/repos/{self.username}/{repo_name}/actions/workflows/{workflow_id}/disable",
            headers=self.headers
        )
        
        if response.status_code == 204:
            print(f"✓ Workflow 已禁用: {workflow_id}")
            return True
        else:
            raise Exception(f"禁用 Workflow 失败: {response.json()}")


def main():
    """主函数 - 命令行接口"""
    parser = argparse.ArgumentParser(
        description="GitHub Manager - 使用GitHub API管理仓库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 创建仓库
  python manager.py create-repo my-project --description "我的项目" --private
  
  # Fork仓库
  python manager.py fork-repo some-owner some-repo
  
  # 列出所有仓库
  python manager.py list-repos
  
  # 创建文件
  python manager.py create-file my-project README.md "# Hello World" -m "Initial commit"
  
  # 更新文件
  python manager.py update-file my-project README.md "# Updated Content" -m "Update README"
  
  # 创建分支
  python manager.py create-branch my-project feature-branch
  
  # 创建Issue
  python manager.py create-issue my-project "Bug报告" --body "发现一个bug"
  
  # 创建PR
  python manager.py create-pr my-project "新功能" feature-branch main
  
  # 查看提交历史
  python manager.py list-commits my-project
  
  # 查看仓库信息
  python manager.py repo-info my-project
  
  # 添加协作者
  python manager.py add-collaborator my-project developer-username --permission push
  
  # 列出协作者
  python manager.py list-collaborators my-project
  
  # 移除协作者
  python manager.py remove-collaborator my-project developer-username

  # ==================== Workflow 管理 ====================
  
  # 列出所有 workflows
  python manager.py list-workflows my-project
  
  # 查看 workflow 详情
  python manager.py get-workflow my-project 12345678
  
  # 列出 workflow 运行记录
  python manager.py list-runs my-project
  python manager.py list-runs my-project --workflow 12345678 --status completed --limit 5
  
  # 查看运行详情
  python manager.py get-run my-project 9876543210
  
  # 触发 workflow 运行
  python manager.py trigger-workflow my-project ci.yml --ref main
  python manager.py trigger-workflow my-project deploy.yml --ref main --inputs '{"environment":"production"}'
  
  # 取消运行
  python manager.py cancel-run my-project 9876543210
  
  # 重新运行
  python manager.py rerun my-project 9876543210
  python manager.py rerun my-project 9876543210 --failed-only
  
  # 查看 jobs
  python manager.py list-jobs my-project 9876543210
  
  # 下载日志
  python manager.py get-logs my-project 9876543210
  python manager.py get-logs my-project 9876543210 --output logs.zip
  
  # 删除运行记录
  python manager.py delete-run my-project 9876543210
  
  # 启用/禁用 workflow
  python manager.py enable-workflow my-project ci.yml
  python manager.py disable-workflow my-project ci.yml
        """
    )
    
    parser.add_argument("--token", help="GitHub Personal Access Token (或使用环境变量 GITHUB_TOKEN)")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 创建仓库
    create_repo_parser = subparsers.add_parser("create-repo", help="创建新仓库")
    create_repo_parser.add_argument("name", help="仓库名称")
    create_repo_parser.add_argument("--description", default="", help="仓库描述")
    create_repo_parser.add_argument("--private", action="store_true", help="创建私有仓库")
    create_repo_parser.add_argument("--no-init", action="store_true", help="不自动初始化")
    
    # 删除仓库
    delete_repo_parser = subparsers.add_parser("delete-repo", help="删除仓库")
    delete_repo_parser.add_argument("name", help="仓库名称")

    # Fork仓库
    fork_repo_parser = subparsers.add_parser("fork-repo", help="Fork一个仓库")
    fork_repo_parser.add_argument("owner", help="要fork的仓库的拥有者")
    fork_repo_parser.add_argument("repo", help="要fork的仓库名称")
    
    # 列出仓库
    list_repos_parser = subparsers.add_parser("list-repos", help="列出所有仓库")
    list_repos_parser.add_argument("--visibility", choices=["all", "public", "private"], 
                                   default="all", help="仓库可见性")
    
    # 创建文件
    create_file_parser = subparsers.add_parser("create-file", help="创建文件")
    create_file_parser.add_argument("repo", help="仓库名称")
    create_file_parser.add_argument("path", help="文件路径")
    create_file_parser.add_argument("content", help="文件内容")
    create_file_parser.add_argument("-m", "--message", required=True, help="提交信息")
    create_file_parser.add_argument("--branch", default="main", help="分支名称")
    
    # 更新文件
    update_file_parser = subparsers.add_parser("update-file", help="更新文件")
    update_file_parser.add_argument("repo", help="仓库名称")
    update_file_parser.add_argument("path", help="文件路径")
    update_file_parser.add_argument("content", help="新的文件内容")
    update_file_parser.add_argument("-m", "--message", required=True, help="提交信息")
    update_file_parser.add_argument("--branch", default="main", help="分支名称")
    
    # 获取文件内容
    get_file_parser = subparsers.add_parser("get-file", help="获取文件内容")
    get_file_parser.add_argument("repo", help="仓库名称")
    get_file_parser.add_argument("path", help="文件路径")
    get_file_parser.add_argument("--branch", default="main", help="分支名称")
    
    # 创建分支
    create_branch_parser = subparsers.add_parser("create-branch", help="创建分支")
    create_branch_parser.add_argument("repo", help="仓库名称")
    create_branch_parser.add_argument("branch", help="新分支名称")
    create_branch_parser.add_argument("--from", dest="from_branch", default="main", 
                                     help="基于哪个分支创建")
    
    # 列出分支
    list_branches_parser = subparsers.add_parser("list-branches", help="列出所有分支")
    list_branches_parser.add_argument("repo", help="仓库名称")
    
    # 创建Issue
    create_issue_parser = subparsers.add_parser("create-issue", help="创建Issue")
    create_issue_parser.add_argument("repo", help="仓库名称")
    create_issue_parser.add_argument("title", help="Issue标题")
    create_issue_parser.add_argument("--body", default="", help="Issue内容")
    create_issue_parser.add_argument("--labels", nargs="+", help="标签列表")
    
    # 创建PR
    create_pr_parser = subparsers.add_parser("create-pr", help="创建Pull Request")
    create_pr_parser.add_argument("repo", help="仓库名称")
    create_pr_parser.add_argument("title", help="PR标题")
    create_pr_parser.add_argument("head", help="源分支")
    create_pr_parser.add_argument("base", help="目标分支")
    create_pr_parser.add_argument("--body", default="", help="PR描述")
    
    # 列出提交
    list_commits_parser = subparsers.add_parser("list-commits", help="列出提交历史")
    list_commits_parser.add_argument("repo", help="仓库名称")
    list_commits_parser.add_argument("--branch", default="main", help="分支名称")
    list_commits_parser.add_argument("--limit", type=int, default=10, help="返回数量")
    
    # 仓库信息
    repo_info_parser = subparsers.add_parser("repo-info", help="获取仓库信息")
    repo_info_parser.add_argument("repo", help="仓库名称")
    
    # 添加协作者
    add_collab_parser = subparsers.add_parser("add-collaborator", help="添加协作者")
    add_collab_parser.add_argument("repo", help="仓库名称")
    add_collab_parser.add_argument("username", help="要添加的GitHub用户名")
    add_collab_parser.add_argument("--permission", 
                                   choices=["pull", "push", "admin", "maintain", "triage"],
                                   default="push", 
                                   help="权限级别 (默认: push)")
    
    # 列出协作者
    list_collab_parser = subparsers.add_parser("list-collaborators", help="列出所有协作者")
    list_collab_parser.add_argument("repo", help="仓库名称")
    
    # 移除协作者
    remove_collab_parser = subparsers.add_parser("remove-collaborator", help="移除协作者")
    remove_collab_parser.add_argument("repo", help="仓库名称")
    remove_collab_parser.add_argument("username", help="要移除的GitHub用户名")
    
    # ==================== Workflow 管理命令 ====================
    
    # 列出 workflows
    list_workflows_parser = subparsers.add_parser("list-workflows", help="列出所有 Workflows")
    list_workflows_parser.add_argument("repo", help="仓库名称")
    
    # 获取 workflow 详情
    get_workflow_parser = subparsers.add_parser("get-workflow", help="获取 Workflow 详情")
    get_workflow_parser.add_argument("repo", help="仓库名称")
    get_workflow_parser.add_argument("workflow_id", help="Workflow ID 或文件名")
    
    # 列出运行记录
    list_runs_parser = subparsers.add_parser("list-runs", help="列出 Workflow 运行记录")
    list_runs_parser.add_argument("repo", help="仓库名称")
    list_runs_parser.add_argument("--workflow", help="Workflow ID（可选，不指定则列出所有）")
    list_runs_parser.add_argument("--status", choices=["queued", "in_progress", "completed"],
                                  help="过滤状态")
    list_runs_parser.add_argument("--branch", help="过滤分支")
    list_runs_parser.add_argument("--limit", type=int, default=10, help="返回数量 (默认: 10)")
    
    # 获取运行详情
    get_run_parser = subparsers.add_parser("get-run", help="获取运行详情")
    get_run_parser.add_argument("repo", help="仓库名称")
    get_run_parser.add_argument("run_id", type=int, help="运行 ID")
    
    # 触发 workflow
    trigger_workflow_parser = subparsers.add_parser("trigger-workflow", help="手动触发 Workflow")
    trigger_workflow_parser.add_argument("repo", help="仓库名称")
    trigger_workflow_parser.add_argument("workflow_id", help="Workflow ID 或文件名")
    trigger_workflow_parser.add_argument("--ref", default="main", help="分支或标签名 (默认: main)")
    trigger_workflow_parser.add_argument("--inputs", help="输入参数 (JSON 格式)")
    
    # 取消运行
    cancel_run_parser = subparsers.add_parser("cancel-run", help="取消正在运行的 Workflow")
    cancel_run_parser.add_argument("repo", help="仓库名称")
    cancel_run_parser.add_argument("run_id", type=int, help="运行 ID")
    
    # 重新运行
    rerun_parser = subparsers.add_parser("rerun", help="重新运行 Workflow")
    rerun_parser.add_argument("repo", help="仓库名称")
    rerun_parser.add_argument("run_id", type=int, help="运行 ID")
    rerun_parser.add_argument("--failed-only", action="store_true", help="只重新运行失败的 jobs")
    
    # 列出 jobs
    list_jobs_parser = subparsers.add_parser("list-jobs", help="列出运行中的所有 Jobs")
    list_jobs_parser.add_argument("repo", help="仓库名称")
    list_jobs_parser.add_argument("run_id", type=int, help="运行 ID")
    
    # 获取日志
    get_logs_parser = subparsers.add_parser("get-logs", help="下载运行日志")
    get_logs_parser.add_argument("repo", help="仓库名称")
    get_logs_parser.add_argument("run_id", type=int, help="运行 ID")
    get_logs_parser.add_argument("--output", "-o", help="输出文件路径")
    
    # 删除运行记录
    delete_run_parser = subparsers.add_parser("delete-run", help="删除运行记录")
    delete_run_parser.add_argument("repo", help="仓库名称")
    delete_run_parser.add_argument("run_id", type=int, help="运行 ID")
    
    # 启用 workflow
    enable_workflow_parser = subparsers.add_parser("enable-workflow", help="启用 Workflow")
    enable_workflow_parser.add_argument("repo", help="仓库名称")
    enable_workflow_parser.add_argument("workflow_id", help="Workflow ID 或文件名")
    
    # 禁用 workflow
    disable_workflow_parser = subparsers.add_parser("disable-workflow", help="禁用 Workflow")
    disable_workflow_parser.add_argument("repo", help="仓库名称")
    disable_workflow_parser.add_argument("workflow_id", help="Workflow ID 或文件名")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 获取GitHub Token
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("错误: 请提供GitHub Token (使用 --token 参数或设置 GITHUB_TOKEN 环境变量)")
        sys.exit(1)
    
    try:
        # 初始化GitHub管理器
        gh = GitHubManager(token)
        print(f"已认证用户: {gh.username}\n")
        
        # 执行命令
        if args.command == "create-repo":
            gh.create_repository(
                args.name, 
                args.description, 
                args.private, 
                not args.no_init
            )
        
        elif args.command == "delete-repo":
            confirm = input(f"确定要删除仓库 '{args.name}' 吗? (yes/no): ")
            if confirm.lower() == "yes":
                gh.delete_repository(args.name)
            else:
                print("已取消")
        
        elif args.command == "fork-repo":
            gh.fork_repository(args.owner, args.repo)

        elif args.command == "list-repos":
            gh.list_repositories(args.visibility)
        
        elif args.command == "create-file":
            gh.create_file(args.repo, args.path, args.content, args.message, args.branch)
        
        elif args.command == "update-file":
            gh.update_file(args.repo, args.path, args.content, args.message, args.branch)
        
        elif args.command == "get-file":
            content = gh.get_file_content(args.repo, args.path, args.branch)
            print(f"\n文件内容 ({args.path}):\n")
            print(content)
        
        elif args.command == "create-branch":
            gh.create_branch(args.repo, args.branch, args.from_branch)
        
        elif args.command == "list-branches":
            gh.list_branches(args.repo)
        
        elif args.command == "create-issue":
            gh.create_issue(args.repo, args.title, args.body, args.labels)
        
        elif args.command == "create-pr":
            gh.create_pull_request(args.repo, args.title, args.head, args.base, args.body)
        
        elif args.command == "list-commits":
            gh.list_commits(args.repo, args.branch, args.limit)
        
        elif args.command == "repo-info":
            gh.get_repository_info(args.repo)
        
        elif args.command == "add-collaborator":
            gh.add_collaborator(args.repo, args.username, args.permission)
        
        elif args.command == "list-collaborators":
            gh.list_collaborators(args.repo)
        
        elif args.command == "remove-collaborator":
            gh.remove_collaborator(args.repo, args.username)
        
        # ==================== Workflow 命令处理 ====================
        
        elif args.command == "list-workflows":
            gh.list_workflows(args.repo)
        
        elif args.command == "get-workflow":
            gh.get_workflow(args.repo, args.workflow_id)
        
        elif args.command == "list-runs":
            gh.list_workflow_runs(
                args.repo,
                workflow_id=args.workflow,
                status=args.status,
                branch=args.branch,
                limit=args.limit
            )
        
        elif args.command == "get-run":
            gh.get_workflow_run(args.repo, args.run_id)
        
        elif args.command == "trigger-workflow":
            inputs = None
            if args.inputs:
                try:
                    inputs = json.loads(args.inputs)
                except json.JSONDecodeError:
                    print("错误: --inputs 参数必须是有效的 JSON 格式")
                    sys.exit(1)
            gh.trigger_workflow(args.repo, args.workflow_id, args.ref, inputs)
        
        elif args.command == "cancel-run":
            gh.cancel_workflow_run(args.repo, args.run_id)
        
        elif args.command == "rerun":
            gh.rerun_workflow(args.repo, args.run_id, args.failed_only)
        
        elif args.command == "list-jobs":
            gh.list_workflow_jobs(args.repo, args.run_id)
        
        elif args.command == "get-logs":
            gh.get_workflow_run_logs(args.repo, args.run_id, args.output)
        
        elif args.command == "delete-run":
            confirm = input(f"确定要删除运行记录 '{args.run_id}' 吗? (yes/no): ")
            if confirm.lower() == "yes":
                gh.delete_workflow_run(args.repo, args.run_id)
            else:
                print("已取消")
        
        elif args.command == "enable-workflow":
            gh.enable_workflow(args.repo, args.workflow_id)
        
        elif args.command == "disable-workflow":
            gh.disable_workflow(args.repo, args.workflow_id)
        
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
