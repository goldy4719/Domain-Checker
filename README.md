# DNS & Email Security Checker (Python)

This is a command-line utility built in Python to query and validate a domain's critical DNS records. I created this tool to refine and automate the DNS troubleshooting I performed during my cybersecurity internship.

Its primary purpose is to quickly audit a domain's email security posture by analyzing its **SPF** and **DMARC** records—protocols I was responsible for deploying for regulated clients (HIPAA, NIST 800-171) at my MSP. This project directly demonstrates my hands-on experience with the protocols Mr. Mussman and I discussed.

## Features

* **Multi-Record Query:** Gathers `A` (IP Address), `MX` (Mail Server), and `TXT` (SPF) records from the root domain.
* **Correct DMARC Implementation:** Correctly queries the `_dmarc` subdomain (`_dmarc.domain.com`) to find the DMARC policy, mimicking the behavior of real-world mail servers.
* **Human-Readable DMARC Parser:**
    * The tool doesn't just print the DMARC record; it parses the `v=DMARC1; p=reject...` string.
    * It uses a Python dictionary (a key-value map) to translate technical tags (e.g., `p`, `rua`) into friendly, human-readable names ("Policy", "Send Aggregates To") for a clean report.
* **Graceful Error Handling:** Built with `try...except` blocks to handle non-existent domains or missing records without crashing.

## How to Use

This script requires the `dnspython` library.

1.  **Install the dependency:**
    ```bash
    pip install dnspython
    ```

2.  **Run the script from your terminal:**
    ```bash
    python DNS_Check.py <domain_to_query>
    ```

3.  **Example:**
    ```bash
    python DNS_Check.py google.com
    ```
