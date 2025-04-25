from cliapp import Application
from cliapp import Command
import asyncio

async def test(*args, n=False, t=False):
    print(*args)
    await asyncio.sleep("me")

if __name__ == "__main__":
    app = Application(config="tests/config.json")
    
    command = Command("test", test)
    command.addFlag("n", help="Should show number result")
    command.addFlag("t")
    
    # command.addSelection("option", [ "first", "second" ])
    command.addSelection("another", [ "me", "myself", "I" ])
    # command.addSelection("name", [ "Devin" ])
    
    app.add(command)
    
    app.run()