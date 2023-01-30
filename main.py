import discord

intents = discord.Intents().all()
client = discord.Client(intents=intents)
ticket_count = 0
lock_emoji = "\U0001F512"

@client.event
async def on_message(message):
    global ticket_count
    if message.content.startswith("!create_ticket"):
        ticket_count += 1
        category = discord.utils.get(message.guild.categories, name="TICKETS")
        if not category:
            category = await message.guild.create_category("TICKETS")
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            message.guild.owner: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ticket_channel = await message.guild.create_text_channel(f"ticket-{ticket_count}", category=category, overwrites=overwrites)
        await message.channel.send(f"Ticket channel created: {ticket_channel.mention}")
        message = await ticket_channel.send(f"{message.author.mention} need a Infernal cape service!\n\n{message.author.mention} Opening a ticket means you read & agree our ToS!\n\nSupport will be with you shortly.\nTo close this ticket react with {lock_emoji}")
        await message.add_reaction(lock_emoji)

        @client.event
        async def on_message(message):
            global ticket_count
            if message.content.startswith("!create_ticket"):
                ticket_count += 1
                category = discord.utils.get(message.guild.categories, name="TICKETS")
                if not category:
                    category = await message.guild.create_category("TICKETS")
                overwrites = {
                    message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    message.guild.owner: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                ticket_channel = await message.guild.create_text_channel(f"ticket-{ticket_count}", category=category,
                                                                         overwrites=overwrites)
                await message.channel.send(f"Ticket channel created: {ticket_channel.mention}")
                message = await ticket_channel.send(
                    f"{message.author.mention} need a Infernal cape service!\n\n{message.author.mention} Opening a ticket means you read & agree our ToS!\n\nSupport will be with you shortly.\nTo close this ticket react with {lock_emoji}")
                await message.add_reaction(lock_emoji)

            elif message.content.startswith("$add"):
                user = None
                try:
                    user = await discord.ext.commands.MemberConverter().convert(ctx=message.channel,
                                                                                argument=message.content.split(" ")[1])
                except:
                    pass
                if not user:
                    user = discord.utils.get(message.guild.members, id=int(message.content.split(" ")[1].strip("<@!>")))
                if not user:
                    await message.channel.send(f"User not found.")
                    return
                overwrites = message.channel.overwrites_for(user)
                if overwrites.send_messages is None:
                    overwrites.send_messages = True
                    overwrites.read_messages = True
                    await message.channel.set_permissions(user, overwrite=overwrites)
                    await message.channel.send(f"{user.mention} has been added to the ticket.")
                else:
                    await message.channel.send(f"{user.mention} is already a member of this ticket.")


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    if reaction.emoji == lock_emoji and (user == reaction.message.author or user == reaction.message.guild.owner or user.permissions_in(reaction.message.channel).manage_channels):
        transcript_channel = None
        category = discord.utils.get(reaction.message.guild.categories, name="TRANSCRIPTS")
        if not category:
            category = await reaction.message.guild.create_category("TRANSCRIPTS")
        overwrites = {
            reaction.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            reaction.message.author: discord.PermissionOverwrite(read_messages=True),
            reaction.message.guild.owner: discord.PermissionOverwrite(read_messages=True)
        }
        async for message in reaction.message.channel.history(limit=None):
            if transcript_channel is None:
                transcript_channel = await reaction.message.guild.create_text_channel(f"ticket-{ticket_count}-transcript", category=category, overwrites=overwrites)
            transcript_message = f"{message.created_at} [{message.author}] {message.content}"
            await transcript_channel.send(transcript_message)
        await reaction.message.channel.delete()
print('please enter your token:')

TOKEN=input()
print(TOKEN)
client.run(TOKEN)