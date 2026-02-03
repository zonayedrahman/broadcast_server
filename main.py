import cmd

from server import BroadcastServer

class ServerCLI(cmd.Cmd):
    intro = 'Welcome to the Broadcast Server CLI. Type help or ? to list commands.\n'
    prompt = 'broadcast-server '
    file = None

    def do_start(self, arg):
        'start: Starts up a server that listens for connections'
        
        broadcast_server = BroadcastServer()
        broadcast_server.start()

    def do_bye(self, arg):
        'bye: Exits the CLI'
        print('Closing....')
        return True


if __name__ == "__main__":
    server_cli = ServerCLI()
    server_cli.cmdloop()
