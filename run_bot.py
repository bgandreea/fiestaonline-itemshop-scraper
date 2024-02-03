import discord
from discord import app_commands

from utilities.helper import scan_for_items, client
from utilitie import environment

# Initialize Discord bot
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=environment.DISCORD_SERVER_ID))
    print("Ready!")


@tree.command(name="scan_shop",
              description="Function that scans the Fiesta Online shop for Permanent items",
              guild=discord.Object(id=environment.DISCORD_SERVER_ID))
async def scan_shop(interaction):
    await interaction.response.send_message("@everyone Today's List of Permanent Items:")
    channel_id = interaction.channel_id
    await scan_for_items(environment.CHANNEL_ID)


client.run(f"{environment.DISCORD_BOT_SECRET_KEY}")
