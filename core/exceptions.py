class GitHubManagerError(Exception):
    """基础异常类"""
    pass


class AuthenticationError(GitHubManagerError):
    """认证失败异常"""
    pass


class ResourceNotFoundError(GitHubManagerError):
    """资源未找到异常"""
    pass


class APIError(GitHubManagerError):
    """API 请求错误"""
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)
