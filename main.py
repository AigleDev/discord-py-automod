import discord
from discord.ext import commands
import time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
MAX_MESSAGE = 5

user_message_counts = {}

@bot.event
async def on_ready():
    print(f'Bot is working...')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if len(message.content) > 0 and message.content.count(message.content[0]) / len(message.content) >= 0.6:
        await message.delete()
        await message.channel.send(f'{message.author.mention}, kindly refrain from excessive emoji spam.')

    user_id = message.author.id
    current_time = time.time()

    if user_id in user_message_counts:
        messages_sent, last_message_time = user_message_counts[user_id]

        if current_time - last_message_time < 1:
            user_message_counts[user_id] = (messages_sent + 1, current_time)

            if messages_sent >= MAX_MESSAGE:
                await message.delete()
                await message.channel.send(f'{message.author.mention}, please avoid flooding the chat.')
        else:
            user_message_counts[user_id] = (1, current_time)
    else:
        user_message_counts[user_id] = (1, current_time)

    await bot.process_commands(message)

bot.run('TOKEN')
