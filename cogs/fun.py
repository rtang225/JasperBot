import discord
import asyncio
import random
import datetime

from discord.ext import commands
from cogs.mongo import mongo, db
from BotConfig import BotConfig

class fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    rps = db["RPS"]
    rpsls = db["RPSLS"]
    stat = db["Stats"]
    
#Hug
    @commands.command()
    async def hug(self, ctx, *, member: commands.MemberConverter):
        await ctx.message.delete()
        if member == ctx.author:
            await ctx.send(f'{ctx.author.mention} has hugged themselves!?')
        elif member.id == 773215529082159135:
            await ctx.send(f'Thank You for the hug! :heart: <:pandahug:776186238213554187>')
            await asyncio.sleep(5)
            await ctx.send(f'Lemme give you a hug back {ctx.author.mention} :heart: <:pandahug:776186238213554187>')
        else:
            await ctx.send(f'{ctx.author.mention} has given {member.mention} a hug! :heart: <:pandahug:776186238213554187>')

    @hug.error
    async def hug_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} has given... wait a minute, who are you hugging? Please specify a user!')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{ctx.author.mention} has given a hug to the air! Now, I assume you want to specify a real user?')

#Boyuan
    @commands.command()
    async def boyuan(self, ctx):
        await ctx.message.delete()
        msg = await ctx.send('Go Fuck Yourself <@412316765918461955>')
        responses = ['Go Fuck Yourself Botanist', 'Go Fuck Yourself Cumstain', 'Go Fuck Yourself Boycash', 'Go Fuck Yourself Boyuan', 'Go Fuck Yourself Boylan', 'Go Fuck Yourself Buoyancy', 'Go Fuck Yourself Boyuan']
        for response in responses:
            await msg.edit(content = response)

#Bam
    @commands.command(aliases = ['bang'])
    @commands.cooldown(1, 3.0, commands.BucketType.user)
    async def bam(self, ctx, member: commands.MemberConverter):
        await ctx.message.delete()
        if member == ctx.author:
            await ctx.send(f'BANG!?! {ctx.author.mention} has thrown a ~~axe~~ boommerang at their head')
        elif member.id == 773215529082159135:
            await ctx.send(f'BANGG!!! {ctx.author.mention} has thrown an axe at... wait where is it?')
        else:
            await ctx.send(f'BANGG!!! {ctx.author.mention} has thrown an axe at {member.mention}')
            value = random.randint(1, 10)
            if value > 8:
                question = await ctx.send(f'AND IT HAS HIT THEM! They are down and critically injured\nWould you like to finish them? React quickly!')
                await question.add_reaction('✔️')
                await question.add_reaction('❌')
                try:
                    reaction, user = await ctx.bot.wait_for('reaction_add', check = lambda r, u: u == ctx.author and str(r.emoji) in ('✔️','❌'), timeout = 3)
                    if str(reaction.emoji) == '✔️':
                        await question.delete()
                        await ctx.send(f"You pull out another axe and uh yeah, let's just say their head isn't attached anymore")
                        #Kill
                        user = {"_id": ctx.author.id}
                        if (self.stat.count_documents(user) == 0):
                            self.stat.insert_one({"_id": ctx.author.id, "kills": 1, "deaths": 0, "revives": 0})
                        else:
                            mongo.increment(self, self.stat, ctx.author.id, "kills", 1)
                        #Death
                        user = {"_id": member.id}
                        if (self.stat.count_documents(user) == 0):
                            self.stat.insert_one({"_id": member.id, "kills": 0, "deaths": 1, "revives": 0})
                        else:
                            mongo.increment(self, self.stat, member.id, "deaths", 1)
                    elif str(reaction.emoji) == '❌':
                        await ctx.send(f"Ok nice guy, why'd you throw the axe at them in the first place? Now drag them to the hospital")
                except asyncio.TimeoutError:
                    await ctx.send(f"You're too slow! {member.mention} has pulled out their revolver and headshotted you!")
            else:
                await ctx.send(f"HAHA You suck, you missed and you can't aim. {member.mention} it's your turn to take a shot now. Use command `!bam @User`")

    @bam.error
    async def bam_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'BANG???{ctx.author.mention} has thrown a hammer at something or someone but clearly did not know how to aim. Please specify the user to hit')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'BANGG!!! {ctx.author.mention} has thrown an axe at a ghost. OW! Oh that went through me.\nCAN YOU PLEASE THROW IT AT A REAL USER PLEASE?')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'You are on cooldown! Try again in {error.retry_after:.2f}s', delete_after = 5.0)

#Kill
    @commands.command()
    @commands.cooldown(1, 3.0, commands.BucketType.user)
    async def kill(self, ctx, *, member: commands.MemberConverter):
        await ctx.message.delete()
        if member == ctx.author:
            await ctx.send(f'{member.mention} has been killed, after further investigation this has been listed as a suicide.')

            user = {"_id": ctx.author.id}
            if (self.stat.count_documents(user) == 0):
                self.stat.insert_one({"_id": ctx.author.id, "kills": 1, "deaths": 1, "revives": 0})
            else:
                mongo.increment(self, self.stat, ctx.author.id, "kills", 1)
                mongo.increment(self, self.stat, ctx.author.id, "deaths", 1)

        elif member.id == 773215529082159135:
            await ctx.send(f'{ctx.author.mention} has been killed, it seems as though they were killed by a turn table...')
            mongo.increment(self, self.stat, 773215529082159135, "kills", 1)

            user = {"_id": ctx.author.id}
            if (self.stat.count_documents(user) == 0):
                self.stat.insert_one({"_id": ctx.author.id, "kills": 0, "deaths": 1, "revives": 0})
            else:
                mongo.increment(self, self.stat, ctx.author.id, "deaths", 1)

        else:
            await ctx.send(f'DEAD BODY!!!! {member.mention} has been killed, the suspect is still on the loose!')

            user = {"_id": ctx.author.id}
            if (self.stat.count_documents(user) == 0):
                self.stat.insert_one({"_id": ctx.author.id, "kills": 1, "deaths": 0, "revives": 0})
            else:
                mongo.increment(self, self.stat, ctx.author.id, "kills", 1)

            user = {"_id": member.id}
            if (self.stat.count_documents(user) == 0):
                self.stat.insert_one({"_id": member.id, "kills": 0, "deaths": 1, "revives": 0})
            else:
                mongo.increment(self, self.stat, member.id, "deaths", 1)

    @kill.error
    async def kill_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} has been arrested for attempted murder. They were walking around stabbing the air with a knife. Probably on drugs.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{ctx.author.mention} has been arrested for being under illegal substances. They claimed that they were killing someone but they were just stabbing a tree.')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'You are on cooldown! Try again in {error.retry_after:.2f}s', delete_after = 5.0)

#Revive
    @commands.command()
    @commands.cooldown(1, 3.0, commands.BucketType.user)
    async def revive(self, ctx, *, member: commands.MemberConverter):
        await ctx.message.delete()
        if member == ctx.author:
            await ctx.send(f'{member.mention} has attempted to revive themself, they have clearly failed and is more dead than ever.')

            user = {"_id": ctx.author.id}
            if (self.stat.count_documents(user) == 0):
                self.stat.insert_one({"_id": member.id, "kills": 0, "deaths": 1, "revives": 0})
            else:
                mongo.increment(self, self.stat, member.id, "deaths", 1)

        else:
            await ctx.send(f'{member.mention} has been revived by {ctx.author.mention}!')

            user = {"_id": member.id}
            if (self.stat.count_documents(user) == 0):
                self.stat.insert_one({"_id": member.id, "kills": 0, "deaths": 0, "revives": 1})
            else:
                mongo.increment(self, self.stat, member.id, "revives", 1)

    @revive.error
    async def revive_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('What are you trying revive? The air?')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("I'm fairly sure you just summoned some random dead guy. Call Constantine for help")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'You are on cooldown! Try again in {error.retry_after:.2f}s', delete_after = 5.0)

#Life Stats
    @commands.command()
    async def stats(self, ctx, *, member: commands.MemberConverter = None):
        await ctx.message.delete()
        if member == None:
            member = ctx.author
        
        user = {"_id": member.id}
        if (self.stat.count_documents(user) == 0):
            kills = 0
            deaths = 0
            revives = 0
        else:
            kills = int(mongo.get(self, self.stat, member.id, "kills"))
            deaths = int(mongo.get(self, self.stat, member.id, "deaths"))
            revives = int(mongo.get(self, self.stat, member.id, "revives"))

        embed = discord.Embed(title = 'Life Stats', color = BotConfig.color())
        embed.set_author(name = member.name + '#' + member.discriminator, icon_url = member.display_avatar.url)
        embed.add_field(name = 'Kills:', value = kills)
        embed.add_field(name = 'Deaths:', value = deaths)
        embed.add_field(name = 'Revives:', value = revives)
        if deaths == 0:
            embed.add_field(name = 'Kills per Death (K/D):', value = '∞')
        else:
            embed.add_field(name = 'Kills per Death (K/D):', value = round(kills/deaths, 2))
        if revives - deaths > 0:
            embed.add_field(name = 'Alive?', value = 'Yes')
        elif revives - deaths < 0:
            embed.add_field(name = 'Alive?', value = 'No')
        elif revives - deaths == 0:
            embed.add_field(name = 'Alive?', value = 'Just Barely')
        await ctx.send(embed = embed)        

#Fuck yourself
    @commands.command(aliases = ['fuckoff', 'gfys'])
    async def fys(self, ctx, *, member: commands.MemberConverter):
        await ctx.message.delete()
        if member.id == 773215529082159135 or member.id == 524001661379936268:
            await ctx.send(f'No you go fuck yourself {ctx.author.mention}')
        else:
            await ctx.send(f'{ctx.author.mention} has told {member.mention} to fuck themselves')

    @fys.error
    async def fys_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention} Please state who you want to fuck.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'{ctx.author.mention} Look, they DONT EVEN EXIST. Mention a real user **please**')

#Fake Ban
    @commands.command()
    async def bann(self, ctx, member: commands.MemberConverter, *, reason = None):
        await ctx.message.delete()
        date = datetime.datetime.now()
        embed = discord.Embed(color = BotConfig.color())
        embed.set_author(name = member.name + '#' + member.discriminator + ' has been bannned', icon_url = member.display_avatar.url)
        embed.add_field(name = 'For reason:', value = reason, inline = True)
        embed.set_footer(text = f'{date:%B %d, %Y} at {date:%H:%M} EST', icon_url = BotConfig.footer())
        await ctx.send(embed = embed)

    @bann.error
    async def bann_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('I SHALL BAN- uh, who? Please state the user to be bannned')
        elif isinstance(error, commands.MemberNotFound):
            date = datetime.datetime.now()
            embed = discord.Embed(color = BotConfig.color())
            embed.set_author(name = 'A ghost user has been bannned', icon_url = 'https://media.discordapp.net/attachments/818494514867077144/844997139280822332/image0.jpg')
            embed.add_field(name = 'For reason:', value = f"{ctx.author.mention} has no idea what they're doing", inline = True)
            embed.set_footer(text = f'{date:%B %d, %Y} at {date:%H:%M} EST', icon_url = BotConfig.footer())
            await ctx.send(embed = embed)

#Rock Paper Scissors
    @commands.command(aliases = ['rps'])
    async def rockpaperscissors(self, ctx):
        await ctx.message.delete()
        userresponses = ['rock', 'paper', 'scissors', 'r', 'p', 's']
        botresponses = ['Rock', 'Paper', 'Scissors']
        r = ['rock', 'r']
        p = ['paper', 'p']
        s = ['scissors', 's']
        descriptions = ['Type in your repsonse when I say shoot. (R, P, S)', 'Rock 🪨', 'Paper 📰', 'Scissors ✂️', '🌠 **SHOOT!** 🌠']
        
        #Error catching responses
        result = 'An unknown error has occurred'
        bot = 'You have typed an invalid option! You lost.'
        
        #Check to ensure person has played before and opens new profile if not
        data = {"_id": ctx.author.id}
        if (self.rps.count_documents(data) == 0):
            self.rps.insert_one({"_id": ctx.author.id, "wins": 0, "ties": 0, "loses": 0})
        
        #Sends the embeds
        for x in descriptions:
            default = discord.Embed(title = 'Rock Paper Scissors', description = x, color = BotConfig.color())
            default.set_footer(text = 'Type cancel after Shoot to exit.')
            if x == descriptions[0]:
                msg = await ctx.send(embed = default)
                await asyncio.sleep(3)
            else:
                await msg.edit(embed = default)
                await asyncio.sleep(1)
        
        #Obtains message from the user
        try:
            user = await ctx.bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 15)
        except asyncio.TimeoutError:
            await ctx.send(f'Timed Out')
            return
        
        #Decides which reply to send through
        def reply(x, y) -> str:
            if x < y:
                mongo.increment(self, self.rps, ctx.author.id, "wins", 1)
                return 'You won!'
            elif x > y:
                mongo.increment(self, self.rps, ctx.author.id, "loses", 1)
                return 'You lost.'
            else:
                mongo.increment(self, self.rps, ctx.author.id, "ties", 1)
                return "It's a draw!"

        if user.content.lower() == 'cancel':
            await ctx.send('Cancelled.')
            return
        
        #Interprets the response and bot response
        if user.content.lower() in userresponses:
            bot = random.choice(botresponses)
            magic = [p, r, s, p, r]
            for x in range (1, 4):
                if user.content.lower() in magic[x]:
                    for y in range(x-1, x+2):
                        if bot.lower() in magic[y]:
                            result = reply(x, y)
                            break
                    break
        else:
            result = reply(1, 0)
        
        #Sends out response to user
        await ctx.send(bot)
        wins = int(mongo.get(self, self.rps, ctx.author.id, "wins"))
        ties = int(mongo.get(self, self.rps, ctx.author.id, "ties"))
        loses = int(mongo.get(self, self.rps, ctx.author.id, "loses"))
        record = discord.Embed(title = result, description = f'Your record in RPS is {wins} - {ties} - {loses}', color = BotConfig.color())
        await ctx.send(embed = record)

#Rock Paper Scissors Lizard Spock
    @commands.command(aliases = ['rpsls'])
    async def rps5(self, ctx):
        await ctx.message.delete()
        userresponses = ['rock', 'paper', 'scissors', 'lizard', 'spock', 'r', 'p', 'sc', 'l', 'sp']
        botresponses = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
        r = ['rock', 'r']
        p = ['paper', 'p']
        sc = ['scissors', 'sc']
        l = ['lizard', 'l']
        sp = ['spock', 'sp']
        descriptions = ['Type in your repsonse when I say shoot. (R, P, Sc, L, Sp)', 'Rock 🪨', 'Paper 📰', 'Scissors ✂️', 'Lizard 🦎', 'Spock 🖖', '🌠 **SHOOT!** 🌠']

        #Error catching responses
        result = 'An unknown error has occurred'
        bot = 'You have typed an invalid option! You lost.'

        #Check to ensure person has played before and opens new profile if not
        data = {"_id": ctx.author.id}
        if (self.rpsls.count_documents(data) == 0):
            self.rpsls.insert_one({"_id": ctx.author.id, "wins": 0, "ties": 0, "loses": 0})

        #Sends the Embed
        for x in descriptions:
            default = discord.Embed(title = 'Rock Paper Scissors Lizard Spock', description = x, color = BotConfig.color())
            default.set_footer(text = 'If you have no idea what this is, use command !rpslsinfo. Type cancel after Shoot to exit.')
            if x == descriptions[0]:
                msg = await ctx.send(embed = default)
                await asyncio.sleep(4)
            else:
                await msg.edit(embed = default)
                await asyncio.sleep(0.75)

        #Obtains message from the user
        try:
            user = await ctx.bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 15)
        except asyncio.TimeoutError:
            await ctx.send(f'Timed Out')
            return
        
        #Decides which reply to send through
        def reply(x, y) -> str:
            if x < y:
                mongo.increment(self, self.rpsls, ctx.author.id, "wins", 1)
                return 'You won!'
            elif x > y:
                mongo.increment(self, self.rpsls, ctx.author.id, "loses", 1)
                return 'You lost.'
            else:
                mongo.increment(self, self.rpsls, ctx.author.id, "ties", 1)
                return "It's a draw!"

        if user.content.lower() == 'cancel':
            await ctx.send('Cancelled.')
            return

        #Interprets the response and bot response
        if user.content.lower() in userresponses:
            bot = random.choice(botresponses)
            magic = [l, p, sp, r, sc, l, p, sp, r]
            for x in range (2, 7):
                if user.content.lower() in magic[x]:
                    for y in range(x-2, x+3):
                        if bot.lower() in magic[y]:
                            result = reply(x, y)
                            break
                    break
        else:
            result = reply(1, 0)

        #Sends out response to user
        await ctx.send(bot)
        wins = int(mongo.get(self, self.rpsls, ctx.author.id, "wins"))
        ties = int(mongo.get(self, self.rpsls, ctx.author.id, "ties"))
        loses = int(mongo.get(self, self.rpsls, ctx.author.id, "loses"))
        record = discord.Embed(title = result, description = f'Your record in RPSLS is {wins} - {ties} - {loses}', color = BotConfig.color())
        await ctx.send(embed = record)

#RPSLS Info
    @commands.command()
    async def rpslsinfo(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title = 'Info about RPSLS', color = BotConfig.color())
        embed.set_image(url = 'https://cdn.discordapp.com/attachments/818494514867077144/853816412714958858/image0.png')
        await ctx.send(embed = embed)

#RPSStats
    @commands.command(aliases = ['rpsstats'])
    async def rockpaperscissorsstats(self, ctx, *, member: commands.MemberConverter = None):
        await ctx.message.delete()
        if member == None:
            member = ctx.author
        user = {"_id": member.id}
        if (self.rps.count_documents(user) == 0):
            wins1 = 0
            ties1 = 0
            loses1 = 0
            value1 = 'No Stats'
            winrate1 = '-'
        else:
            wins1 = int(mongo.get(self, self.rps, member.id, "wins"))
            ties1 = int(mongo.get(self, self.rps, member.id, "ties"))
            loses1 = int(mongo.get(self, self.rps, member.id, "loses"))
            winrate1 = round(wins1/(wins1+ties1+loses1)*100)
            value1 = f'{wins1} wins, {ties1} ties, {loses1} loses'

        if (self.rpsls.count_documents(user) == 0):
            wins2 = 0
            ties2 = 0
            loses2 = 0
            value2 = 'No Stats'
            winrate2 = '-'
        else:
            wins2 = int(mongo.get(self, self.rpsls, member.id, "wins"))
            ties2 = int(mongo.get(self, self.rpsls, member.id, "ties"))
            loses2 = int(mongo.get(self, self.rpsls, member.id, "loses"))
            winrate2 = round(wins2/(wins2+ties2+loses2)*100)
            value2 = f'{wins2} wins, {ties2} ties, {loses2} loses'

        if (wins1 + wins2 + ties1 + ties2 + loses1 + loses2) == 0:
            totalwinrate = '0%'
        else:
            totalwinrate = f'{round((wins1 + wins2)/(wins1 + wins2 + ties1 + ties2 + loses1 + loses2)*100)}%'

        embed = discord.Embed(title = 'All RPS Stats', color = BotConfig.color())
        embed.set_author(name = member.name + '#' + member.discriminator, icon_url = member.display_avatar.url)
        embed.add_field(name = '__Total Stats:__', value = f'{wins1 + wins2} wins, {ties1 + ties2} ties, {loses1 + loses2} loses')
        embed.add_field(name = '__Total Winrate:__', value = totalwinrate)
        embed.add_field(name = '\u200b', value = '\u200b')
        embed.add_field(name = 'RPS Stats:', value = value1)
        embed.add_field(name = 'RPS Winrate:', value = f'{winrate1}%')
        embed.add_field(name = '\u200b', value = '\u200b')
        embed.add_field(name = 'RPSLS Stats:', value = value2)
        embed.add_field(name = 'RPS Winrate:', value = f'{winrate2}%')
        embed.add_field(name = '\u200b', value = '\u200b')
        await ctx.send(embed = embed)

    @rockpaperscissorsstats.error
    async def rockpaperscissorsstats_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please use this format: `!rpsstats @User`', delete_after = 5.0)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('Please ping a valid user', delete_after = 5.0)

#8 Ball
    @commands.command(aliases = ['8ball'])
    async def eightball(self, ctx, *, question):
        await ctx.message.delete()
        responses = ['It is Certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
        'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', "Don't count on it.", 'My reply is no.', 'My sources say no.',
        'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(title = '🎱 8 Ball!', description = f'Question: **__{question}__**\nBy: {ctx.author.mention}' , color = BotConfig.color())
        embed.add_field(name = 'Response:', value = random.choice(responses))
        await ctx.send(embed = embed)

    @eightball.error
    async def eightball_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please use this format: `!8ball (Question)`', delete_after = 5.0)

#High 5
    @commands.command(aliases = ['high5', 'hf', 'h5'])
    async def highfive(self, ctx, *, member: commands.MemberConverter):
        await ctx.message.delete()
        if member == ctx.author:
            await ctx.send("Ok, I get that you're lonely but you can't give yourself a highfive")
        else:
            await ctx.send(f'{ctx.author.mention} has given {member.mention} a highfive. 🖐️')
            value = random.randint(1, 1000)
            if value in range(500, 505):
                await ctx.send(f'{member.mention} you also have COVID now')

    @highfive.error
    async def highfive_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please use this format: `!highfive @User`', delete_after = 5.0)

#Panini
    @commands.command(aliases = ['pani'])
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    async def panini(self, ctx):
        await ctx.message.delete()
        await ctx.send('<@536953999593701418>', delete_after = 0.1)
        await ctx.send('https://media.discordapp.net/attachments/785336906589667391/1034194132983369780/petthepanini.gif')
    
    @panini.error
    async def panini_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()

#Andrew
    @commands.command(aliases = ['andy'])
    @commands.cooldown(1, 2.0, commands.BucketType.user)
    async def andrew(self, ctx):
        await ctx.message.delete()
        await ctx.send('<@947329370903679036>')
        if ctx.author.id == 536953999593701418:
            await ctx.send('<:pandano:1056365728317575318>')
        else:
            await ctx.send('<:noO:789642384550920202>')

    @andrew.error
    async def andrew_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
        
async def setup(client):
    await client.add_cog(fun(client))
