import discord
import diy as api
import db
import config

from discord.ext import tasks, commands
from datetime import datetime

from discord.ext import tasks, commands
from datetime import datetime

class ChessClient(discord.Client):
    def __init__(self):
        self.active = False
        super().__init__()
        
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        self.active = True

    async def on_message(self, message):
        # Don't respond to messages from bots
        if message.author == self.user or message.author.id == 913559549309489162:
            print(f"Bot message, not responding. [{message.content[:max(len(message.content), 30)]}...]")
            return
        else:
            print(f"Got message {message.content[:max(len(message.content), 70)]}")

        channel = message.channel

        # Check to see if it's a command
        match message.content.split(" "):
            # Put cases here...

            case _:
                print("No command found in message.")
                pass

def main():
    client = ChessClient()

    client.run(config.discord_client_token())

if __name__ == "__main__":
    main()
