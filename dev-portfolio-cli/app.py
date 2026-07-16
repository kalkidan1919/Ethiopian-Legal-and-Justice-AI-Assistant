import os
import json
import urllib.request
import sys

class DeveloperPortfolio:
    
    def __init__(self, json_file_path="profile.json"):
        self.json_file_path = json_file_path
        self.profile_data = {}
        self.github_api_data = {}

    # Method 1: Load and parse local JSON profile
    def load_local_profile(self):
        try:
            with open(self.json_file_path, 'r') as file:
                self.profile_data = json.load(file)
                print("[SUCCESS] Local profile file loaded successfully!")
        except FileNotFoundError:
            print(f"[ERROR] Could not find file: '{self.json_file_path}'")
            sys.exit(1)
        except json.JSONDecodeError:
            print("[ERROR] FAILED TO PARSE JSON. Check your syntax/commas.")
            sys.exit(1)

    # Method 2: Fetch dynamic GitHub repository stats
    def fetch_github_data(self):
        username = self.profile_data.get("github_username")
        repo = self.profile_data.get("github_repo")
        
        if not username or not repo or repo == "YOUR_ACTUAL_REPOSITORY_NAME_HERE":
            print("[GITHUB INFO] No repository configured in profile.json. Skipping GitHub fetch.")
            return

        # Auto-clean in case a full URL path was accidentally provided
        if "/" in repo:
            repo = repo.rstrip("/").split("/")[-1]

        api_url = f"https://api.github.com/repos/{username}/{repo}"
        request_headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            request_headers['Authorization'] = f'token {github_token}'
            print("[INFO] Authenticating with GITHUB_TOKEN...")
        
        request = urllib.request.Request(api_url, headers=request_headers)

        try:
            print(f"[INFO] Connecting to GitHub API for '{username}/{repo}'...")
            # Using a 4-second timeout limit so the script never hangs up
            with urllib.request.urlopen(request, timeout=4.0) as response:
                self.github_api_data = json.loads(response.read().decode())
                print("[SUCCESS] Live GitHub API data fetched successfully!")
        except Exception as e:
            print(f"[GITHUB API WARNING] Could not retrieve live repo stats ({type(e).__name__}).")

    # Method 3: Render CLI portfolio view
    def display_portfolio_cli(self):
        print("\n" + "="*60)
        user_name = self.profile_data.get("name", "Unknown Developer")
        print(f"DEVELOPER PORTFOLIO FOR: {user_name.upper()}")
        print("="*60)
        
        print(f"📍 Current Role:  {self.profile_data.get('role', 'N/A')}")
        print(f"🏫 University:    {self.profile_data.get('university', 'N/A')}")
        print(f"📝 Description:   {self.profile_data.get('bio', 'N/A')}")
        
        user_skills = self.profile_data.get("skills", [])
        print(f"🛠️  Technical Skills: {', '.join(user_skills)}")
        print("-" * 60)
        
        # GitHub Display block
        if self.github_api_data and "message" not in self.github_api_data:
            print("💻 LIVE PROJECT STATS (GITHUB):")
            print(f"📦 Repository:       {self.github_api_data.get('name', 'N/A')}")
            print(f"⭐ Stars:            {self.github_api_data.get('stargazers_count', 0)}")
            print(f"🍴 Forks:            {self.github_api_data.get('forks_count', 0)}")
            print(f"⚡ Primary Language: {self.github_api_data.get('language', 'N/A')}")
        else:
            print("⚠️  Live GitHub stats are currently unavailable.")
            
        print("=" * 60 + "\n")

    def run(self):
        self.load_local_profile()
        self.fetch_github_data()
        self.display_portfolio_cli()

if __name__ == "__main__":
    portfolio_app = DeveloperPortfolio(json_file_path="profile.json")
    portfolio_app.run()