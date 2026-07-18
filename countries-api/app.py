import json
import urllib.request
import urllib.parse
import urllib.error

class APIError(Exception):
    """Custom exception raised for failed external REST API calls."""
    pass

class ProfileError(Exception):
    """Custom exception raised for local configuration file problems."""
    pass


class DeveloperPortfolio:
    """An encapsulated application to manage profile displays and external REST APIs."""
    
    def __init__(self, config_path: str = "profile.json"):
        self.config_path = config_path
        self.profile_data = {}
        self.live_country_data = {}

    def load_profile(self) -> None:
        """Reads and parses the profile.json configuration safely."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                self.profile_data = json.load(file)
        except FileNotFoundError:
            raise ProfileError(f"Missing configuration: '{self.config_path}' does not exist.")
        except json.JSONDecodeError:
            raise ProfileError(f"Malformed schema: Check '{self.config_path}' for trailing commas.")

    def fetch_country_stats(self) -> None:
        """Handshakes with the REST Countries API based on the home country."""
        country_name = self.profile_data.get("home_country")
        if not country_name:
            # We don't crash, we just skip fetching.
            return

        # URL encode country name (e.g. "United Kingdom" becomes "United%20Kingdom")
        encoded_country = urllib.parse.quote(country_name)
        url = f"https://restcountries.com/v3.1/name/{encoded_country}?fullText=true"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Portfolio-App/1.0"})
            with urllib.request.urlopen(req, timeout=5.0) as response:
                payload = json.loads(response.read().decode())
                
                if isinstance(payload, list) and len(payload) > 0:
                    self.live_country_data = payload[0]
                else:
                    raise APIError("No matching records found in the directory.")
        except urllib.error.HTTPError as http_err:
            if http_err.code == 404:
                raise APIError(f"Country '{country_name}' was not found in the official registry.")
            else:
                raise APIError(f"Server responded with status code {http_err.code}.")
        except urllib.error.URLError:
            raise APIError("Network handshake timed out. Check your local connection.")
        except Exception as err:
            raise APIError(f"Unexpected parsing anomaly: {str(err)}")

    def display(self) -> None:
        """Generates a clean terminal interface with native data fallback mechanisms."""
        print("\n" + "═" * 50)
        print("          💻 DEVELOPER PORTFOLIO CLI v2.0         ")
        print("═" * 50)
        
        # Safe lookups using dictionary fallback parameters
        print(f"👤 Name:       {self.profile_data.get('name', 'N/A')}")
        print(f"💼 Role:       {self.profile_data.get('role', 'N/A')}")
        print(f"🏫 Education:  {self.profile_data.get('university', 'N/A')}")
        print(f"📍 Home Base:  {self.profile_data.get('home_country', 'N/A')}")
        print("─" * 50)

        # Print dynamically fetched metadata if loaded
        if self.live_country_data:
            capital_list = self.live_country_data.get("capital", ["N/A"])
            capital = capital_list[0] if isinstance(capital_list, list) else capital_list
            population = self.live_country_data.get("population", 0)
            
            # Extracting nested dictionary properties cleanly
            currencies_dict = self.live_country_data.get("currencies", {})
            currency_desc = "N/A"
            if currencies_dict:
                first_currency_key = list(currencies_dict.keys())[0]
                currency_info = currencies_dict.get(first_currency_key, {})
                currency_desc = f"{currency_info.get('name', 'N/A')} ({currency_info.get('symbol', '')})"

            print("📊 LIVE GEOGRAPHIC STATS")
            print(f"🏛️ Capital:    {capital}")
            print(f"👥 Population: {population:,}")
            print(f"💵 Currency:   {currency_desc}")
        else:
            print("📊 LIVE GEOGRAPHIC STATS: [Unavailable or Incomplete Profile]")
            
        print("═" * 50 + "\n")


def main():
    portfolio = DeveloperPortfolio("profile.json")
    
    try:
        portfolio.load_profile()
        print("🔄 Connecting to REST Countries registry...")
        portfolio.fetch_country_stats()
        portfolio.display()
        
    except ProfileError as config_err:
        print(f"🛑 CRITICAL SETUP ERROR: {config_err}")
    except APIError as api_err:
        print(f"⚠️ API RETRIEVAL FAILURE: {api_err}")
        # Run display anyway to show whatever profile details loaded locally
        portfolio.display()
    except KeyboardInterrupt:
        print("\n👋 Process terminated by user.")

if __name__ == "__main__":
    main()