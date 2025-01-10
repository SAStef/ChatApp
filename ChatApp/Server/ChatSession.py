import sys

class ChatSession:
    def __init__(self, p):
        self.parent = p

def signal_handler(server_instance):
    print("\nServeren lukkes ned...")
    server_instance.running = False
    sys.exit(0)
