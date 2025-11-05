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

#Print out dmarc settings
def dmarcPrinter(record_txt):

    print("DMARC Found: ")

# Use a dictionary to transalate terms
    tag_dictionary = {
        "v" : "version",
        "p" : "protection",
        "rua": "send aggregates to",
        "ruf": "send forensics to",
        "pct" : "filter %",
        "sp" : "subdomain policy",
        "adkim" : "DKIM alignment",
        "aspf" : "spf alignment"
    }

    try:
        #Remove quotes and split up tags
        tags = record_txt.strip('"').split(';')

        #For every tag remove white space
        for tag in tags:
            tag.strip()
            if not tag:
                continue

        #Split at equals, get definition and print
            parts = tag.split('=')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()

                name = tag_dictionary.get(key, key)

                print(f"| {name} ({key}) : {value} | ")

    except Exception as e:
        print(f"Error printing DMARC records: {e}")











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

            else:
                print(f"Other | {record.to_text()} |")

    except Exception as e:
        print (f"TXT Record not found: {e}")

#Find dmarc records at the dmarc address
    try:
        dmarc_address = ("_dmarc." + domain)
        print(f"Checking DMARC record at: ({dmarc_address})")
        dmarc_records = dns.resolver.resolve(dmarc_address, "TXT")
        #Print out dmarc settings
        for record in dmarc_records:
            dmarcPrinter(record.to_text(dmarc_records))
    except Exception as e:
        print(f"No DMARC record found. {e}")


#Little error check to make sure user correctly calls
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You must provide a domain")
        print("Ex: python DNS_Check.py google.com")
        sys.exit(1)

domain_to_check = sys.argv[1]

check_domain(domain_to_check)


