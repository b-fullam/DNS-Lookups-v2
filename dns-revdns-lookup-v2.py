import subprocess
import re
import time
import argparse


# //////////////////////////////////////////////
#
# Python Automated DNS and Reverse DNS Lookups v2.0
# by Brett Fullam
#
# DNS and Reverse DNS Lookups
# Bulk DNS and Reverse DNS Lookups
# Option to generate a report.txt file
#
# //////////////////////////////////////////////


# Initiate the parser
parser = argparse.ArgumentParser(prog='dns-revdns-lookup', description="Python DNS & Reverse DNS Lookups v2.0 by Brett Fullam")
parser.add_argument('-l', "--list", help="indicate list as input", action="store_true")
parser.add_argument("-o", "--output", help="output report", action="store_true")
parser.add_argument("-d", "--dns", help="DNS lookup")
parser.add_argument("-r", "--rev-dns", help="Reverse DNS lookup")
parser.add_argument("-V", "--version", help="show program version", action="store_true")


#/////////////  BEGIN -- timestamp

# grab the epoch timestamp at run time and convert to human-readable for the artifact output document footer information
timeStamp = time.time()

# convert epoch timestamp to human-readable date time formatted
report_time = time.strftime('%c', time.localtime(timeStamp))

# create a custom string to be included at the end of the generated output
report_time_footer = str('DNS & Reverse DNS Lookups Generated: ') + report_time + str('\ncreated by Python DNS & Reverse DNS Lookups v2.0') + str('\n\n')

#/////////////  END -- timestamp



# ///////////////// START DNS Lookup

lookupData = []

def dnsLookup(arg):

    # set lookupData to a global value to share the stored value with other functions
    global lookupData

    # initialize array
    lookupData = []

    # use subprocess to call the host command in the os
    process = subprocess.Popen(['host', arg], 
                               stdout=subprocess.PIPE,
                               encoding='utf-8')
    data = process.communicate()
    # uncomment to test subprocess "host" output
    # print(data[0])
    
    # Save data variable information to the global lookupData variable so it will be accessible outside of the dnsLookup() function.
    lookupData = data[0]
    
# ///////////////// END DNS Lookup



# ///////////////// START DNS Lookup LIST

# this function will handle importing a user defined list of domains, grab the most complete parts of the domain entries, and store them in an array called lst.  Then each validated entry will be submitted to the urlReport() function, and an html table will be returned for each of them and stored in an array called html_table_array.

def dnsLookupList(arg):
    
    # open and read the file containing a list of domain names
    with open(arg) as fcontent:
        fstring = fcontent.readlines()
    
    # declaring the regex pattern to grab the most complete parts of the domain entries from a list to reduce errors
    pattern = re.compile(r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?')

    # set lst to a global value to share the stored value with other functions
    global lst

    # initialized array
    lst=[]
    
    # extracting the domains
    for line in fstring:
        lst.append(pattern.search(line)[0])

    # iterate through the array of domains
    # with the dnsLookup() function
    for i in lst:
        dnsLookup(i)
    
# ///////////////// END DNS Lookup LIST


# ///////////////// START REVERSE DNS Lookup LIST

# this function will handle importing a user defined list of IP addresses, sort each IP as public or private IP range, and store them in separate arrays called Public_IPs or Private_IPs.  Then, since we are only interested in public IPs, only the IPs stored in the Public_IPs array will be validated and submitted to the dnsLookup() function. 

def dnsLookupRevList(arg):

    # open and read the file containing a list of IPs
    with open(arg) as fh:
        string = fh.readlines()

    # declaring a regex pattern to filter Private from Public IP addresses in a list
    pattern = re.compile(r'(^0\.)|(^10\.)|(^100\.6[4-9]\.)|(^100\.[7-9]\d\.)|(^100\.1[0-1]\d\.)|(^100\.12[0-7]\.)|(^127\.)|(^169\.254\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.0\.0\.)|(^192\.0\.2\.)|(^192\.88\.99\.)|(^192\.168\.)|(^198\.1[8-9]\.)|(^198\.51\.100\.)|(^203.0\.113\.)|(^22[4-9]\.)|(^23[0-9]\.)|(^24[0-9]\.)|(^25[0-5]\.)')

    # initialized array
    Private_IPs =[]
    Public_IPs=[]

    # extracting the IP addresses
    for line in string:
        line = line.rstrip()
        result = pattern.search(line)

        if result:
            Private_IPs.append(line)
        else:
            Public_IPs.append(line)
    
    
    """
    Display the sorted Private and Public IP addresses found in the imported list for debugging purposes.

    print("Private IPs")
    print(Private_IPs)
    
    print("Public IPs")
    print(Public_IPs)

    """
    
    # declaring a regex pattern to further filter the list for valid Public IP addresses
    pattern2 =re.compile(r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])')
    
    # set valid2 to a global value to share the stored value with other functions
    global valid2

    # initialized arrays
    valid2 =[]
    invalid2=[]

    # extracting the valid PUblic IP addresses
    for i in Public_IPs:
        i = i.rstrip()
        result = pattern2.search(i)
        
        if result:
            valid2.append(i)
        else:
            invalid2.append(i)

    # displaying the sorted valid IP addresses prior to running the reverse dns lookup
    print("Valid Public IP Addresses Found:")
    
    # uncomment for testing the valid IP addresses stored in valid2
    # for v in valid2:
    #    print(v)

    # uncomment to display invalid ip addresses for debugging
    # for iv in invalid2:
    #    print(iv)

    # iterate through the array of valid public ip addresses
    # with the dnsLookup function
    for i in valid2:
        dnsLookup(i)

# ///////////////// END REVERSE DNS Lookup LIST



# //////////////////////////  START COMMAND-LINE Arguments

# Read arguments from the command line
args = parser.parse_args()

# Check for --list or -l, --output or -o, AND --dns or -d
if args.list == True and args.output == True and args.dns:
    # create and open a file named 'report.txt' to write our data to
    f = open("report.txt" , "w")
    # BEGIN Report Content
    print("\nDNS Lookup Report: \n")
    f.write("\nDNS Lookup Report: \n\n")
    # send the path and/or file name of a list of domains to the dnsLookupList() function
    dnsLookupList(args.dns)
    # iterate over the list of domains, and print each entry to the screen as a list of domains included in the DNS Lookup analysis
    # write the same list to the report.txt file
    for i in lst:
        print(i)
        f.write(i + "\n")
    print("\n")
    # for each entry in the lst variable returned by the dnsLookupList() function
    # print dnsLookup() results to the screen
    # write dnsLookup() results to the report.txt file
    f.write("\n")
    for i in lst:
        print("\n" + i + "\n")
        f.write("\n" + i + "\n\n")
        #f.write("\n\n")
        dnsLookup(i)
        print(lookupData)
        f.write(lookupData)
        f.write("\n")
    # print human readable timestamp from the host system
    # to the screen and write to report.txt file
    print("\n" + report_time_footer)
    f.write("\n")
    f.write(report_time_footer)
    # close the report.txt file
    f.close()  
# Check for --list or -l AND --dns or -d
elif args.list == True and args.dns:
    print("\nDNS Lookup Report: \n")
    # send the path and/or file name of a list of domains to the dnsLookupList() function
    dnsLookupList(args.dns)
    # iterate over the list of domains, and print each entry to the screen as a list of domains included in the DNS Lookup analysis
    # write the same list to the report.txt file
    for i in lst:
        print(i)
    print("\n")
    # for each entry in the lst variable returned by the dnsLookupList() function
    # print dnsLookup() results to the screen
    for i in lst:
        print("\n" + i + "\n")
        dnsLookup(i)
        print(lookupData)
    # print human readable timestamp from the host system
    print("\n" + report_time_footer)    

# Check for --output or -o AND --dns or -d
elif args.output == True and args.dns:
    # create and open a file named 'report.txt' to write our data to
    f = open("report.txt" , "w")
    # BEGIN Report Content
    print("\nDNS Lookup: " + args.dns + "\n")
    # send the path and/or file name of a domain to the dnsLookup() function
    dnsLookup(args.dns)
    # print dnsLookup() results to the screen
    # write dnsLookup() results to the report.txt file
    print(lookupData)
    f.write("\nDNS Lookup: " + args.dns + "\n\n")
    f.write(lookupData + "\n\n")
    # print human readable timestamp from the host system
    # to the screen and write to report.txt file
    print("\n" + report_time_footer)
    f.write(report_time_footer)
    # close the report.txt file
    f.close()    
# Check for --dns or -d
elif args.dns:
    print("\nDNS Lookup: " + args.dns + "\n")
    dnsLookup(args.dns)
    # print dnsLookup() results to the screen
    print(lookupData)
    # print human readable timestamp from the host system
    # to the screen
    print("\n" + report_time_footer)
# Check for --list or -l, --output or -o, AND --rev_dns or -r
elif args.list == True and args.output == True and args.rev_dns:
    # create and open a file named 'report.txt' to write our data to
    f = open("report.txt" , "w")
    # BEGIN Report Content
    print("\nReverse DNS Lookup Report: \n")
    f.write("\nReverse DNS Lookup Report: \n\n")
    # send the path and/or file name of a list of domains to the dnsLookupRevList() function
    dnsLookupRevList(args.rev_dns)
    # iterate over the list of IP addresses, and print each entry to the screen as a list of IPs included in the Reverse DNS Lookup analysis
    # write the same list to the report.txt file
    f.write("Valid Public IP Addresses Found:\n")
    for i in valid2:
        print(i)
        f.write(i + "\n")
    print("\n")
    # for each entry in the valid2 variable returned by the dnsLookupRevList() function
    # print dnsLookup() results to the screen
    # write dnsLookup() results to the report.txt file
    f.write("\n")
    for i in valid2:
        print("\n" + i + "\n")
        f.write("\n" + i + "\n\n")
        dnsLookup(i)
        print(lookupData)
        f.write(lookupData)
        f.write("\n")
    # print human readable timestamp from the host system
    # to the screen and write to report.txt file
    print("\n" + report_time_footer)
    f.write("\n")
    f.write(report_time_footer)
    # close the report.txt file
    f.close()  
# Check for --list or -l AND --rev-dns or -r
elif args.list == True and args.rev_dns:
    print("\nReverse DNS Lookup Report: \n")
    # send the path and/or file name of a list of domains to the dnsLookupRevList() function
    dnsLookupRevList(args.rev_dns)
    # iterate over the list of IP addresses, and print each entry to the screen as a list of IPs included in the Reverse DNS Lookup analysis
    for i in valid2:
        print(i)
    print("\n")
    # for each entry in the valid2 variable returned by the dnsLookupRevList() function
    # print dnsLookup() results to the screen
    for i in valid2:
        print("\n" + i + ": \n")
        dnsLookup(i)
        print(lookupData)
    # print human readable timestamp from the host system
    # to the screen
    print("\n" + report_time_footer) 
# Check for --output or -o AND --rev-dns or -r
elif args.output == True and args.rev_dns:
    # create and open a file named 'report.txt' to write our data to
    f = open("report.txt" , "w")
    # BEGIN Report Content
    print("\nReverse DNS Lookup: " + args.rev_dns + "\n")
    # send the path and/or file name of an IP address to the dnsLookup() function
    dnsLookup(args.rev_dns)
    # print dnsLookup() results to the screen
    # write dnsLookup() results to the report.txt file
    print(lookupData)
    f.write("\nReverse DNS Lookup: " + args.rev_dns + "\n\n")
    f.write(lookupData + "\n\n")
    # print human readable timestamp from the host system
    # to the screen and write to report.txt file
    print("\n" + report_time_footer)
    f.write(report_time_footer)
    # close the report.txt file
    f.close() 
# Check for --rev-dns or -r
elif args.rev_dns:
    # BEGIN Report Content
    print("\nReverse DNS Lookup: " + args.rev_dns + "\n") 
    # send the path and/or file name of an IP address to the dnsLookup() function
    dnsLookup(args.rev_dns)
    # print dnsLookup() results to the screen
    print(lookupData)
    # print human readable timestamp from the host system
    # to the screen
    print("\n" + report_time_footer)
# Check for --version or -V
elif args.version:
    print("DNS & Reverse DNS Lookups version 2.0")
# Print usage information if no arguments are provided
else:
    print("usage: dns-revdns-lookup [-h] [-l] [-o] [-d DNS] [-r REV_DNS] [-V]")

# //////////////////////////  END COMMAND-LINE Arguments