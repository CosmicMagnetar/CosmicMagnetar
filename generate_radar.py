import os
import requests
import re

# Configuration
USERNAME = "CosmicMagnetar"
TOKEN = os.getenv("METRICS_TOKEN")
headers = {"Authorization": f"token {TOKEN}"}

def fetch_stats():
    try:
        # 1. User basic data
        user_data = requests.get(f"https://api.github.com/users/{USERNAME}", headers=headers).json()
        repos = user_data.get("public_repos", 0)
        followers = user_data.get("followers", 0)

        # 2. PRs & Issues
        prs = requests.get(f"https://api.github.com/search/issues?q=author:{USERNAME}+type:pr", headers=headers).json().get("total_count", 0)
        issues = requests.get(f"https://api.github.com/search/issues?q=author:{USERNAME}+type:issue", headers=headers).json().get("total_count", 0)

        # 3. Stars (Summed from all repos)
        repos_list = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers).json()
        stars = sum(repo['stargazers_count'] for repo in repos_list if isinstance(repo, dict))

        return [repos, issues, prs, stars, followers]
    except Exception as e:
        print(f"Fetch failed: {e}")
        return [0, 0, 0, 0, 0]

stats = fetch_stats()
labels = "['Repos', 'Issues', 'PRs', 'Stars', 'Followers']"

# QuickChart URL with a "Quantum Neon" style
chart_url = (
    f"https://quickchart.io/chart?c={{type:'radar',data:{{labels:{labels},"
    f"datasets:[{{label:'Quantum Stats',data:{stats},fill:true,"
    f"backgroundColor:'rgba(0, 255, 170, 0.15)',borderColor:'rgba(0, 255, 170, 1)',"
    f"pointBackgroundColor:'rgba(0, 255, 170, 1)',borderWidth:2}}]}},"
    f"options:{{scale:{{ticks:{{beginAtZero:true,display:false,maxTicksLimit:4}},"
    f"gridLines:{{color:'rgba(255, 255, 255, 0.1)'}},"
    f"angleLines:{{color:'rgba(255, 255, 255, 0.1)'}},"
    f"pointLabels:{{fontSize:11,fontColor:'#00ffaa',fontStyle:'bold'}}}}}}}}"
)

# README Update Logic
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Specifically targets the gap between your tags
pattern = r".*?"
replacement = f'\n<p align="center">\n  <img src="{chart_url}" width="450" />\n</p>\n'

if re.search(pattern, content, flags=re.DOTALL):
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README updated successfully!")
else:
    print("Error: Could not find the RADAR_CHART tags in your README.md")