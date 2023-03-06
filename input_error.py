def input_error(func):
    def inner():
        try:
           func() 
        except KeyError:
            print("I don't know this command or this contact does not exist... To find out the list of commands, write 'help'")
            inner()
    return inner