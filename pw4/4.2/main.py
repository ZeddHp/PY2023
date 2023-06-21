# pip install pandas
import pandas as pd

# file_name = input("Enter file name: ")
file_name = "mbox-short.txt"
domain_list = []

with open(f'../Data/{file_name}', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith("From "):
            email = line.split()[1]
            domain = email.split('@')[1]
            domain_list.append(domain)

# create unique list of domains and count of emails from each domain
domain_set = {}

for domain in domain_list:
    domain_set[domain] = domain_set.get(domain, 0) + 1

# print domain_email_count
print(domain_set)

# print unique domains and their email count
sorted_domain_list = sorted(set(domain_list))

# print sorted data in tabular format
header = ['Domain', 'Count', '(*)']
data = []
for domain in sorted_domain_list:
    count = domain_list.count(domain)
    asterisks = '*' * domain_set[domain]
    data.append((domain, count, asterisks))

df = pd.DataFrame(data, columns=header)
print(df)
