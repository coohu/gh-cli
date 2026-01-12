from core.client import GitHubClient
from managers.repository import RepositoryManager
from managers.file import FileManager
from managers.workflow import WorkflowManager

class CommandHandler:
    def __init__(self, token: str):
        self.client = GitHubClient(token)
        self.repo_manager = RepositoryManager(self.client)
        self.file_manager = FileManager(self.client)
        self.workflow_manager = WorkflowManager(self.client)
        
        print(f"已认证用户: {self.client.username}\n")
    
    def execute(self, args):
        """执行命令"""
        command = args.command.replace('-', '_')
        handler = getattr(self, f"handle_{command}", None)
        
        if handler:
            handler(args)
        else:
            print(f"未知命令: {args.command}")
    
    def handle_create_repo(self, args):
        """处理创建仓库命令"""
        self.repo_manager.create(
            args.name,
            args.description,
            args.private,
            not args.no_init
        )

    def handle_fork_repo(self, args):
        self.repo_manager.fork(
            args.owner,
            args.repo_name
        )
    
    def handle_list_repos(self, args):
        """处理列出仓库命令"""
        self.repo_manager.list(args.visibility)
    
    def handle_create_file(self, args):
        """处理创建文件命令"""
        self.file_manager.create(
            args.repo,
            args.path,
            args.content,
            args.message,
            args.branch
        )
    
    def handle_list_workflows(self, args):
        """处理列出 workflows 命令"""
        self.workflow_manager.list_workflows(args.repo)
    
    def handle_trigger_workflow(self, args):
        """处理触发 workflow 命令"""
        import json
        inputs = None
        if args.inputs:
            inputs = json.loads(args.inputs)
        self.workflow_manager.trigger(
            args.repo,
            args.workflow_id,
            args.ref,
            inputs
        )
