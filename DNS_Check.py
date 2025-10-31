"""
Miles Goldberger
10/20/25


This is a simple python script to list out the DNS records of a given domain
in order to automate the process of troubleshooting DNS issues

I initially created a script similar to this during my internship, but this is a refined version
"""

#dns.resolver does the majority of the work for me, connecting to the
#resolver and communicating to find the Authoritative Name Server
import dns.resolver
import sys

#Create a domain checker, when given domain it sorts
#through the DNS records, getting the address with the dns resolver
# then printing every address that was returned

#We repeat these steps for MX and TXT records
def check_domain(domain):
    print (f" Checking DNS Records for: {domain} ")

    try:
        a_records = dns.resolver.resolve(domain, 'a')

        print("IP Addresses: ")

        for record in a_records:
            print(f"| {record.to_text()} |")
    except Exception as e:
        print (f"A Record not found: {e}")

    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        print(f"Mail Servers: ")
        for record in mx_records:
            print (f"| {record.to_text()} |")
    except Exception as e:
        print(f"MX Record not found: {e}")

    # Specifically, for TXT records, we filter to figure out
    # If record is for SPF, DKIM, or other
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        print(f"TXT Records: ")
        for record in txt_records:
            record_text = record.to_text()
            if "v=spf1" in record_text:
                print(f" SPF | {record.to_text()} |")
            elif "v=DMARC1" in record_text:
                print(f" DMARC | {record.to_text()} |")
            else:
                print(f"Other | {record.to_text()} |")
    except Exception as e:
        print (f"TXT Record not found: {e}")


#Little error check to make sure user correctly calls
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must provide a domain")
        print("Ex: python DNS_Check.py google.com")
        sys.exit(1)

domain_to_check = sys.argv[1]

check_domain(domain_to_check)


