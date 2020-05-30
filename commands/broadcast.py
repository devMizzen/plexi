import sys
import asyncio
from discord import Embed, Color

# Initialising arguments
client = sys.argv[1]
message = sys.argv[2]
text = sys.argv[3]

# I love my mom
sent_to = 0
total_guilds = 0

await message.channel.send("🕑 Please wait...")

# Sending your text EVERYWHERE
for guild in client.guilds:
    total_guilds += 1
    channel = None
    for text_channel in guild.text_channels:
        if "plexi-announcements" in text_channel.name:
            channel = text_channel
            break
    if channel is not None:
        try:
            await channel.send(text)
            sent_to += 1
        except Exception as e:
            print(f">>> Guild: {guild.name} | ID: {guild.id} | An exception occurred: {e}")

reply = Embed(
    title="✅ Success",
    description=f"Sent successfully to `{sent_to}` out of `{total_guilds}` guilds",
    color=Color.dark_green()
)
reply.set_footer(text=str(message.author), icon_url=str(message.author.avatar_url))
await message.channel.send(embed=reply)

var = 123
print(var)
sys.stdout.flush()