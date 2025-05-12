import dns.resolver  # type: ignore
import sys

# The Script Analyzing DNS records for a group of domains

def check_spf(domain):
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        spf_records = [rdata.to_text() for rdata in answers if "v=spf1" in rdata.to_text()]
        return spf_records if spf_records else None
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return f"Domain does not exist: {domain}"
    except Exception as e:
        return f"Error checking SPF for {domain}: {e}"

def check_mx(domain):
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return [rdata.exchange.to_text() for rdata in answers]
    except dns.resolver.NoAnswer:
        return []
    except dns.resolver.NXDOMAIN:
        return []
    except Exception:
        return []

def check_aaaa(domain):
    try:
        answers = dns.resolver.resolve(domain, "AAAA")
        return [rdata.to_text() for rdata in answers]
    except dns.resolver.NoAnswer:
        return []
    except dns.resolver.NXDOMAIN:
        return []
    except Exception:
        return []

def check_dns(domain):
    print(f"\nChecking DNS records for domain: {domain}")
    
    spf_result = check_spf(domain)
    if isinstance(spf_result, list):
        print(f"SPF records found: {spf_result}")
    else:
        print(spf_result or "No SPF records found")
    
    mx_result = check_mx(domain)
    print(f"MX records: {mx_result if mx_result else 'No MX records found'}")
    
    aaaa_result = check_aaaa(domain)
    print(f"AAAA records: {aaaa_result if aaaa_result else 'No AAAA records found'}")

    return spf_result, mx_result, aaaa_result

def check_group(domains):
    spf_plus_all = []
    spf_question_all = []
    mx_domain = []
    spf_other = []

    dns_results = []

    for domain in domains:
        try:
            spf_result, mx_result, aaaa_result = check_dns(domain)

            # SPF treatment
            if isinstance(spf_result, list):
                spf_combined = " ".join(spf_result)
                if "+all" in spf_combined:
                    spf_plus_all.append(domain)
                elif "?all" in spf_combined:
                    spf_question_all.append(domain)
                elif any(domain in mx for mx in mx_result): 
                    mx_domain.append(domain)
                else:
                    spf_other.append(domain)

            # Store detailed results
            dns_results.append(f"Domain: {domain}")
            dns_results.append(f"SPF: {spf_result if spf_result else 'No SPF records found'}")
            dns_results.append(f"MX: {mx_result if mx_result else 'No MX records found'}")
            dns_results.append(f"AAAA: {aaaa_result if aaaa_result else 'No AAAA records found'}")
            dns_results.append("\n" + "-"*50 + "\n")

        except Exception as e:
            dns_results.append(f"Error checking domain {domain}: {e}")
            continue

    # Save categories to files
    with open("spf_plus_all.txt", "w") as f:
        f.write("\n".join(spf_plus_all))

    with open("spf_question_all.txt", "w") as f:
        f.write("\n".join(spf_question_all))

    with open("spf_other.txt", "w") as f:
        f.write("\n".join(spf_other))

    with open("mx_match_domain.txt", "w") as f:
        f.write("\n".join(mx_domain))

    with open("dns_results.txt", "w") as f:
        f.write("\n".join(dns_results))

if __name__ == "__main__":
    input_domains = input("Enter the domains to check DNS records (e.g., example.com, domain2.com): ").strip()
    domains = [d.strip() for d in input_domains.split(",") if d.strip()]
    check_group(domains)
