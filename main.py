import discord
import db
import config

from discord.ext import tasks, commands
from datetime import datetime

class ChessClient(discord.Client):
    def __init__(self):
        self.active = False
        super().__init__(intents=discord.Intents.all())
        
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
            case ["!start", *args]:
                # TODO implement a way for the other player to accept a game invite
                inviter_name = message.author.name
                invitee_name = " ".join(args)
                print(f"Got request to start a new game between {inviter_name} and {invitee_name}")

                inviter_known, inviter_id = config.player_known(inviter_name)
                invitee_known, invitee_id = config.player_known(invitee_name)

                if inviter_known and invitee_known:
                    success, reason = db.create_game(inviter_name, inviter_id, invitee_name, invitee_id)
                    if not success:
                        await channel.send(reason)
                    else:
                        # TODO send board
                        await channel.send("Game created.")
                else:
                    await channel.send("One or both players unknown to the chess bot -- use !register to register yourself")

            case _:
                print("No command found in message.")
                pass

def main():
    client = ChessClient()

    client.run(config.discord_client_token())

if __name__ == "__main__":
    main()
