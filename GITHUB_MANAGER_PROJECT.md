# GitHub Manager 项目说明

## 项目概述

这是一个功能完整的 Python 脚本，用于通过 GitHub REST API 操作 GitHub 仓库。它提供了命令行接口和 Python 模块两种使用方式，可以自动化完成项目创建、代码提交、分支管理等常见 GitHub 操作任务。

## 项目文件

```
/home/coohu/
├── github_manager.py          # 主脚本文件（核心功能）
├── requirements.txt           # Python 依赖包列表
├── .env.github               # 环境变量配置示例
├── README_github_manager.md  # 详细使用文档
└── github_example.sh         # 使用示例脚本
```

## 核心功能

### 1. 仓库管理
- ✅ 创建新仓库（支持公开/私有）
- ✅ 删除仓库（带确认机制）
- ✅ 列出所有仓库（支持按可见性筛选）
- ✅ 获取仓库详细信息

### 2. 文件操作
- ✅ 创建文件并提交到仓库
- ✅ 更新现有文件内容
- ✅ 获取文件内容
- ✅ 支持在任意分支操作

### 3. 分支管理
- ✅ 创建新分支
- ✅ 列出所有分支
- ✅ 基于指定分支创建新分支

### 4. 协作功能
- ✅ 创建 Issue（支持标签）
- ✅ 创建 Pull Request
- ✅ 查看提交历史

## 技术特点

### 架构设计
- **面向对象设计**：使用 `GitHubManager` 类封装所有 API 操作
- **命令行接口**：使用 `argparse` 提供友好的 CLI 体验
- **模块化**：可作为 Python 模块导入使用

### API 集成
- **GitHub REST API v3**：使用官方 REST API
- **认证方式**：Personal Access Token
- **内容编码**：Base64 编码处理文件内容
- **错误处理**：完善的异常处理和错误提示

### 安全性
- **Token 保护**：支持环境变量和命令行参数
- **删除确认**：危险操作需要用户确认
- **权限控制**：明确说明所需的 API 权限

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Token

```bash
# 方法 1: 使用环境变量
export GITHUB_TOKEN=your_github_token_here

# 方法 2: 使用配置文件
cp .env.github .env.github.local
# 编辑 .env.github.local 添加你的 token
source .env.github.local
```

### 3. 测试脚本

```bash
# 查看帮助
python github_manager.py --help

# 列出所有仓库
python github_manager.py list-repos

# 创建测试仓库
python github_manager.py create-repo test-repo --description "测试仓库"
```

## 使用示例

### 命令行方式

```bash
# 创建仓库
python github_manager.py create-repo my-project --description "我的项目" --private

# 创建文件
python github_manager.py create-file my-project README.md "# Hello World" -m "Initial commit"

# 创建分支
python github_manager.py create-branch my-project dev

# 创建 PR
python github_manager.py create-pr my-project "新功能" dev main --body "添加新功能"
```

### Python 模块方式

```python
from github_manager import GitHubManager

# 初始化
gh = GitHubManager(token="your_token")

# 创建仓库
repo = gh.create_repository("test-repo", description="测试", private=True)

# 创建文件
gh.create_file("test-repo", "hello.py", "print('Hello')", "Add hello.py")

# 创建分支
gh.create_branch("test-repo", "dev")
```

## 支持的命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `create-repo` | 创建仓库 | `create-repo my-repo --private` |
| `delete-repo` | 删除仓库 | `delete-repo my-repo` |
| `list-repos` | 列出仓库 | `list-repos --visibility public` |
| `create-file` | 创建文件 | `create-file repo path content -m "msg"` |
| `update-file` | 更新文件 | `update-file repo path content -m "msg"` |
| `get-file` | 获取文件 | `get-file repo path` |
| `create-branch` | 创建分支 | `create-branch repo branch-name` |
| `list-branches` | 列出分支 | `list-branches repo` |
| `create-issue` | 创建Issue | `create-issue repo "title" --body "desc"` |
| `create-pr` | 创建PR | `create-pr repo "title" head base` |
| `list-commits` | 提交历史 | `list-commits repo --limit 10` |
| `repo-info` | 仓库信息 | `repo-info repo` |

## 实际应用场景

### 场景 1: 自动化项目初始化
```bash
# 创建仓库并初始化项目结构
python github_manager.py create-repo new-project
python github_manager.py create-file new-project .gitignore "*.pyc\n__pycache__/" -m "Add gitignore"
python github_manager.py create-file new-project README.md "# New Project" -m "Add README"
python github_manager.py create-branch new-project develop
```

### 场景 2: 批量仓库管理
```bash
# 列出所有私有仓库
python github_manager.py list-repos --visibility private

# 批量更新 README
for repo in repo1 repo2 repo3; do
    python github_manager.py update-file $repo README.md "Updated content" -m "Update README"
done
```

### 场景 3: CI/CD 集成
```bash
# 在 CI 流程中自动创建 release 分支
python github_manager.py create-branch my-app release-v1.0 --from main
python github_manager.py create-pr my-app "Release v1.0" release-v1.0 main
```

## 注意事项

### 安全建议
- ⚠️ 不要将 token 提交到版本控制系统
- ⚠️ 定期更换 Personal Access Token
- ⚠️ 使用最小权限原则（只授予必要的权限）
- ⚠️ 删除操作不可恢复，请谨慎使用

### 最佳实践
- ✅ 使用有意义的提交信息
- ✅ 在生产环境操作前先在测试仓库验证
- ✅ 使用分支进行功能开发
- ✅ 定期备份重要仓库

## 扩展功能建议

如果需要扩展功能，可以考虑添加：

1. **Release 管理**：创建和管理 GitHub Releases
2. **Webhook 配置**：自动配置仓库 webhooks
3. **团队管理**：添加/删除协作者
4. **标签管理**：创建和管理 Git tags
5. **Actions 管理**：触发 GitHub Actions 工作流
6. **统计分析**：获取仓库统计数据
7. **批量操作**：支持配置文件批量执行操作
8. **交互模式**：提供交互式命令行界面

## 故障排查

### 常见问题

**Q: 认证失败**
```
错误: 认证失败: {'message': 'Bad credentials'}
解决: 检查 GITHUB_TOKEN 是否正确设置
```

**Q: 权限不足**
```
错误: 创建仓库失败: {'message': 'Not Found'}
解决: 确保 token 有 'repo' 权限
```

**Q: 文件已存在**
```
错误: 创建文件失败: {'message': 'Invalid request'}
解决: 使用 update-file 命令而不是 create-file
```

**Q: 分支不存在**
```
错误: 获取源分支失败
解决: 检查分支名称是否正确，或先创建该分支
```

## 性能考虑

- API 速率限制：认证用户每小时 5000 次请求
- 文件大小限制：单个文件最大 100MB
- 批量操作：建议添加延迟避免触发速率限制
- 大文件处理：考虑使用 Git LFS

## 开发信息

- **开发语言**：Python 3.6+
- **依赖库**：requests
- **API 版本**：GitHub REST API v3
- **许可证**：MIT License

## 相关资源

- [GitHub REST API 文档](https://docs.github.com/en/rest)
- [Personal Access Token 创建指南](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub API 速率限制](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)

## 更新日志

### v1.0.0 (2025-11-11)
- ✅ 初始版本发布
- ✅ 实现基本的仓库管理功能
- ✅ 实现文件操作功能
- ✅ 实现分支管理功能
- ✅ 实现 Issue 和 PR 创建功能
- ✅ 提供完整的命令行接口
- ✅ 支持作为 Python 模块使用

---

**开始使用 GitHub Manager，让 GitHub 操作自动化！** 🚀