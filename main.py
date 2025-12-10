import sys
from .config import Config
from .cli.parser import create_parser
from .cli.commands import CommandHandler


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 获取 Token
    token = args.token or Config.get_token()
    if not token:
        print("错误: 请提供 GitHub Token (使用 --token 参数或设置 GITHUB_TOKEN 环境变量)")
        sys.exit(1)
    
    try:
        handler = CommandHandler(token)
        handler.execute(args)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()