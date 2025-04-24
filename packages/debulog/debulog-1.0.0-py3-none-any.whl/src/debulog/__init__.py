def log(message):
    print("DEBUG: " + message)

def warn(message):
    print("\033[93m" + "DEBUG: " + message + "\033[0m")

def error(message):
    print("\033[91m" + "DEBUG: " + message + "\033[0m")