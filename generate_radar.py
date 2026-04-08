import os
import requests

# Configuration
USERNAME = "CosmicMagnetar"
TOKEN = os.getenv("METRICS_TOKEN")
headers = {"Authorization": f"token {TOKEN}"}

def fetch_stats():
    # 1. Public Repos
    user_url = f"https://api.github.com/users/{USERNAME}"
    user_data = requests.get(user_url, headers=headers).json()
    repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)

    # 2. PRs & Issues (Search API)
    pr_url = f"https://api.github.com/search/issues?q=author:{USERNAME}+type:pr"
    issue_url = f"https://api.github.com/search/issues?q=author:{USERNAME}+type:issue"
    
    prs = requests.get(pr_url, headers=headers).json().get("total_count", 0)
    issues = requests.get(issue_url, headers=headers).json().get("total_count", 0)

    # 3. Stars (Sum of all stars on your repos)
    star_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos_list = requests.get(star_url, headers=headers).json()
    stars = sum(repo['stargazers_count'] for repo in repos_list)

    return [repos, issues, prs, stars, followers]

stats = fetch_stats()
labels = "['Repositories', 'Issues', 'PRs', 'Stars', 'Followers']"

# QuickChart URL with a "Quantum/Neon" Theme
chart_url = (
    f"https://quickchart.io/chart?c={{type:'radar',data:{{labels:{labels},"
    f"datasets:[{{label:'Player Stats',data:{stats},fill:true,"
    f"backgroundColor:'rgba(0, 210, 255, 0.2)',borderColor:'rgba(0, 210, 255, 1)',"
    f"pointBackgroundColor:'rgba(255, 0, 255, 1)'}}]}},"
    f"options:{{scale:{{ticks:{{beginAtZero:true,display:false}},"
    f"pointLabels:{{fontSize:14,fontColor:'#888'}}}}}}}}"
)

# Read README, replace placeholder, and write back
with open("README.md", "r") as f:
    content = f.read()

import re
replacement = f'\n<img src="{chart_url}" width="500" />\n'
new_content = re.sub(r".*?", replacement, content, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(new_content)