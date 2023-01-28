import discord
import datetime
import random

from BotConfig import BotConfig

hi = {
    "triggers": ['hello', 'hi', 'hey', 'howdy'],
    "responses": ['Hello', 'Greetings!', 'Howdy', 'Hi!!', 'Hey', 'Helloooooo', 'sup', 'WASSSSUP', 'WAZZUP!', 'Yo!']
}

bye = {
    "triggers": ['bye', 'goodbye', 'bye bye', 'goodnight', 'gn', 'cya', 'see ya', 'adios', 'byee'],
    "responses": ['Bye!', 'Goodbye!', 'See ya!', 'Au revoir', 'k bye']
}

howareyou = {
    "triggers": ['how are you', 'how are you?', 'how r u', 'how are u', 'how r you', 'how r u?', 'how are u?', 'how r you?', 'whats up?', "what's up?", 'whats up', "what's up", "hru"],
    "responses": ['Good! How about you?', "I'm great! How about you?", 'Awesome! How about you?']
}

disagreement = {
    "triggers": ['fuck you bot', 'shut up bot', 'shutup bot', 'fuck u bot', 'fuk you bot', 'fuck u bot', 'fuck off bot', 'fuk off bot'],
    "responses": ['What did I do :(', 'Im sorry', 'screw you', 'fuck you', 'fuck off', 'ok fine', 'no u', ':(', '<@412316765918461955>']
}

triggerAndResponse = [hi, bye, howareyou, disagreement]

async def messageTriggers(client: discord.Client, message: discord.Message):
    if message.author == client.user or message.author.bot:
        pass
    else:
        dmlog = True
        for m in triggerAndResponse:
            if message.content.lower() in m["triggers"]:
                dmlog = False
                await message.channel.send(random.choice(m["responses"]))
        if message.guild == None:
            if dmlog == True:
                date = datetime.datetime.now()
                dms = client.get_channel(BotConfig.log_dms())
                embed = discord.Embed(title = 'DM Message', description = message.content, color = BotConfig.color())
                embed.set_author(name = message.author, icon_url = message.author.avatar_url)
                embed.add_field(name = 'Reply:', value = f'`!dm {message.author.id} `')
                embed.set_footer(text = f'{date:%B %d, %Y} at {date:%H:%M} EST', icon_url = BotConfig.footer())
                await dms.send(embed = embed)
        elif message.content == '69':
            await message.channel.typing()
            await message.channel.send('Nice')
            reactions = ['🇳','🇮', '🇨', '🇪']
            for reaction in reactions:
                await message.add_reaction(reaction)
        elif message.content == '100':
            await message.add_reaction('💯')
        elif message.content == '420':
            await message.channel.typing()
            await message.channel.send('Nice')
            reactions = ['🌿', '🇳','🇮', '🇨', '🇪', '😎']
            for reaction in reactions:
                await message.add_reaction(reaction)
        elif client.user.mentioned_in(message):
            list = []
            for letter in message.content:
                list.append(letter)
            if list[0] != BotConfig.prefix():
                await message.channel.typing()
                responses = ['You pinged?', 'Amogus?', 'no u', '**NO U**', '🔫', 'ping REEEEEEEEEEEEEEEEE', 'https://tenor.com/view/ping-who-pinged-me-disturbed-gif-14162073']
                await message.channel.send(random.choice(responses))