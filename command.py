command_list = [
    "'add ...' - with this command I save a new contact. Instead of '...', enter the name and phone number, \nnecessarily separated by a 'space'.",
    "'change ... - with this command I save the new phone number of an existing contact. Instead of '...', \nenter the name and phone number, necessarily with a 'space'.",
    "'phone ....' - With this command, I output the phone number for the specified contact. Instead of '...' \nenter the name of the contact whose number should be displayed.",
    "'show_all' - With this command, I output all saved contacts with phone numbers.",
    "'good bye', 'close', 'exit' by any of these commands I complete my work."
]

contact_list = {}

def hello(*args):

    print("    > How can I help you?! To find out the list of commands, write 'help'.")


def print_command(*args):

    print("\n")

    for comm in command_list:
        print(f"    > {comm}\n")


def new_contact(*args):
    
    contact_list.update([args[1:]])
    print(f"    > You have added a new contact: {' '.join(args[1:])}.\n")


def show_contact(*args):

    print(  f"    > {args[1]}: {contact_list[args[1]]}\n")


def show_all(*args):

    for it in contact_list.items():
        print(f"    > {it[0]}: {it[1]}\n")


def change(*args):

    contact_list.update([args[1:]])
    print(f"    > You have updated the contact {args[1]}: {args[2]}.\n")


OPERATIONS = {
    "exit": ["exit", "close", "good bye"],
    "hello": hello, 
    "help": print_command,
    "add": new_contact,
    "phone": show_contact,
    "show_all": show_all,
    "change": change
}