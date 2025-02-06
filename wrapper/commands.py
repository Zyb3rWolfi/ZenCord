class Command:

    def __init__(self, name, func):
        self.name = name
        self.func = func
    
class CommandHandler:

    def __init__(self, prefix="!"):
        self.prefix = prefix
        
        self.commands = {}
    
    def command(self, name):

        def wrapper(func):
            self.commands[name] = Command(name, func)
            return func
        return wrapper
    
    async def handle_command(self, message, bot):
        content = message["content"]
        print(f"Received message: {content}")  # Debugging message content
        if not message["content"].startswith(self.prefix):
            print("Check 1")
            return
        
        args = message["content"][len(self.prefix):].split()
        command_name = args.pop(0).lower()
        print("Check 2")
        if command_name in self.commands:
            command = self.commands[command_name]
            await command.func(bot, message, args)
            try:
                print(f"Executing command: {command_name}")
            except Exception as e:
                print(f"Error while executing command '{command_name}': {e}")
        else:
            print(f"Command '{command_name}' not found.")