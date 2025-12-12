import argparse

def create_parser():
    """创建并配置参数解析器"""
    parser = argparse.ArgumentParser(
        prog="github_manager",
        description="GitHub Manager - 使用 GitHub API 管理仓库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 仓库管理
  %(prog)s create-repo my-project --description "我的项目" --private
  %(prog)s delete-repo my-project
  %(prog)s fork-repo some-owner some-repo
  %(prog)s list-repos --visibility public
  %(prog)s repo-info my-project
  
  # 文件操作
  %(prog)s create-file my-repo README.md "# Hello World" -m "Initial commit"
  %(prog)s update-file my-repo README.md "# Updated" -m "Update README"
  %(prog)s get-file my-repo README.md --branch main
  
  # 分支管理
  %(prog)s create-branch my-repo feature-branch --from main
  %(prog)s list-branches my-repo
  
  # Issue 和 PR
  %(prog)s create-issue my-repo "Bug报告" --body "发现一个bug"
  %(prog)s create-pr my-repo "新功能" feature-branch main --body "添加新功能"
  
  # 协作者管理
  %(prog)s add-collaborator my-repo username --permission push
  %(prog)s list-collaborators my-repo
  %(prog)s remove-collaborator my-repo username
  
  # 提交历史
  %(prog)s list-commits my-repo --branch main --limit 20
  
  # Workflow 管理
  %(prog)s list-workflows my-repo
  %(prog)s get-workflow my-repo 12345678
  %(prog)s list-runs my-repo --status completed --limit 5
  %(prog)s get-run my-repo 9876543210
  %(prog)s trigger-workflow my-repo ci.yml --ref main
  %(prog)s cancel-run my-repo 9876543210
  %(prog)s rerun my-repo 9876543210 --failed-only
  %(prog)s list-jobs my-repo 9876543210
  %(prog)s get-logs my-repo 9876543210 --output logs.zip
  %(prog)s delete-run my-repo 9876543210
  %(prog)s enable-workflow my-repo ci.yml
  %(prog)s disable-workflow my-repo ci.yml

更多信息请访问: https://docs.github.com/en/rest
        """
    )
    
    parser.add_argument(
        "--token",
        help="GitHub Personal Access Token (或使用环境变量 GITHUB_TOKEN)"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="可用命令",
        metavar="COMMAND"
    )
    
    # 添加各类命令
    _add_repository_commands(subparsers)
    _add_file_commands(subparsers)
    _add_branch_commands(subparsers)
    _add_issue_pr_commands(subparsers)
    _add_collaborator_commands(subparsers)
    _add_commit_commands(subparsers)
    _add_workflow_commands(subparsers)
    
    return parser


def _add_repository_commands(subparsers):
    """添加仓库管理相关命令"""
    
    # 创建仓库
    create_repo = subparsers.add_parser(
        "create-repo",
        help="创建新仓库",
        description="在你的 GitHub 账户下创建一个新仓库"
    )
    create_repo.add_argument("name", help="仓库名称")
    create_repo.add_argument(
        "--description",
        default="",
        help="仓库描述"
    )
    create_repo.add_argument(
        "--private",
        action="store_true",
        help="创建私有仓库（默认为公开）"
    )
    create_repo.add_argument(
        "--no-init",
        action="store_true",
        help="不自动初始化仓库（不创建 README）"
    )
    
    # 删除仓库
    delete_repo = subparsers.add_parser(
        "delete-repo",
        help="删除仓库",
        description="永久删除一个仓库（需要确认）"
    )
    delete_repo.add_argument("name", help="要删除的仓库名称")
    
    # Fork 仓库
    fork_repo = subparsers.add_parser(
        "fork-repo",
        help="Fork 一个仓库",
        description="将其他用户的仓库 Fork 到你的账户"
    )
    fork_repo.add_argument("owner", help="要 Fork 的仓库的拥有者")
    fork_repo.add_argument("repo", help="要 Fork 的仓库名称")
    
    # 列出仓库
    list_repos = subparsers.add_parser(
        "list-repos",
        help="列出所有仓库",
        description="列出你账户下的所有仓库"
    )
    list_repos.add_argument(
        "--visibility",
        choices=["all", "public", "private"],
        default="all",
        help="仓库可见性过滤（默认: all）"
    )
    
    # 仓库信息
    repo_info = subparsers.add_parser(
        "repo-info",
        help="获取仓库详细信息",
        description="显示仓库的详细信息，包括统计数据"
    )
    repo_info.add_argument("repo", help="仓库名称")


def _add_file_commands(subparsers):
    """添加文件操作相关命令"""
    
    # 创建文件
    create_file = subparsers.add_parser(
        "create-file",
        help="创建文件",
        description="在仓库中创建新文件"
    )
    create_file.add_argument("repo", help="仓库名称")
    create_file.add_argument("path", help="文件路径（如: src/main.py）")
    create_file.add_argument("content", help="文件内容")
    create_file.add_argument(
        "-m", "--message",
        required=True,
        help="提交信息"
    )
    create_file.add_argument(
        "--branch",
        default="main",
        help="目标分支（默认: main）"
    )
    
    # 更新文件
    update_file = subparsers.add_parser(
        "update-file",
        help="更新文件",
        description="更新仓库中已存在的文件"
    )
    update_file.add_argument("repo", help="仓库名称")
    update_file.add_argument("path", help="文件路径")
    update_file.add_argument("content", help="新的文件内容")
    update_file.add_argument(
        "-m", "--message",
        required=True,
        help="提交信息"
    )
    update_file.add_argument(
        "--branch",
        default="main",
        help="目标分支（默认: main）"
    )
    
    # 获取文件内容
    get_file = subparsers.add_parser(
        "get-file",
        help="获取文件内容",
        description="读取并显示仓库中文件的内容"
    )
    get_file.add_argument("repo", help="仓库名称")
    get_file.add_argument("path", help="文件路径")
    get_file.add_argument(
        "--branch",
        default="main",
        help="分支名称（默认: main）"
    )


def _add_branch_commands(subparsers):
    """添加分支管理相关命令"""
    
    # 创建分支
    create_branch = subparsers.add_parser(
        "create-branch",
        help="创建分支",
        description="基于现有分支创建新分支"
    )
    create_branch.add_argument("repo", help="仓库名称")
    create_branch.add_argument("branch", help="新分支名称")
    create_branch.add_argument(
        "--from",
        dest="from_branch",
        default="main",
        help="基于哪个分支创建（默认: main）"
    )
    
    # 列出分支
    list_branches = subparsers.add_parser(
        "list-branches",
        help="列出所有分支",
        description="显示仓库的所有分支"
    )
    list_branches.add_argument("repo", help="仓库名称")


def _add_issue_pr_commands(subparsers):
    """添加 Issue 和 Pull Request 相关命令"""
    
    # 创建 Issue
    create_issue = subparsers.add_parser(
        "create-issue",
        help="创建 Issue",
        description="在仓库中创建新的 Issue"
    )
    create_issue.add_argument("repo", help="仓库名称")
    create_issue.add_argument("title", help="Issue 标题")
    create_issue.add_argument(
        "--body",
        default="",
        help="Issue 内容描述"
    )
    create_issue.add_argument(
        "--labels",
        nargs="+",
        help="标签列表（空格分隔）"
    )
    
    # 创建 Pull Request
    create_pr = subparsers.add_parser(
        "create-pr",
        help="创建 Pull Request",
        description="创建一个新的 Pull Request"
    )
    create_pr.add_argument("repo", help="仓库名称")
    create_pr.add_argument("title", help="PR 标题")
    create_pr.add_argument("head", help="源分支（要合并的分支）")
    create_pr.add_argument("base", help="目标分支（合并到的分支）")
    create_pr.add_argument(
        "--body",
        default="",
        help="PR 描述"
    )


def _add_collaborator_commands(subparsers):
    """添加协作者管理相关命令"""
    
    # 添加协作者
    add_collab = subparsers.add_parser(
        "add-collaborator",
        help="添加协作者",
        description="邀请用户成为仓库的协作者"
    )
    add_collab.add_argument("repo", help="仓库名称")
    add_collab.add_argument("username", help="要添加的 GitHub 用户名")
    add_collab.add_argument(
        "--permission",
        choices=["pull", "push", "admin", "maintain", "triage"],
        default="push",
        help="权限级别（默认: push）\n"
             "  pull: 只读访问\n"
             "  push: 读写访问\n"
             "  admin: 管理员权限\n"
             "  maintain: 维护者权限\n"
             "  triage: 分类权限"
    )
    
    # 列出协作者
    list_collab = subparsers.add_parser(
        "list-collaborators",
        help="列出所有协作者",
        description="显示仓库的所有协作者及其权限"
    )
    list_collab.add_argument("repo", help="仓库名称")
    
    # 移除协作者
    remove_collab = subparsers.add_parser(
        "remove-collaborator",
        help="移除协作者",
        description="从仓库中移除协作者"
    )
    remove_collab.add_argument("repo", help="仓库名称")
    remove_collab.add_argument("username", help="要移除的 GitHub 用户名")


def _add_commit_commands(subparsers):
    """添加提交历史相关命令"""
    
    # 列出提交历史
    list_commits = subparsers.add_parser(
        "list-commits",
        help="列出提交历史",
        description="显示仓库的提交历史"
    )
    list_commits.add_argument("repo", help="仓库名称")
    list_commits.add_argument(
        "--branch",
        default="main",
        help="分支名称（默认: main）"
    )
    list_commits.add_argument(
        "--limit",
        type=int,
        default=10,
        help="显示数量（默认: 10）"
    )


def _add_workflow_commands(subparsers):
    """添加 GitHub Actions Workflow 相关命令"""
    
    # 列出 Workflows
    list_workflows = subparsers.add_parser(
        "list-workflows",
        help="列出所有 Workflows",
        description="显示仓库中所有的 GitHub Actions Workflows"
    )
    list_workflows.add_argument("repo", help="仓库名称")
    
    # 获取 Workflow 详情
    get_workflow = subparsers.add_parser(
        "get-workflow",
        help="获取 Workflow 详情",
        description="显示特定 Workflow 的详细信息"
    )
    get_workflow.add_argument("repo", help="仓库名称")
    get_workflow.add_argument(
        "workflow_id",
        help="Workflow ID 或文件名（如: ci.yml）"
    )
    
    # 列出运行记录
    list_runs = subparsers.add_parser(
        "list-runs",
        help="列出 Workflow 运行记录",
        description="显示 Workflow 的运行历史"
    )
    list_runs.add_argument("repo", help="仓库名称")
    list_runs.add_argument(
        "--workflow",
        help="Workflow ID（可选，不指定则列出所有）"
    )
    list_runs.add_argument(
        "--status",
        choices=["queued", "in_progress", "completed"],
        help="过滤运行状态"
    )
    list_runs.add_argument(
        "--branch",
        help="过滤分支"
    )
    list_runs.add_argument(
        "--limit",
        type=int,
        default=10,
        help="返回数量（默认: 10）"
    )
    
    # 获取运行详情
    get_run = subparsers.add_parser(
        "get-run",
        help="获取运行详情",
        description="显示特定 Workflow 运行的详细信息"
    )
    get_run.add_argument("repo", help="仓库名称")
    get_run.add_argument("run_id", type=int, help="运行 ID")
    
    # 触发 Workflow
    trigger_workflow = subparsers.add_parser(
        "trigger-workflow",
        help="手动触发 Workflow",
        description="手动触发一个 Workflow 运行（需要 workflow_dispatch 事件）"
    )
    trigger_workflow.add_argument("repo", help="仓库名称")
    trigger_workflow.add_argument(
        "workflow_id",
        help="Workflow ID 或文件名（如: ci.yml）"
    )
    trigger_workflow.add_argument(
        "--ref", "--branch", "-b",
        dest="ref",
        default="main",
        help="分支或标签名（默认: main）。可使用 --ref, --branch 或 -b"
    )
    trigger_workflow.add_argument(
        "--inputs",
        help='输入参数（JSON 格式），如: \'{"environment":"production"}\''
    )
    
    # 取消运行
    cancel_run = subparsers.add_parser(
        "cancel-run",
        help="取消正在运行的 Workflow",
        description="取消一个正在进行中的 Workflow 运行"
    )
    cancel_run.add_argument("repo", help="仓库名称")
    cancel_run.add_argument("run_id", type=int, help="运行 ID")
    
    # 重新运行
    rerun = subparsers.add_parser(
        "rerun",
        help="重新运行 Workflow",
        description="重新运行一个已完成的 Workflow"
    )
    rerun.add_argument("repo", help="仓库名称")
    rerun.add_argument("run_id", type=int, help="运行 ID")
    rerun.add_argument(
        "--failed-only",
        action="store_true",
        help="只重新运行失败的 jobs"
    )
    
    # 列出 Jobs
    list_jobs = subparsers.add_parser(
        "list-jobs",
        help="列出运行中的所有 Jobs",
        description="显示 Workflow 运行中的所有 Jobs 及其步骤"
    )
    list_jobs.add_argument("repo", help="仓库名称")
    list_jobs.add_argument("run_id", type=int, help="运行 ID")
    
    # 获取日志
    get_logs = subparsers.add_parser(
        "get-logs",
        help="下载运行日志",
        description="下载 Workflow 运行的日志文件（ZIP 格式）"
    )
    get_logs.add_argument("repo", help="仓库名称")
    get_logs.add_argument("run_id", type=int, help="运行 ID")
    get_logs.add_argument(
        "--output", "-o",
        help="输出文件路径（如: logs.zip）"
    )
    
    # 删除运行记录
    delete_run = subparsers.add_parser(
        "delete-run",
        help="删除运行记录",
        description="永久删除一个 Workflow 运行记录"
    )
    delete_run.add_argument("repo", help="仓库名称")
    delete_run.add_argument("run_id", type=int, help="运行 ID")
    
    # 启用 Workflow
    enable_workflow = subparsers.add_parser(
        "enable-workflow",
        help="启用 Workflow",
        description="启用一个被禁用的 Workflow"
    )
    enable_workflow.add_argument("repo", help="仓库名称")
    enable_workflow.add_argument(
        "workflow_id",
        help="Workflow ID 或文件名（如: ci.yml）"
    )
    
    # 禁用 Workflow
    disable_workflow = subparsers.add_parser(
        "disable-workflow",
        help="禁用 Workflow",
        description="禁用一个 Workflow（不会自动触发）"
    )
    disable_workflow.add_argument("repo", help="仓库名称")
    disable_workflow.add_argument(
        "workflow_id",
        help="Workflow ID 或文件名（如: ci.yml）"
    )


if __name__ == "__main__":
    # 用于测试解析器
    parser = create_parser()
    parser.print_help()