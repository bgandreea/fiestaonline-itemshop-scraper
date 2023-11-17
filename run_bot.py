import discord
from discord import app_commands

from utilities.helper import scan_for_items, client

# Initialize Discord bot
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=your_discord_server_id))
    print("Ready!")


@tree.command(name="scan_shop",
              description="Function that scans the Fiesta Online shop for Permanent items",
              guild=discord.Object(id=your_discord_server_id))
async def scan_shop(interaction):
    await interaction.response.send_message("@everyone Today's List of Permanent Items:")
    channel_id = interaction.channel_id
    await scan_for_items(channel_id)


client.run("your_discord_bot_secret_key")
