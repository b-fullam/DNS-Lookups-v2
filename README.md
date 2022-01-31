# DNS-Lookups-v2

Python script that functions like a CLI tool to perform both DNS and Reverse DNS lookups from either a single entry or in bulk from a list as input.  The script also provides an additional option to output the results to a text file.

## Automating DNS and Reverse DNS Lookups with optional reporting

Enter a single IP address or domain, or select either a list of IP addresses or domains to be submitted for DNS or Reverse DNS lookups.  You can also specify an option to output the results to a text file called "report.txt".

Here are the options included in the script:

``` noLineNumbers
usage: dns-revdns-lookup [-h] [-l] [-o] [-d DNS] [-r REV_DNS] [-V]

Python DNS & Reverse DNS Lookups v2.0 by Brett Fullam

options:
  -h, --help            show this help message and exit
  -l, --list            indicate list as input
  -o, --output          output report
  -d DNS, --dns DNS     DNS lookup
  -r REV_DNS, --rev-dns REV_DNS
                        Reverse DNS lookup
  -V, --version         show program version
```

### DNS Lookups

Here's a sample of the command to run the dns-revdns-lookup script using a single entry, google.com, as the input by using the "--dns" or "-d" option followed by the domain name.

``` noLineNumbers
python3 dns-revdns-lookup.py -d google.com 
```

Here's the output of the command in the example above:

``` noLineNumbers
DNS Lookup: google.com

google.com has address 142.251.129.142
google.com has IPv6 address 2800:3f0:4001:81e::200e
google.com mail is handled by 20 alt1.aspmx.l.google.com.
google.com mail is handled by 40 alt3.aspmx.l.google.com.
google.com mail is handled by 50 alt4.aspmx.l.google.com.
google.com mail is handled by 10 aspmx.l.google.com.
google.com mail is handled by 30 alt2.aspmx.l.google.com.


DNS & Reverse DNS Lookups Generated: Mon Jan 31 15:52:57 2022
created by Python DNS & Reverse DNS Lookups v2.0
```
To save the output to a text file, use the "--output" or "-o" option, as well as the "--dns" or "-d" option:
``` noLineNumbers
python3 dns-revdns-lookup.py -o -d google.com
```

To perform a DNS lookup from a list use the "--list" or "-l" option:
``` noLineNumbers
python3 dns-revdns-lookup.py -l -d test-domains.com
```
To perform a DNS lookup from a list and save the output to a text file, use the "--list" or "-l" option, as well as the "--output" or "-o" option:
``` noLineNumbers
python3 dns-revdns-lookup.py -l -o -d test-domains.com
```

> The generated report, named "report.txt", is saved in the same directory that the Python script resides.

### Reverse DNS Lookups

Here's a sample of the command to run the dns-revdns-lookup script using a single entry, 8.8.8.8, as the input by using the "--rev-dns" or "-r" option followed by the IP address.

``` noLineNumbers
python3 dns-revdns-lookup.py -r 8.8.8.8 
```

Here's the output of the command in the example above:

``` noLineNumbers
Reverse DNS Lookup: 8.8.8.8

8.8.8.8.in-addr.arpa domain name pointer dns.google.


DNS & Reverse DNS Lookups Generated: Mon Jan 31 16:02:28 2022
created by Python DNS & Reverse DNS Lookups v2.0
```
To save the output to a text file, use the "--output" or "-o" option, as well as the "--rev-dns" or "-r" option:
``` noLineNumbers
python3 dns-revdns-lookup.py -o -r 8.8.8.8 
```

To perform a Reverse DNS lookup from a list use the "--list" or "-l" option:
``` noLineNumbers
python3 dns-revdns-lookup.py -l -r test-ips.txt 
```
To perform a Reverse DNS lookup from a list and save the output to a text file, use the "--list" or "-l" option, as well as the "--output" or "-o" option:
``` noLineNumbers
python3 dns-revdns-lookup.py -l -o -r test-ips.txt 
```

> The generated report, named "report.txt", is saved in the same directory that the Python script resides.

## Getting Started 

1. Download the repository as a zip file, or use git to clone the repository.

2. Install dependencies.  The script was created using Python 3, and the only dependency you'll need to install is the "module re" (regex) to add support for regular expressions.  However, I've included a requirements.txt file that contains the specific version if you prefer to use the following command to install the dependencies instead:

``` noLineNumbers
pip3 install -r requirements.txt
```

3. I also included 2 text files for testing the list option ("--list" or "-l") for both DNS and Reverse DNS lookups.  One for domains, test-domains.txt, which has domains with intentional formatting errors to test the regex pattern for domains included in the script.  One for IP addresses, test-ips.txt, which includes a mix of public and private IP addresses, as well as a handful of improperly formatted IP addresses to test the 2 regex patterns for IPs included script.
