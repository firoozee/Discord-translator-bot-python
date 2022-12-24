import discord
from discord.ext import commands
from datetime import datetime, date
import googletrans
import dotenv
import os

# Load .env variables
dotenv.load_dotenv()

###########################
# Globals
###########################
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
is_client_running = False


###########################
# Events
###########################

@bot.event
async def on_ready():
    global is_client_running

    if not is_client_running:
        is_client_running = True
        print(f"Bot initialising...")


@bot.event
async def on_message(message):
    # Avoid the bot replying to bots
    if message.author.bot:
        return

    # Reply hello to hello messages
    if message.content.lower().startswith('hello'):
        await message.channel.send(f"Hello {message.author.mention}")
        return

    if not message.content.startswith('!'):
        return

    # Process command
    async with message.channel.typing():
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    # Only show the raw error output to the discord user if it is not an internal exception
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("An error occured while processing the command, but don't worry, KAVEH team is currently looking into it. please report this if it hapens again.")
    else:
        await ctx.send(error)

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "command exception", type(error), error)
    raise error




###########################
# Commands
###########################

@bot.command(aliases=['tr'])
async def translate(ctx, lang_to, *args):
    """
    Translates the given text to the language `lang_to`.
    The language translated from is automatically detected.
    """

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)





###########################
# Run Client
###########################

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))