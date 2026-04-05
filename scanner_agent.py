import os
import datetime
from github import Github

def run_security_scan():
    # Target repo ka path actions se milta hai
    scan_path = os.getenv('SCAN_PATH', '../target_repo')
    # Bandit scanner chala raha hai
    os.system(f"bandit -r {scan_path} -f txt -o scan_results.txt")
    return "Scan Completed ✅"

def update_readme(scan_status):
    token = os.environ.get("GH_PAT")
    repo_name = os.environ.get("TARGET_REPO")
    
    if not token or not repo_name:
        print("Missing GH_PAT or TARGET_REPO")
        return

    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        readme = repo.get_contents("README.md")
        content = readme.decoded_content.decode('utf-8')
        date_today = datetime.datetime.now().strftime("%d-%B-%Y")
        
        status_msg = f"> 🛡️ **Security Status:** {scan_status} | **Last Audit:** {date_today}"
        
        # README content update logic
        if "🛡️ **Security Status:**" in content:
            lines = content.split('\n')
            new_content = '\n'.join([status_msg if "🛡️ **Security Status:**" in l else l for l in lines])
        else:
            new_content = content + f"\n\n---\n{status_msg}\n"

        repo.update_file(readme.path, f"Security update {date_today}", new_content, readme.sha)
        print(f"Success: Updated {repo_name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    status = run_security_scan()
    update_readme(status)
