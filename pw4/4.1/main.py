
email_list = []  # list to store email addresses

# file_name = input("Enter file name: ")
file_name = "mbox-short.txt"

# with open(file_name, 'r') as f:
with open(f'../Data/{file_name}', 'r') as f:
    # read lines from file
    lines = f.readlines()
    # iterate through lines
    for line in lines:
        # if line starts with 'From ' add to from_list
        if line.startswith("From "):
            # split line into components
            components = line.split()

            # get email address
            email = components[1]

            # add email to email_list
            email_list.append(email)

# sort email_list
email_list.sort()

# print emails in email_list
for email in email_list:
    print(email, '\n', end='')

# from_list size
print(
    f'There were {len(email_list)} lines in the file with From as the first word')
