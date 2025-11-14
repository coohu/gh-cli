#!/bin/bash
# GitHub Manager 使用示例脚本

echo "================================"
echo "GitHub Manager 使用示例"
echo "================================"
echo ""

# 检查是否设置了 GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  警告: 未设置 GITHUB_TOKEN 环境变量"
    echo ""
    echo "请先设置你的 GitHub Token:"
    echo "  export GITHUB_TOKEN=your_token_here"
    echo ""
    echo "或者使用 --token 参数:"
    echo "  python github_manager.py --token your_token_here [command]"
    echo ""
    echo "获取 Token 的方法:"
    echo "  1. 访问 https://github.com/settings/tokens"
    echo "  2. 点击 'Generate new token (classic)'"
    echo "  3. 选择权限: repo, delete_repo, user"
    echo "  4. 生成并复制 token"
    echo ""
    exit 1
fi

echo "✓ 已检测到 GITHUB_TOKEN"
echo ""

# 示例 1: 列出所有仓库
echo "示例 1: 列出所有仓库"
echo "命令: python github_manager.py list-repos"
echo "----------------------------------------"
# python github_manager.py list-repos
echo ""

# 示例 2: 创建测试仓库
echo "示例 2: 创建测试仓库"
echo "命令: python github_manager.py create-repo test-repo-$(date +%s) --description '测试仓库'"
echo "----------------------------------------"
# REPO_NAME="test-repo-$(date +%s)"
# python github_manager.py create-repo $REPO_NAME --description "测试仓库"
echo ""

# 示例 3: 查看某个仓库的信息
echo "示例 3: 查看仓库信息"
echo "命令: python github_manager.py repo-info your-repo-name"
echo "----------------------------------------"
# python github_manager.py repo-info your-repo-name
echo ""

# 示例 4: 创建文件
echo "示例 4: 在仓库中创建文件"
echo "命令: python github_manager.py create-file your-repo README.md '# Hello' -m 'Initial commit'"
echo "----------------------------------------"
# python github_manager.py create-file your-repo README.md "# Hello World" -m "Initial commit"
echo ""

# 示例 5: 创建分支
echo "示例 5: 创建新分支"
echo "命令: python github_manager.py create-branch your-repo dev"
echo "----------------------------------------"
# python github_manager.py create-branch your-repo dev
echo ""

# 示例 6: 查看提交历史
echo "示例 6: 查看提交历史"
echo "命令: python github_manager.py list-commits your-repo"
echo "----------------------------------------"
# python github_manager.py list-commits your-repo
echo ""

echo "================================"
echo "提示: 取消注释上面的命令来实际执行"
echo "================================"
echo ""
echo "更多命令请查看帮助:"
echo "  python github_manager.py --help"
echo ""
echo "查看特定命令的帮助:"
echo "  python github_manager.py create-repo --help"
echo "  python github_manager.py create-file --help"
echo ""