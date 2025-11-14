# GitHub Manager - GitHub API 操作脚本

一个功能完整的 Python 脚本，用于通过 GitHub API 管理仓库，实现项目创建、代码提交、分支管理、Issue/PR 创建等常见任务。

## 功能特性

✨ **仓库管理**
- 创建新仓库（公开/私有）
- 删除仓库
- 列出所有仓库
- 获取仓库详细信息

📝 **文件操作**
- 创建文件并提交
- 更新文件内容
- 获取文件内容
- 支持任意分支操作

🌿 **分支管理**
- 创建新分支
- 列出所有分支
- 基于指定分支创建新分支

🐛 **Issue 和 PR**
- 创建 Issue（支持标签）
- 创建 Pull Request
- 查看提交历史

## 安装依赖

```bash
pip install requests
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

## 配置

### 1. 获取 GitHub Personal Access Token

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token (classic)"
3. 选择以下权限：
   - `repo` - 完整的仓库控制权限
   - `delete_repo` - 删除仓库权限
   - `user` - 读取用户信息
4. 生成并复制 token

### 2. 设置环境变量

**方法一：使用配置文件**

```bash
# 编辑 .env.github 文件
nano .env.github

# 添加你的 token
GITHUB_TOKEN=ghp_your_token_here

# 加载环境变量
source .env.github
```

**方法二：直接导出**

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

**方法三：命令行参数**

```bash
python github_manager.py --token ghp_your_token_here [command]
```

## 使用方法

### 基本语法

```bash
python github_manager.py [--token TOKEN] <command> [arguments]
```

### 命令列表

#### 1. 创建仓库

```bash
# 创建公开仓库
python github_manager.py create-repo my-project --description "我的新项目"

# 创建私有仓库
python github_manager.py create-repo my-private-repo --description "私有项目" --private

# 创建不自动初始化的仓库
python github_manager.py create-repo my-repo --no-init
```

#### 2. 列出仓库

```bash
# 列出所有仓库
python github_manager.py list-repos

# 只列出公开仓库
python github_manager.py list-repos --visibility public

# 只列出私有仓库
python github_manager.py list-repos --visibility private
```

#### 3. 删除仓库

```bash
python github_manager.py delete-repo my-project
# 会提示确认：确定要删除仓库 'my-project' 吗? (yes/no):
```

#### 4. 创建文件

```bash
# 在 main 分支创建文件
python github_manager.py create-file my-project README.md "# Hello World" -m "Initial commit"

# 在指定分支创建文件
python github_manager.py create-file my-project src/main.py "print('Hello')" -m "Add main.py" --branch dev

# 创建多行内容文件
python github_manager.py create-file my-project config.json '{
  "name": "my-app",
  "version": "1.0.0"
}' -m "Add config"
```

#### 5. 更新文件

```bash
# 更新文件内容
python github_manager.py update-file my-project README.md "# Updated Content" -m "Update README"

# 在指定分支更新
python github_manager.py update-file my-project src/main.py "print('Updated')" -m "Update main" --branch dev
```

#### 6. 获取文件内容

```bash
# 获取 main 分支的文件
python github_manager.py get-file my-project README.md

# 获取指定分支的文件
python github_manager.py get-file my-project src/main.py --branch dev
```

#### 7. 创建分支

```bash
# 从 main 分支创建新分支
python github_manager.py create-branch my-project feature-login

# 从指定分支创建新分支
python github_manager.py create-branch my-project hotfix --from dev
```

#### 8. 列出分支

```bash
python github_manager.py list-branches my-project
```

#### 9. 创建 Issue

```bash
# 创建简单 Issue
python github_manager.py create-issue my-project "Bug: 登录失败"

# 创建带内容的 Issue
python github_manager.py create-issue my-project "Feature Request" --body "希望添加暗黑模式"

# 创建带标签的 Issue
python github_manager.py create-issue my-project "Bug Report" --body "发现一个bug" --labels bug urgent
```

#### 10. 创建 Pull Request

```bash
# 创建 PR（从 feature 分支合并到 main）
python github_manager.py create-pr my-project "添加登录功能" feature-login main

# 创建带描述的 PR
python github_manager.py create-pr my-project "修复bug" hotfix main --body "修复了登录失败的问题"
```

#### 11. 查看提交历史

```bash
# 查看 main 分支最近 10 次提交
python github_manager.py list-commits my-project

# 查看指定分支的提交
python github_manager.py list-commits my-project --branch dev

# 查看更多提交
python github_manager.py list-commits my-project --limit 20
```

#### 12. 查看仓库信息

```bash
python github_manager.py repo-info my-project
```

## 完整工作流示例

### 示例 1：创建新项目并添加代码

```bash
# 1. 创建仓库
python github_manager.py create-repo my-awesome-app --description "一个很棒的应用"

# 2. 创建 README
python github_manager.py create-file my-awesome-app README.md "# My Awesome App

这是一个很棒的应用！

## 安装

\`\`\`bash
pip install -r requirements.txt
\`\`\`
" -m "Add README"

# 3. 创建主程序文件
python github_manager.py create-file my-awesome-app main.py "#!/usr/bin/env python3

def main():
    print('Hello, World!')

if __name__ == '__main__':
    main()
" -m "Add main.py"

# 4. 创建配置文件
python github_manager.py create-file my-awesome-app config.json '{
  "app_name": "my-awesome-app",
  "version": "1.0.0"
}' -m "Add config"

# 5. 查看提交历史
python github_manager.py list-commits my-awesome-app
```

### 示例 2：功能分支开发流程

```bash
# 1. 创建功能分支
python github_manager.py create-branch my-project feature-auth

# 2. 在功能分支添加代码
python github_manager.py create-file my-project auth.py "def login(username, password):
    # 登录逻辑
    pass
" -m "Add authentication module" --branch feature-auth

# 3. 更新文档
python github_manager.py update-file my-project README.md "# My Project

## 新功能
- 添加了用户认证功能
" -m "Update README with auth info" --branch feature-auth

# 4. 创建 Pull Request
python github_manager.py create-pr my-project "添加用户认证功能" feature-auth main --body "实现了基本的用户登录和注册功能"

# 5. 创建相关 Issue
python github_manager.py create-issue my-project "测试认证功能" --body "需要对新的认证功能进行全面测试" --labels testing
```

### 示例 3：批量操作脚本

创建一个 bash 脚本来自动化多个操作：

```bash
#!/bin/bash
# setup_project.sh

REPO_NAME="my-new-project"
DESCRIPTION="自动创建的项目"

# 创建仓库
python github_manager.py create-repo $REPO_NAME --description "$DESCRIPTION"

# 创建项目结构
python github_manager.py create-file $REPO_NAME .gitignore "*.pyc
__pycache__/
.env
" -m "Add .gitignore"

python github_manager.py create-file $REPO_NAME requirements.txt "requests>=2.28.0
" -m "Add requirements.txt"

python github_manager.py create-file $REPO_NAME src/main.py "# Main application
" -m "Add main.py"

# 创建开发分支
python github_manager.py create-branch $REPO_NAME develop

echo "项目 $REPO_NAME 创建完成！"
```

## 作为 Python 模块使用

你也可以在自己的 Python 代码中导入使用：

```python
from github_manager import GitHubManager

# 初始化
gh = GitHubManager(token="your_github_token")

# 创建仓库
repo = gh.create_repository("test-repo", description="测试仓库", private=True)

# 创建文件
gh.create_file("test-repo", "hello.txt", "Hello, GitHub!", "Initial commit")

# 创建分支
gh.create_branch("test-repo", "dev")

# 在新分支创建文件
gh.create_file("test-repo", "feature.py", "# New feature", "Add feature", branch="dev")

# 创建 PR
gh.create_pull_request("test-repo", "Merge dev to main", "dev", "main")

# 列出所有仓库
repos = gh.list_repositories()

# 获取仓库信息
info = gh.get_repository_info("test-repo")
```

## 错误处理

脚本包含完善的错误处理机制：

- **认证失败**：检查 token 是否正确
- **仓库不存在**：确认仓库名称拼写正确
- **权限不足**：确保 token 有足够的权限
- **文件已存在**：使用 `update-file` 而不是 `create-file`
- **分支不存在**：先创建分支或检查分支名称

## 注意事项

⚠️ **安全提示**
- 不要将 token 提交到版本控制系统
- 定期更换 token
- 使用最小权限原则
- 删除操作需要确认

📌 **最佳实践**
- 使用有意义的提交信息
- 在删除仓库前做好备份
- 测试操作先在测试仓库进行
- 使用分支进行功能开发

## 常见问题

**Q: 如何获取 GitHub Token？**
A: 访问 GitHub Settings → Developer settings → Personal access tokens → Generate new token

**Q: Token 需要哪些权限？**
A: 至少需要 `repo` 权限，删除仓库需要 `delete_repo` 权限

**Q: 可以操作组织的仓库吗？**
A: 可以，但需要相应的组织权限，并在命令中使用完整的仓库路径

**Q: 如何批量操作多个仓库？**
A: 可以编写 bash 脚本或 Python 脚本循环调用

**Q: 支持 GitHub Enterprise 吗？**
A: 需要修改 `base_url` 为你的 GitHub Enterprise 地址

## 技术细节

- **API 版本**：GitHub REST API v3
- **认证方式**：Personal Access Token
- **编码方式**：文件内容使用 Base64 编码
- **默认分支**：main（可配置）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 作者

Created with ❤️ by Cline

---

**快速开始**

```bash
# 1. 安装依赖
pip install requests

# 2. 设置 token
export GITHUB_TOKEN=your_token_here

# 3. 创建第一个仓库
python github_manager.py create-repo hello-world --description "My first repo"

# 4. 添加文件
python github_manager.py create-file hello-world README.md "# Hello World" -m "Initial commit"

# 5. 查看结果
python github_manager.py repo-info hello-world
```

开始使用 GitHub Manager 来自动化你的 GitHub 工作流吧！🚀