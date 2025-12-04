# GitHub 协作者管理功能

本文档介绍如何使用 `manager.py` 脚本管理 GitHub 仓库的协作者。

## 功能概述

该脚本提供了三个主要的协作者管理功能：

1. **添加协作者** - 向仓库添加新的协作者并设置权限
2. **列出协作者** - 查看仓库的所有协作者及其权限
3. **移除协作者** - 从仓库中移除协作者

## 前置要求

1. **GitHub Personal Access Token**
   - 需要具有 `repo` 权限的 GitHub Token
   - 可以在 GitHub Settings > Developer settings > Personal access tokens 中创建
   - 确保 Token 具有管理仓库协作者的权限

2. **Python 环境**
   - Python 3.6+
   - 安装依赖：`pip install -r requirements.txt`

3. **环境变量设置**
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```
   或者在命令行中使用 `--token` 参数

## 使用方法

### 1. 添加协作者

向指定仓库添加协作者，并设置相应的权限级别。

**基本语法：**
```bash
python manager.py add-collaborator <仓库名称> <GitHub用户名> [--permission <权限级别>]
```

**权限级别选项：**
- `pull` - 只读权限（可以拉取代码）
- `push` - 读写权限（可以推送代码）**[默认]**
- `admin` - 管理员权限（完全控制）
- `maintain` - 维护者权限（管理仓库但不能访问敏感操作）
- `triage` - 分类权限（管理 issues 和 pull requests）

**示例：**

```bash
# 添加协作者，使用默认的 push 权限
python manager.py add-collaborator my-project john-doe

# 添加协作者，指定为只读权限
python manager.py add-collaborator my-project jane-smith --permission pull

# 添加协作者，指定为管理员权限
python manager.py add-collaborator my-project admin-user --permission admin

# 使用 Token 参数
python manager.py add-collaborator my-project developer --token ghp_xxxxxxxxxxxx --permission push
```

**输出示例：**
```
已认证用户: your-username

✓ 成功添加协作者: john-doe (权限: push)
  用户将收到邀请邮件，需要接受邀请后才能访问仓库
```

**注意事项：**
- 被添加的用户会收到一封邀请邮件
- 用户需要接受邀请后才能访问仓库
- 如果用户已经是协作者，此命令会更新其权限级别

### 2. 列出协作者

查看仓库的所有协作者及其权限信息。

**基本语法：**
```bash
python manager.py list-collaborators <仓库名称>
```

**示例：**

```bash
# 列出指定仓库的所有协作者
python manager.py list-collaborators my-project

# 使用 Token 参数
python manager.py list-collaborators my-project --token ghp_xxxxxxxxxxxx
```

**输出示例：**
```
已认证用户: your-username

找到 3 个协作者:
  - your-username (权限: {'admin': True, 'maintain': True, 'push': True, 'triage': True, 'pull': True})
  - john-doe (权限: {'admin': False, 'maintain': False, 'push': True, 'triage': True, 'pull': True})
  - jane-smith (权限: {'admin': False, 'maintain': False, 'push': False, 'triage': False, 'pull': True})
```

### 3. 移除协作者

从仓库中移除指定的协作者。

**基本语法：**
```bash
python manager.py remove-collaborator <仓库名称> <GitHub用户名>
```

**示例：**

```bash
# 移除协作者
python manager.py remove-collaborator my-project john-doe

# 使用 Token 参数
python manager.py remove-collaborator my-project jane-smith --token ghp_xxxxxxxxxxxx
```

**输出示例：**
```
已认证用户: your-username

✓ 成功移除协作者: john-doe
```

**注意事项：**
- 移除操作是立即生效的
- 被移除的用户将立即失去对仓库的访问权限
- 仓库所有者无法被移除

## 完整工作流程示例

以下是一个完整的协作者管理工作流程：

```bash
# 1. 查看当前协作者
python manager.py list-collaborators my-project

# 2. 添加新的开发者（读写权限）
python manager.py add-collaborator my-project developer1 --permission push

# 3. 添加代码审查者（只读权限）
python manager.py add-collaborator my-project reviewer1 --permission pull

# 4. 添加项目管理员
python manager.py add-collaborator my-project admin1 --permission admin

# 5. 再次查看协作者列表，确认添加成功
python manager.py list-collaborators my-project

# 6. 如果需要，更新某个协作者的权限（重新添加即可）
python manager.py add-collaborator my-project developer1 --permission admin

# 7. 移除不再需要的协作者
python manager.py remove-collaborator my-project reviewer1

# 8. 最终确认协作者列表
python manager.py list-collaborators my-project
```

## 错误处理

### 常见错误及解决方案

1. **认证失败**
   ```
   错误: 认证失败: {'message': 'Bad credentials'}
   ```
   - 检查 GitHub Token 是否正确
   - 确认 Token 是否过期
   - 验证 Token 是否具有必要的权限

2. **仓库不存在**
   ```
   错误: 添加协作者失败: {'message': 'Not Found'}
   ```
   - 确认仓库名称拼写正确
   - 确认您对该仓库有管理权限
   - 确认仓库属于当前认证用户

3. **用户不存在**
   ```
   错误: 添加协作者失败: {'message': 'Not Found'}
   ```
   - 确认 GitHub 用户名拼写正确
   - 确认该用户的 GitHub 账号存在

4. **权限不足**
   ```
   错误: 添加协作者失败: {'message': 'Must have admin rights to Repository'}
   ```
   - 只有仓库所有者或管理员才能添加/移除协作者
   - 确认您的 Token 具有足够的权限

## API 限制

- GitHub API 有速率限制（通常为每小时 5000 次请求）
- 对于认证请求，限制更高
- 如果遇到速率限制，请等待一段时间后重试

## 安全建议

1. **保护您的 Token**
   - 不要在代码中硬编码 Token
   - 使用环境变量存储 Token
   - 定期轮换 Token
   - 为 Token 设置最小必要权限

2. **权限管理最佳实践**
   - 遵循最小权限原则
   - 定期审查协作者列表
   - 及时移除不再需要访问的用户
   - 为不同角色设置适当的权限级别

3. **审计日志**
   - GitHub 会记录所有协作者的添加和移除操作
   - 可以在仓库的 Settings > Manage access 中查看历史记录

## 相关资源

- [GitHub API 文档 - Collaborators](https://docs.github.com/en/rest/collaborators)
- [GitHub 权限级别说明](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories/repository-permission-levels-for-an-organization)
- [创建 Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## 技术支持

如果遇到问题，请：
1. 检查本文档的错误处理部分
2. 查看 GitHub API 文档
3. 确认您的 Token 权限设置
4. 查看脚本的详细错误信息

## 更新日志

- **2025-12-04**: 添加协作者管理功能
  - 新增 `add_collaborator` 方法
  - 新增 `list_collaborators` 方法
  - 新增 `remove_collaborator` 方法
  - 添加命令行接口支持
