# DNS Tools Suite

 A collection of Python scripts to inspect and analyze DNS records and discover domain names based on extensions.

## Features

- Check SPF, MX, and AAAA DNS records for any domain.
- Categorize SPF configurations (`+all`, `?all`, etc).
- Search and validate domain names based on TLD extensions.
- Export results to text files for easy reference.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mohammed-bakkali/dns-tools-suite.git
   ```

---

## Usage

1. Run the script:
   ```bash
   python dnsinspect.py
   ```

2. Enter the domains (comma-separated) when prompted:
   ```
   Enter the domains to check DNS records (e.g., example.com, domain2.com): example.com, domain2.com
   ```

3. The script will inspect the DNS records for each domain and output the results into the following files:
   - **`spf_plus_all.txt`**: Domains with `+all` in SPF records.
   - **`spf_question_all.txt`**: Domains with `?all` in SPF records.
   - **`spf_other.txt`**: Domains with other SPF configurations.
   - **`dns_results.txt`**: Detailed DNS records for all processed domains.

---

## Output Example

### `spf_plus_all.txt`
```
example.com
domain2.com
```

### `spf_question_all.txt`
```
domain3.com
```

### `dns_results.txt`
```
Domain: example.com
SPF: ['v=spf1 include:_spf.google.com ~all']
MX: MX records: ['alt1.aspmx.l.google.com.', 'aspmx.l.google.com.']
AAAA: No AAAA records found
--------------------------------------------------

Domain: domain2.com
SPF: No SPF records found
MX: No MX records found
AAAA: AAAA records: ['2606:4700:3033::ac43:abcd']
--------------------------------------------------
```

## Dependencies

- Python 3.x
- dnspython

Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with your enhancements.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

**Mohammed Bakkali**  
_Web Developer_  
