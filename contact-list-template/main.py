import json

CONTACT_FILE_PATH = "contacts.json"

def read_contacts(file_path):
    try:
        with open(file_path, 'r') as f:
            contacts = json.load(f)['contacts']
    except FileNotFoundError:
        contacts = []

    return contacts

def write_contacts(file_path, contacts):
    with open(file_path, 'w') as f:
        contacts = {"contacts": contacts}
        json.dump(contacts, f, indent=6)

def command_prompt():

    while True:
        command = input("Type a command: ").lower()

        if command == "add":
            add_contact(CONTACT_FILE_PATH)

        elif command == "delete":
            delete_contact(CONTACT_FILE_PATH)

        elif command == "list":
            existing_contacts = read_contacts(CONTACT_FILE_PATH) #need to recall existing contacts to account for newly added contacts
            list_contacts(existing_contacts)

        elif command == "search":
            existing_contacts = read_contacts(CONTACT_FILE_PATH)
            search_for_contact(existing_contacts)

        elif command == "q":
            break

        else:
            print("Please enter a valid command")

    return False

def verify_email_address(email):
    if len(email) > 0:

        if "@" not in email:
            return False

        split_email = email.split("@")
        identifier = "".join(split_email[:-1])
        domain = split_email[-1]

        if len(identifier) < 1:
            return False

        if "." not in domain:
            return False

        split_domain = domain.split(".")

        for section in split_domain:
            if len(section) == 0:
                return False

    return True

def verify_phone_number(contact):
    mobile = contact["mobile"]
    home = contact["home"]
    if len(mobile) > 0:

        if "-" or "(" or ")" in mobile:
            new_mobile = mobile.replace("-", "")
            if "(" in new_mobile:
                new_mobile = new_mobile.replace("(", "")
            if ")" in new_mobile:
                new_mobile = new_mobile.replace(")", "")
            if len(new_mobile) != 10:
                print("Invalid mobile phone number.")
                return False
        else:
            if len(mobile) != 10:
                print("Invalid mobile phone number.")
                return False

    if len(home) > 0:

        if "-" or "(" or ")" in home:
            new_home = home.replace("-", "")
            if "(" in new_home:
                new_home = new_home.replace("(", "")
            if ")" in new_home:
                new_home = new_home.replace(")", "")
            if len(new_home) != 10:
                print("Invalid home phone number.")
                return False
        else:
            if len(home) != 10:
                print("Invalid home phone number.")
                return False

    return True

            
def contact_exists(first_name, last_name, existing_contacts):
    for contact in existing_contacts:
        if first_name.lower() == contact["first_name"].lower() and last_name.lower() == contact["last_name"].lower():
            return True
        
def add_contact(contacts):
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    mobile = input("Mobile Phone Number: ")
    home = input("Home Phone Number: ")
    email = input("Email Address: ")
    address = input("Address: ")
    info = {"first_name": first_name, "last_name": last_name, "mobile": mobile, "home": home, "email": email, "address": address}
    existing_contacts = read_contacts(contacts) #if no existing contacts will create empty list

    if not first_name.split() or not last_name.split():
        print("You entered invalid information, this contact was not added.")

    elif contact_exists(first_name, last_name, existing_contacts):
        print(f"A contact with this name already exists.\n"
              "You entered invalid information, this contact was not added.")
    
    elif not verify_phone_number(info):
        print("You entered invalid information, this contact was not added.")

    elif not verify_email_address(info["email"]):
        print("Invalid email address.\n"
              "You entered invalid information, this contact was not added.")

    else:
        existing_contacts.append(info)
        write_contacts(contacts, existing_contacts)

def search_for_contact(contacts):
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    searched_contacts = []
    for contact in contacts:
        if len(first_name) > 0 and first_name.lower() in contact["first_name"].lower():
            searched_contacts.append(contact)
        if len(last_name) > 0 and last_name.lower() in contact["last_name"].lower():
            searched_contacts.append(contact)

    list_contacts(searched_contacts)

def delete_contact(contacts):
    existing_contacts = read_contacts(contacts)
    del_first_name = input("First Name: ")
    del_last_name = input("Last Name: ")
    for contact in existing_contacts:
        if del_first_name.lower() == contact["first_name"].lower() and del_last_name.lower() == contact["last_name"].lower():
            print("found")
            confirm = input("Are you sure you want to delete this contact (y/n)? ").lower()
            if confirm == "no" or confirm == "n":
                break
            if confirm == "yes" or confirm == "y":
                existing_contacts.remove(contact)
                write_contacts(contacts, existing_contacts)
                print("Contact deleted!")
                break
        
    else:
        print("No contact with this name exists.")

def list_contacts(contacts):
    contact_number = 1
    for contact in contacts:
        first_name = contact["first_name"]
        last_name = contact["last_name"]
        print(f"{contact_number}. {first_name} {last_name}")
        for key in contact:  
            if key != "first_name" and key != "last_name":
                if len(contact[key]) > 0:
                    print(f"      {key.capitalize()}: {contact[key]}")
        
        contact_number += 1

def main(contacts_path):
    print(f'\nWelcome to your contact list!\n\n'
          f'The following is a list of usable commands:\n'
          f'"add"' + ': Adds a contact\n'
          f'"delete"' + ': Deletes a contact.\n'
          f'"list"' + ': Lists all contacts.\n'
          f'"search"' + ': Searches for a contact by name.\n'
          f'"q"' + ': Quits the program and saves the contact list.\n\n')
    command_prompt()
    print("Contacts were saved successfully.")

if __name__ == "__main__":
    main(CONTACT_FILE_PATH)


