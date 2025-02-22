
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
    
    async def handle_command(self, context, bot):
        message = context.message
        if not message.content.startswith(self.prefix):
            return
        
        args = message.content[len(self.prefix):].split()
        command_name = args.pop(0).lower()
        if command_name in self.commands:
            try:
                command = self.commands[command_name]
                await command.func(bot, context, args)
            except Exception as e:
                print(e)
        else:
            print(f"Command '{command_name}' not found.")