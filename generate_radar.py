import os
import requests
import re

# Configuration
USERNAME = "CosmicMagnetar"
TOKEN = os.getenv("METRICS_TOKEN")
headers = {"Authorization": f"token {TOKEN}"}

def fetch_stats():
    try:
        # 1. Public Repos & Followers
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
        stars = sum(repo['stargazers_count'] for repo in repos_list if isinstance(repo, dict))

        return [repos, issues, prs, stars, followers]
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return [0, 0, 0, 0, 0]

stats = fetch_stats()
labels = "['Repos', 'Issues', 'PRs', 'Stars', 'Followers']"

# QuickChart URL - Optimized for your "System: Online" theme
chart_url = (
    f"https://quickchart.io/chart?c={{type:'radar',data:{{labels:{labels},"
    f"datasets:[{{label:'Quantum Stats',data:{stats},fill:true,"
    f"backgroundColor:'rgba(0, 255, 170, 0.1)',borderColor:'rgba(0, 255, 170, 1)',"
    f"pointBackgroundColor:'rgba(0, 255, 170, 1)'}}]}},"
    f"options:{{scale:{{ticks:{{beginAtZero:true,display:false,maxTicksLimit:3}},"
    f"gridLines:{{color:'rgba(255, 255, 255, 0.1)'}},"
    f"pointLabels:{{fontSize:12,fontColor:'#00ffaa'}}}}}}}}"
)

# READ AND UPDATE README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# This is the critical fix: Search for the tags specifically
# It replaces everything BETWEEN the tags, but keeps the tags themselves
pattern = r".*?"
replacement = f'\n<div align="center"><img src="{chart_url}" width="400" /></div>\n'

if re.search(pattern, content, flags=re.DOTALL):
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README updated successfully!")
else:
    print("Could not find RADAR_CHART tags in README.md")