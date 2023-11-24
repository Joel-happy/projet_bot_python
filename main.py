import discord
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)


@client.command(name="Hello")
async def delete(ctx):
    messages = await ctx.channel.history(limit=10)

    for each_message in messages:
        await each_message.delete()


@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.event
async def on_typing(channel, user, when):
    await channel.send(user.name + " is typing")


@client.event
async def on_member_join(member):
    general_channel = client.get_channel()
    await general_channel.send("Bienvenue sur le serveur ! " + member.name)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message.content = message.content.lower()

    if message.content.startswith("hello"):
        await message.channel.send("Hello")

    if "cochon" in message.content:
        await message.channel.send("R")

    if message.content == "azerty":
        await message.channel.send("qwerty")

    await client.process_commands(message)

client.run("MTE2NzQ2ODk1MDg4NDQ2MjcwNg.G0H8UI.hSY0wwV6Y86v1cQaZ1ue-fPv-Z6QLpUNcLNtRQ")

#MTE2NzQ2ODk1MDg4NDQ2MjcwNg.G0H8UI.hSY0wwV6Y86v1cQaZ1ue-fPv-Z6QLpUNcLNtRQ