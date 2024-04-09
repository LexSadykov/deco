import re
import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3]).split(" ")
    while len(full_name) < 3:
        full_name.append("")
    contact[:3] = full_name[:3]

    phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?\s*-?(\d{3})-?(\d{2})-?(\d{2})(?:\s*\(?(доб.)\s*(\d+)\)?)?"
    )
    contact[5] = phone_pattern.sub(r"+7(\2)\3-\4-\5 \6\7", contact[5]).strip()
    contact[5] = contact[5].replace("доб.", "доб.").strip() 

unique_contacts = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key not in unique_contacts:
        unique_contacts[key] = contact
    else:
        for i in range(2, len(contact)):
            if contact[i] and not unique_contacts[key][i]:
                unique_contacts[key][i] = contact[i]

unique_contacts_list = [contacts_list[0]] + list(unique_contacts.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(unique_contacts_list)

pprint(unique_contacts_list)