# GitHub Manager 重构指南

## 📁 新的项目结构

```
github_manager/
├── __init__.py              # 包初始化文件
├── __main__.py              # CLI 入口点
├── config.py                # 配置管理
│
├── core/                    # 核心模块
│   ├── __init__.py
│   ├── client.py           # GitHub API 基础客户端
│   └── exceptions.py       # 自定义异常定义
│
├── managers/                # 功能管理器
│   ├── __init__.py
│   ├── repository.py       # 仓库管理 (创建、删除、Fork、列表)
│   ├── file.py            # 文件操作 (创建、更新、读取)
│   ├── branch.py          # 分支管理
│   ├── issue_pr.py        # Issue 和 PR 管理
│   ├── collaborator.py    # 协作者管理
│   └── workflow.py        # GitHub Actions 管理
│
├── cli/                     # 命令行接口
│   ├── __init__.py
│   ├── parser.py          # 参数解析器
│   └── commands.py        # 命令处理器
│
└── utils/                   # 工具函数
    ├── __init__.py
    └── helpers.py         # 辅助函数
```

## 🎯 重构的核心优势

### 1. **单一职责原则**
每个模块只负责一个特定功能域，代码职责清晰：
- `RepositoryManager`: 只处理仓库相关操作
- `FileManager`: 只处理文件操作
- `WorkflowManager`: 只处理 Workflow 相关

### 2. **依赖注入**
所有 Manager 通过构造函数注入 `GitHubClient`，便于测试和替换实现

### 3. **统一的错误处理**
所有 API 调用都通过 `GitHubClient._request()` 统一处理，错误处理集中化

### 4. **易于扩展**
添加新功能只需：
1. 在 `managers/` 创建新的 Manager
2. 在 `cli/commands.py` 添加命令处理
3. 在 `cli/parser.py` 添加参数解析

### 5. **更好的可测试性**
```python
# 可以轻松进行单元测试
def test_create_repository():
    mock_client = MockGitHubClient()
    repo_manager = RepositoryManager(mock_client)
    result = repo_manager.create("test-repo")
    assert result["name"] == "test-repo"
```

## 📝 完整的文件实现建议

### managers/branch.py
```python
"""分支管理模块"""
from typing import Dict, List
from ..core.client import GitHubClient

class BranchManager:
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def create(self, repo_name: str, new_branch: str, 
               from_branch: str = "main") -> Dict:
        """创建新分支"""
        # 获取源分支的 SHA
        ref_data = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}/git/refs/heads/{from_branch}"
        )
        sha = ref_data["object"]["sha"]
        
        # 创建新分支
        data = {"ref": f"refs/heads/{new_branch}", "sha": sha}
        result = self.client._request(
            "POST",
            f"/repos/{self.client.username}/{repo_name}/git/refs",
            json=data
        )
        print(f"✓ 分支创建成功: {new_branch}")
        return result
    
    def list(self, repo_name: str) -> List[Dict]:
        """列出所有分支"""
        branches = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}/branches"
        )
        print(f"\n找到 {len(branches)} 个分支:")
        for branch in branches:
            print(f"  - {branch['name']}")
        return branches
```

### managers/issue_pr.py
```python
"""Issue 和 Pull Request 管理模块"""
from typing import Dict, List, Optional
from ..core.client import GitHubClient

class IssuePRManager:
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def create_issue(self, repo_name: str, title: str, 
                     body: str = "", labels: List[str] = None) -> Dict:
        """创建 Issue"""
        data = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        
        result = self.client._request(
            "POST",
            f"/repos/{self.client.username}/{repo_name}/issues",
            json=data
        )
        print(f"✓ Issue 创建成功: {result['html_url']}")
        return result
    
    def create_pull_request(self, repo_name: str, title: str, 
                           head: str, base: str = "main", 
                           body: str = "") -> Dict:
        """创建 Pull Request"""
        data = {"title": title, "head": head, "base": base, "body": body}
        result = self.client._request(
            "POST",
            f"/repos/{self.client.username}/{repo_name}/pulls",
            json=data
        )
        print(f"✓ Pull Request 创建成功: {result['html_url']}")
        return result
```

### managers/collaborator.py
```python
"""协作者管理模块"""
from typing import Dict, List
from ..core.client import GitHubClient

class CollaboratorManager:
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def add(self, repo_name: str, username: str, 
            permission: str = "push") -> Dict:
        """添加协作者"""
        valid_permissions = ["pull", "push", "admin", "maintain", "triage"]
        if permission not in valid_permissions:
            raise ValueError(f"无效的权限级别。有效值: {', '.join(valid_permissions)}")
        
        data = {"permission": permission}
        self.client._request(
            "PUT",
            f"/repos/{self.client.username}/{repo_name}/collaborators/{username}",
            json=data
        )
        print(f"✓ 成功添加协作者: {username} (权限: {permission})")
        return {"status": "invited", "username": username, "permission": permission}
    
    def list(self, repo_name: str) -> List[Dict]:
        """列出所有协作者"""
        collaborators = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}/collaborators"
        )
        print(f"\n找到 {len(collaborators)} 个协作者:")
        for collab in collaborators:
            print(f"  - {collab['login']}")
        return collaborators
    
    def remove(self, repo_name: str, username: str) -> bool:
        """移除协作者"""
        self.client._request(
            "DELETE",
            f"/repos/{self.client.username}/{repo_name}/collaborators/{username}"
        )
        print(f"✓ 成功移除协作者: {username}")
        return True
```

### cli/parser.py
```python
"""命令行参数解析器"""
import argparse

def create_parser():
    """创建并配置参数解析器"""
    parser = argparse.ArgumentParser(
        prog="github_manager",
        description="GitHub Manager - 使用 GitHub API 管理仓库",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--token", help="GitHub Personal Access Token")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 仓库管理命令
    _add_repo_commands(subparsers)
    
    # 文件管理命令
    _add_file_commands(subparsers)
    
    # Workflow 命令
    _add_workflow_commands(subparsers)
    
    return parser

def _add_repo_commands(subparsers):
    """添加仓库相关命令"""
    # 创建仓库
    create = subparsers.add_parser("create-repo", help="创建新仓库")
    create.add_argument("name", help="仓库名称")
    create.add_argument("--description", default="", help="仓库描述")
    create.add_argument("--private", action="store_true", help="创建私有仓库")
    create.add_argument("--no-init", action="store_true", help="不自动初始化")
    
    # 列出仓库
    list_repos = subparsers.add_parser("list-repos", help="列出所有仓库")
    list_repos.add_argument("--visibility", choices=["all", "public", "private"],
                           default="all", help="仓库可见性")

def _add_file_commands(subparsers):
    """添加文件相关命令"""
    # 创建文件
    create = subparsers.add_parser("create-file", help="创建文件")
    create.add_argument("repo", help="仓库名称")
    create.add_argument("path", help="文件路径")
    create.add_argument("content", help="文件内容")
    create.add_argument("-m", "--message", required=True, help="提交信息")
    create.add_argument("--branch", default="main", help="分支名称")

def _add_workflow_commands(subparsers):
    """添加 Workflow 相关命令"""
    # 列出 workflows
    list_wf = subparsers.add_parser("list-workflows", help="列出所有 Workflows")
    list_wf.add_argument("repo", help="仓库名称")
    
    # 触发 workflow
    trigger = subparsers.add_parser("trigger-workflow", help="手动触发 Workflow")
    trigger.add_argument("repo", help="仓库名称")
    trigger.add_argument("workflow_id", help="Workflow ID 或文件名")
    trigger.add_argument("--ref", "-b", dest="ref", default="main", help="分支名称")
    trigger.add_argument("--inputs", help="输入参数 (JSON 格式)")
```

## 🚀 使用方式

### 作为包使用
```bash
# 安装为包
pip install -e .

# 使用命令
github-manager create-repo my-project --description "My Project"
github-manager list-repos
github-manager create-file my-repo README.md "# Hello" -m "Initial commit"
```

### 作为模块使用
```bash
python -m github_manager create-repo my-project
```

### 在代码中使用
```python
from github_manager.core.client import GitHubClient
from github_manager.managers.repository import RepositoryManager

# 创建客户端
client = GitHubClient(token="your_token")

# 使用管理器
repo_manager = RepositoryManager(client)
repo_manager.create("new-project", description="My new project")
```

## 🔧 迁移步骤

1. **创建新的目录结构**
   ```bash
   mkdir -p github_manager/{core,managers,cli,utils}
   touch github_manager/{__init__,__main__,config}.py
   touch github_manager/core/{__init__,client,exceptions}.py
   touch github_manager/managers/{__init__,repository,file,workflow}.py
   touch github_manager/cli/{__init__,parser,commands}.py
   ```

2. **复制并重构代码**
   - 将原 `GitHubManager` 类拆分到各个 Manager
   - 提取共同的请求逻辑到 `GitHubClient`
   - 将命令行解析逻辑移到 `cli/parser.py`

3. **更新 setup.py** (可选)
   ```python
   from setuptools import setup, find_packages
   
   setup(
       name="github-manager",
       version="2.0.0",
       packages=find_packages(),
       entry_points={
           'console_scripts': [
               'github-manager=github_manager.__main__:main',
           ],
       },
   )
   ```

4. **测试新结构**
   ```bash
   python -m github_manager list-repos
   ```

## ✨ 关键改进点总结

1. **更小的文件**: 每个文件 < 300 行，易于阅读
2. **清晰的职责**: 每个类只做一件事
3. **统一的接口**: 所有 Manager 都遵循相同的模式
4. **更好的错误处理**: 集中式异常处理
5. **易于测试**: 可以单独测试每个组件
6. **易于扩展**: 添加新功能不影响现有代码
7. **代码复用**: 共享逻辑集中在基类中

这个重构大大提高了代码的可维护性和可扩展性! 🎉