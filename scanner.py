import requests
import copy
from bs4 import BeautifulSoup, SoupStrainer

target_domain = "https://google.com"
content = requests.get(target_domain).content

links = set()


def check_target_domain(domain):
    if domain[-1] == "/":
        return domain[:-1]
    else:
        return domain
    

def discover_directory(domain):
    hrefs = set()
    try:
        content = requests.get(domain).content
    except requests.exceptions.ConnectionError:
        pass
    except Exception as e:
        print(f"requests error: {e}")
    
    for link in BeautifulSoup(content, features="html.parser", parse_only=SoupStrainer("a")):
        if hasattr(link, "href"):
            try:
                path = link["href"]
                if (path.startswith("#")
                    or path.startswith("javascript")
                    or path.endswith(".jpg")
                    or path.endswith(".png")
                    or path.endswith(".css")
                    or path.endswith(".js")):
                    continue
                elif path.startswith("/") or path.startswith("?"):
                    hrefs.add(f"{target_domain}{path}")
                elif target_domain not in path and not path.startswith("http"):
                    hrefs.add(f"{target_domain}/{path}")
                else:
                    hrefs.add(path)
            except KeyError:
                pass
            except Exception as e:
                print(f"Error when parsing: {e}")
    
    for href in hrefs:
        if href.startswith(target_domain):
            links.add(href)


if __name__ == "__main__":
    target_domain = check_target_domain(target_domain)
    
    print("""
 __        _______ ____    ____   _  _____ _   _ 
 \\ \\      / / ____| __ )  |  _ \\ / \\|_   _| | | |
  \\ \\ /\\ / /|  _| |  _ \\  | |_) / _ \\ | | | |_| |
   \\ V  V / | |___| |_) | |  __/ ___ \\| | |  _  |
    \\_/\\_/  |_____|____/  |_| /_/   \\_\\_| |_| |_|
    / ___| / ___|  / \\  | \\ | | \\ | | ____|  _ \\    
    \\___ \\| |     / _ \\ |  \\| |  \\| |  _| | |_) |   
     ___) | |___ / ___ \\| |\\  | |\\  | |___|  _ <    
    |____/ \\____/_/   \\_\\_| \\_|_| \\_|_____|_| \\_\\   made by MadMatrix
    """)

    print("Enter a website URL to start scanning (e.g., https://example.com):")
    user_input = input("> ").strip()
    
    if user_input:
        target_domain = check_target_domain(user_input)
        discover_directory(target_domain)
        links_copy = copy.deepcopy(links)
        print(f"Start Scanning on {len(links_copy)} Links.....")
        
        for link in links_copy:
            print(f"Searching on... {link}")
            discover_directory(link)
        
        print(f"Found {len(links)} Links !!!")
    else:
        print("No URL provided. Exiting.")
