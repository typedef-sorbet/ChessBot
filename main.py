import discord
import db
import config
import itertools
import imgkit
from html2image import Html2Image

from discord.ext import tasks, commands
from datetime import datetime

from jinja2 import Environment, PackageLoader, select_autoescape

from PIL import Image

jinja_env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

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
                        self.render_board(db.get_board(inviter_id), "", "")

                        file = discord.File("/home/sanctity/chess_bot/rendered.png", filename="rendered.png")
                        embed = discord.Embed()
                        embed.set_image(url="attachment://rendered.png")

                        await channel.send(f"New game created between {inviter_name} and {invitee_name}", file=file, embed=embed)
                else:
                    await channel.send("One or both players unknown to the chess bot -- use !register to register yourself")

            case _:
                print("No command found in message.")
                pass

    def render_board(self, board_str, from_space, to_space):
        global jinja_env

        spaces = [
            {
                # Prepare for the worst Python ternary you've ever seen.
                "class": "highlighted_space" if space_name == from_space or space_name == to_space else ("white_space" if i % 2 == (i // 8) % 2 else "black_space"),
                # "content": "<p> </p>" if space_content == "x" else f'<img src="{space_content} width=80 height=80"></img>'
                "content": space_content,
                "name": space_name
            }
            for i, (space_content, space_name) in enumerate(zip(board_str.split(","), map(lambda x: "".join(x), itertools.product("abcdefgh", "12345678"))))
        ]

        template = jinja_env.get_template("board.html")
        rendered_html = template.render(spaces=spaces)

        hti = Html2Image()

        # screenshot an HTML string (css is optional)
        hti.screenshot(html_str=rendered_html, save_as='rendered.png', size=(900,900))

        # Sure. Whatever.
        im = Image.open("/home/sanctity/chess_bot/rendered.png")
        left = 8
        top = 18
        im1 = im.crop((left, top, left+800, top+800))

        im1.save("/home/sanctity/chess_bot/rendered.png")


def main():
    client = ChessClient()

    client.run(config.discord_client_token())

if __name__ == "__main__":
    main()
