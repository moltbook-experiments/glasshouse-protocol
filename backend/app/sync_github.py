import os
import requests
import base64
import json
import time

# Vercel constraints
GITHUB_API = "https://api.github.com"

class GitHubSyncer:
    def __init__(self, owner, repo, token, branch="main"):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.branch = branch
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        self.last_sync_path = "/tmp/last_sync_timestamp" if os.environ.get("VERCEL") else "last_sync_timestamp"
        self.sync_interval = 600  # 10 minutes

    def _should_sync(self):
        try:
            if not os.path.exists(self.last_sync_path):
                return True
            with open(self.last_sync_path, 'r') as f:
                last_ts = float(f.read().strip())
            return (time.time() - last_ts) > self.sync_interval
        except:
            return True

    def _update_timestamp(self):
        try:
            with open(self.last_sync_path, 'w') as f:
                f.write(str(time.time()))
        except:
            pass

    def sync_file(self, local_path, repo_path):
        """Push a single file to GitHub"""
        if not self._should_sync():
            return False

        if not os.path.exists(local_path):
            return False

        try:
            with open(local_path, 'r') as f:
                content = f.read()
            
            # Encode content
            b64_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

            # Get SHA of existing file (if any)
            url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/contents/{repo_path}"
            resp = requests.get(url, headers=self.headers)
            sha = None
            if resp.status_code == 200:
                sha = resp.json().get('sha')

            # Create/Update file
            data = {
                "message": f"Sync from Glasshouse Protocol [Automated]",
                "content": b64_content,
                "branch": self.branch
            }
            if sha:
                data["sha"] = sha

            put_resp = requests.put(url, headers=self.headers, json=data)
            if put_resp.status_code in [200, 201]:
                self._update_timestamp()
                return True
            else:
                print(f"Failed to sync {repo_path}: {put_resp.text}")
                return False

        except Exception as e:
            print(f"Sync error: {e}")
            return False

# Convenience function used by hooks
def trigger_sync(file_map):
    """
    file_map: dict of {local_path: repo_path}
    """
    token = os.environ.get("GITHUB_TOKEN")
    repo_slug = os.environ.get("GITHUB_REPOSITORY") # "owner/repo"

    if not token or not repo_slug:
        return # Cannot sync without config

    owner, repo_name = repo_slug.split('/')
    
    syncer = GitHubSyncer(owner, repo_name, token)
    
    for local, remote in file_map.items():
        syncer.sync_file(local, remote)

