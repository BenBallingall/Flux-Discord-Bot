from ibdd import IssueBasedDD
from itertools import cycle
import asyncio
from discord.ext import commands
import discord
import os
from blockchain import Blockchain, Block
print("Flux Discord Bot")

blockchain = Blockchain()


TOKEN = os.environ['IBDD_DISCORD_BOT_TOKEN']

client = commands.Bot(command_prefix='!')

status = ['Have fun!', 'VOTE FLUX', 'Type: !IBDD']


async def get_issue(issue_id):
    issue_data = issue_id.split('-')
    server = client.get_guild(id=int(issue_data[0]))
    channel = client.get_channel(int(issue_data[1]))
    message = await channel.fetch_message(int(issue_data[2]))
    return(message.content.replace('!IBDD ', '').replace('"', ''))


async def update_blockchain():
    await client.wait_until_ready()
    while not client.is_closed():
        new_data = 'new_data.txt'
        if new_data in os.listdir():
            f = open(new_data, 'r')
            data = ''
            for line in f:
                data = line
            f.close()
            blockchain.mine(Block(data))
            os.remove(new_data)
            server = client.get_guild(id=551999201714634752)
            channel = client.get_channel(645889124817043457)
            await channel.send(blockchain.block)
        await asyncio.sleep(5)


@client.event
async def on_ready():
    # game = discord.Game(name='Type: !IBDD')
    # await client.change_presence(status=discord.Status.idle, activity=game)
    print('Bot ready!')
    server_id = '551999201714634752'
    server = client.get_guild(server_id)
    if server:
        print("Yes")
    else:
        print("No")
    user = await client.fetch_user("449910203220099073")

    await user.send("Hello , i'm awake")

    print(user)


# unicode form http://www.fileformat.info/info/unicode/char/274e/index.htm
ibdd_emojis = ['\u2611', '\u274E', '\U0001F48E', '\U0001F4CA']


@client.event
async def on_message(message):
    # print("message.author: " + str(message.author) + "con: "+message.content[:10])
    if str(message.author) == 'Flux Bot#8753' and message.content[:10] == "**Vote: **":
        for emoji in ibdd_emojis:
            await message.add_reaction(emoji)
    if str(message.author) == 'Flux Bot#8753' and message.content[:8] == "You will":
        # print("YOU WILLL")
        for emoji in ibdd_emojis[:2]:
            await message.add_reaction(emoji)

    await client.process_commands(message)

# write message
@client.command(pass_context=True)
async def IBDD(ctx, *args):
    server_id = ctx.message.guild.id
    channel_id = ctx.message.channel.id
    message_id = ctx.message.id
    server = client.get_guild(id=server_id)
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    print(message.content)
    if len(args) == 0:
        await ctx.send('**To create an IBDD issue to be voted on type: ** \n !IBDD "Issue to be voted on"')
    elif len(args) == 1:
        issue_id = str(server_id) + '-' + str(channel_id) + '-' + str(message_id)
        # global new_ibdd
        print(args[0])
        if not issue_id in os.listdir():
            f = open(issue_id, 'w')
            f.write(args[0])
            f.close()
        # new_ibdd = IssueBasedDD(issue_id, str(args[0]))
        if server:
            for member in server.members:
                if 'Flux Bot#8753' != str(member) and 'Flux Projects#3812' != str(member):
                    print('name: {}'.format(member))
                    await member.send('**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote\n`{}`'.format(issue_id))
                    # await client.send_message(member, '**Vote: **' + str(args[0])+'\n:ballot_box_with_check: YES \n:negative_squared_cross_mark: NO \n:gem: Convert vote to Political Capital \n:bar_chart:  Trade Political Capital for share in vote')
        await ctx.send('**Vote for** *{}* **will end in 5 mins**'.format(args[0]))
    else:
        await ctx.send('*error*')

# write message
@client.command()
async def use(ctx, *args):
    new_data = 'new_data.txt'
    use_ammount = float(args[0])
    issue_id = args[1]
    issue_message = await get_issue(issue_id)
    user = ctx.message.author.id
    current_bal = 50.22  # make function to get new bal
    new_bal = current_bal - use_ammount
    print(issue_message)
    f = open(new_data, 'a+')
    f.write('["{}","{}",{},{}],'.format(user, issue_id, use_ammount, new_bal))
    f.close()
    await ctx.send("You used {} PC credits\n`{}`".format(use_ammount, issue_id))


# Read and write
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


# Delete messages
@client.command(pass_context=True)
async def clear(ctx, amount=100):
    if str(ctx.message.author) == 'KipDawgz#8789':
        channel = ctx.message.channel
        messages = []
        counter = 0
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say('Messages deleted')


# assign Roles
@client.event
async def on_member_join(member):
    role = doscord.utils.get(member.server.roles, name='Cool People')
    await client.add_roles(member, role)


@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = message.channel
    if str(user.name) != 'Flux Bot':
        # print(reaction.emoji, user.name)
        if message.content[:10] == "**Vote: **":

            issue_id = message.content.split('\n')[-1].replace('`', '')
            issue_message = await get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[0]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await user.send('You have voted **YES** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
                # print(user.id)
                # print(user.name)
                # new_ibdd.vote_yes(user.id)
            elif reaction.emoji == ibdd_emojis[1]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await user.send('You have voted **NO** {} to the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[2]:
                await message.remove_reaction(ibdd_emojis[3], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await message.remove_reaction(ibdd_emojis[2], message.author)
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await user.send('You have opted to ** Convert vote to Political Capital** {} for the issue: *{}*\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
            elif reaction.emoji == ibdd_emojis[3]:
                await user.send('You will **Trade Political Capital for share in vote** {} for the issue: \n*"{}"* \nHow would you like to vote?\n`{}`'.format(reaction.emoji, reaction.message.content.split('\n')[0][10:], issue_id))
        elif message.content[:8] == "You will":
            issue_id = message.content.split('\n')[-1].replace('`', '')
            issue_message = await get_issue(issue_id)
            if reaction.emoji == ibdd_emojis[1] or reaction.emoji == ibdd_emojis[0]:
                await message.remove_reaction(ibdd_emojis[0], message.author)
                await message.remove_reaction(ibdd_emojis[1], message.author)
                await user.send('How much PC whould you like use to vote {} for the issue \n*"{}"*\nYour current balance is **12.65 PC** \nType: **!use** `[amount]` `[issue id]`'.format(reaction.emoji, issue_message))

    # await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))


# Background task


client.loop.create_task(update_blockchain())
client.run(TOKEN)
