import discord
import random
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
# from discord.ext.commands import Bot

token = os.environ.get('bot_token')
Bot = commands.Bot(command_prefix="!")


@Bot.event
async def on_ready():
    print("Bot is online")
    print('We have logged in as {0.user}'.format(Bot))
    print("With the iD: {0.user.id}".format(Bot))


statuses = {
    'online': 'теперь в сети',
    'offline': 'вышел из сети'
}

@Bot.event
async def on_member_update(before, after):
    channel = Bot.get_channel(595267827548553256)
    if before.status == after.status:
        return
    if before.is_on_mobile() or after.is_on_mobile():
        return
    condition_after = (str(after.status) == "online" or str(after.status) == "offline")
    condition_before = (str(before.status) != "idle" and str(before.status) != "dnd")
    if condition_after and condition_before:
        await channel.send('{0} {1}'.format(after.mention, statuses[str(after.status)]))


@Bot.event
async def on_message(message):
    if message.content.startswith('Федор') and message.author.id != Bot.user.id:
        await message.channel.send("Федор свинтус")
    if message.content == "Nani?":
        await message.channel.send("omae wa mou shindeiru")
    await Bot.process_commands(message)


@Bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(Bot.latency * 1000)}ms')


@Bot.command()
async def about(ctx, member: discord.Member):
    await ctx.send('С нами с {0}, в данный момент: {1}\nСервер(?): {2}'
                   .format(member.joined_at.__format__('%d.%m.%y'), member.status, member.guild))


@Bot.command(name='clear')  # В чем смысл такого определения команды?
@has_permissions(administrator=True)
async def _clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@_clear.error
async def clear_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.send("{}, у тебя нет прав на это!".format(ctx.author.mention))  # Не работает


@Bot.command()
async def hello(ctx):
    await ctx.send('Wake up {0}...'.format(ctx.author.mention))
    my_file = discord.File("C:/Users/Сергей/Pictures/neo.png", filename="neo.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://neo.png")
    await ctx.send(file=my_file, embed=embed)


"""GAMES"""


@Bot.command(pass_context=True)  # Смысл pass_context?
async def coin(ctx):  # flip a coin
    choice = random.randint(1, 2)
    if choice == 1:
        await ctx.send('Орел <:kevin:596046050423341182>')
    if choice == 2:
        await ctx.send('Решка')


@Bot.command(aliases=['8ball'])  # Полезная штука
async def _8ball(ctx, *, question):
    responses = ['Бесспорно',
                 'Предрешено',
                 'Никаких сомнений',
                 'Определённо да',
                 'Можешь быть уверен в этом',
                 'Мне кажется — «да»',
                 'Вероятнее всего',
                 'Хорошие перспективы',
                 'Знаки говорят — «да»',
                 'Да',
                 'Пока не ясно, попробуй снова',
                 'Спроси позже',
                 'Лучше не рассказывать',
                 'Сейчас нельзя предсказать',
                 'Сконцентрируйся и спроси опять',
                 'Даже не думай',
                 'Мой ответ — «нет»',
                 'По моим данным — «нет»',
                 'Перспективы не очень хорошие',
                 'Весьма сомнительно']
    await ctx.send(f'Вопрос: {question}\nОтвет: {random.choice(responses)}')

Bot.run(token)
