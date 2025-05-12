import requests
import re

"""
🔍 Domain Finder by TLD - crt.sh Scraper
----------------------------------------

This script allows users to search for domain names associated with a specific top-level domain (TLD)
(e.g., .com, .net, .fm) by querying the Certificate Transparency log database via crt.sh.

"""
def search_domains_by_extension():
    domain_extension = input("🔹 Enter the domain extension to search for (e.g., .com, .net, .fm): ").strip()
    
    if not domain_extension.startswith("."):
        print("❌ Invalid extension. Please include a dot (e.g., .com, .net, .org).")
        return

    url = f"https://crt.sh/?q=%{domain_extension}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        domains = set()
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

        for entry in data:
            name = entry.get("name_value", "")
            found_domains = name.split("\n")
            for domain in found_domains:
                clean_domain = domain.replace("www.", "").strip()  # Remove "www." and trailing spaces

                # Delete domains containing "*." or email
                if not email_pattern.search(clean_domain) and not clean_domain.startswith("*.") and clean_domain.endswith(domain_extension):
                    domains.add(clean_domain)

        if not domains:
            print(f"❌ No domains found for extension: {domain_extension}")
            return
        
        # Save unique domains in a file
        output_file = f"domains_{domain_extension[1:]}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(sorted(domains)))

        print(f"✅ Found {len(domains)} unique domains and saved them to: {output_file}")

    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}")

#  Run the function
search_domains_by_extension()
