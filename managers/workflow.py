from typing import Dict, List, Optional
from core.client import GitHubClient

class WorkflowManager:
    def __init__(self, client: GitHubClient):
        self.client = client
    
    def list_workflows(self, repo_name: str) -> List[Dict]:
        """列出仓库的所有 workflows"""
        data = self.client._request(
            "GET",
            f"/repos/{self.client.username}/{repo_name}/actions/workflows"
        )
        workflows = data.get("workflows", [])
        
        print(f"\n找到 {len(workflows)} 个 Workflow:")
        for wf in workflows:
            state_icon = "✓" if wf["state"] == "active" else "○"
            print(f"  {state_icon} [{wf['id']}] {wf['name']}")
            print(f"      路径: {wf['path']}")
            print(f"      状态: {wf['state']}")
        return workflows
    
    def list_runs(self, repo_name: str, workflow_id: Optional[str] = None,
                  status: Optional[str] = None, branch: Optional[str] = None,
                  limit: int = 10) -> List[Dict]:
        """列出 workflow 运行记录"""
        params = {"per_page": limit}
        if status:
            params["status"] = status
        if branch:
            params["branch"] = branch
        
        if workflow_id:
            endpoint = f"/repos/{self.client.username}/{repo_name}/actions/workflows/{workflow_id}/runs"
        else:
            endpoint = f"/repos/{self.client.username}/{repo_name}/actions/runs"
        
        data = self.client._request("GET", endpoint, params=params)
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
        return runs
    
    def trigger(self, repo_name: str, workflow_id: str,
                ref: str = "main", inputs: Optional[Dict] = None) -> bool:
        """手动触发 workflow 运行"""
        data = {"ref": ref}
        if inputs:
            data["inputs"] = inputs
        
        self.client._request(
            "POST",
            f"/repos/{self.client.username}/{repo_name}/actions/workflows/{workflow_id}/dispatches",
            json=data
        )
        print(f"✓ Workflow 触发成功")
        print(f"  Workflow: {workflow_id}")
        print(f"  分支: {ref}")
        return True
    
    def cancel_run(self, repo_name: str, run_id: int) -> bool:
        """取消正在运行的 workflow"""
        self.client._request(
            "POST",
            f"/repos/{self.client.username}/{repo_name}/actions/runs/{run_id}/cancel"
        )
        print(f"✓ 已请求取消运行: {run_id}")
        return True
