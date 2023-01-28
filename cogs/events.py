import discord
import random
import datetime

from cogs._events.messageTriggers import messageTriggers
from discord.ext import tasks, commands
from cogs.mongo import mongo, db
from BotConfig import BotConfig

class events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.identification_check.start()
        self.identification_message.start()
        self.mute_checker.start()
        self.memberCount.start()

    def cog_unload(self):
        self.identification_check.cancel()
        self.identification_message.cancel()
        self.mute_checker.cancel()
        self.memberCount.cancel()

    mute = db["Mutes"]
    task = db["Tasks"]
    rr = db["RR"]

#on_message
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await messageTriggers(self.client, message)

#Discord Bot Connection
    @commands.Cog.listener()
    async def on_ready(self):
        date = datetime.datetime.now()
        print(f'{self.client.user.name} is connected at {date:%B %d, %Y} at {date:%H:%M} EST!')
        logs = self.client.get_channel(BotConfig.log_logs())
        general = self.client.get_channel(BotConfig.lcss_general())
        await general.typing()
        await logs.send(f'{self.client.user.name} is connected at {date:%B %d, %Y} at {date:%H:%M} EST!')
        responses = ['DEAD BODY!!!! <@498176822404579330> has been killed, the suspect is still on the loose!', 'I am Online!', 'zoo wee mama',
        'gooooooooooood morninnnnnnnnnnng ~~Vietnam~~ LCSS Discord', "<@536953999593701418> I didn't kill myself last night",
        'Who is ready to either get hugged or killed?', 'Traceback Error: Uhh- idk what is happening',
        "We're no strangers to love\nYou know the rules and so do I\nA full commitment's what I'm thinking of\nYou wouldn't get this from any other guy\nI just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nWe've known each other for so long\nYour heart's been aching but you're too shy to say it\nInside we both know what's been going on\nWe know the game and we're gonna play it\nAnd if you ask me how I'm feeling\nDon't tell me you're too blind to see\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give, never gonna give\n(Give you up)\nWe've known each other for so long\nYour heart's been aching but you're too shy to say it\nInside we both know what's been going on\nWe know the game and we're gonna play it\nI just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye"]
        await general.send(random.choice(responses))

#Member Joining
    @commands.Cog.listener() 
    async def on_member_join(self, member: discord.Member):
        guild = self.client.get_guild(BotConfig.lcss_id())
        welcome = self.client.get_channel(BotConfig.lcss_welcome())
        general = self.client.get_channel(BotConfig.lcss_general())
        identification = self.client.get_channel(BotConfig.lcss_identification())
        vc = self.client.get_channel(BotConfig.lcss_membercount())
        if member.guild == guild:
            value = mongo.get(self, self.task, "Lockdown", "value")
            if value == True:
                lockdown = discord.utils.get(guild.roles, name = 'Lockdown')
                await member.add_roles(lockdown)
            embed = discord.Embed(title = 'Welcome fellow Golden Ghost!', description = f'Please read {guild.rules_channel.mention} and enjoy your stay!\nAlso stop by {identification.mention} to get identified!', color = BotConfig.color())
            embed.set_author(name = f'{member.name}#{member.discriminator}', icon_url = BotConfig.footer())
            embed.set_thumbnail(url = member.display_avatar.url)
            await welcome.send(embed = embed)
            members = len([m for m in guild.members if not m.bot])
            await vc.edit(reason = 'New User', name = '👻 Member Count: ' + str(members))
            try:
                await member.send(f"Hello Golden Ghost, I am your friendly neighbourhood LCSS Bot! Welcome to the server and be sure to read {guild.rules_channel.mention}. Other than that enjoy your stay and I'll see you around!")
            except discord.HTTPException:
                await general.send(f"Hello {member.mention}! Since your DMs have been turned off, I'll do my little speech here. I am your friendly neighbourhood LCSS Bot! Welcome to the server and be sure to read {guild.rules_channel.mention}. Other than that enjoy your stay and I'll see you around!")

#Member Leaving
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild = self.client.get_guild(BotConfig.lcss_id())
        welcome = self.client.get_channel(BotConfig.lcss_welcome())
        vc = self.client.get_channel(BotConfig.lcss_membercount())
        if member.guild == guild:
            members = len([m for m in guild.members if not m.bot])
            await vc.edit(reason = 'User Left', name = '👻 Member Count: ' + str(members))
            embed = discord.Embed(title = 'Goodbye fellow Golden Ghost!', description = 'Sorry to see you go!', color = BotConfig.color())
            embed.set_author(name = f'{member.name}#{member.discriminator}', icon_url = BotConfig.footer())
            embed.set_thumbnail(url = member.display_avatar.url)
            await welcome.send(embed = embed)

#Identified Themself
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.client.get_guild(BotConfig.lcss_id())
        member = after
        roleIdentify = discord.utils.get(guild.roles, name = 'Please Identify Yourself!')
        listOfRoles: map[discord.Role] = map(lambda roleName: discord.utils.get(guild.roles, name = roleName), ['Alumni', 'Grade 12', 'Grade 11', 'Grade 10', 'Grade 9', 'Other Schools'])
        identifiedRoles = []
        for r in listOfRoles:
            identifiedRoles.append(r)
        for identifiedRole in identifiedRoles:
            try:
                if roleIdentify in before.roles and after.roles:
                    if identifiedRole not in before.roles and identifiedRole in after.roles:
                        await member.remove_roles(roleIdentify, reason = 'User Identified Themself')
            except AttributeError:
                pass
#Counting Failed GIF to DMs
        role = discord.utils.get(guild.roles, name = 'YOU HAVE FAILED #counting')
        if role not in before.roles and role in after.roles:
            await after.send(file = discord.File('youhavefailedthiscity.gif'))

#Check if users have identified
    @tasks.loop(minutes = 45)
    async def identification_check(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(BotConfig.lcss_id())
        roleIdentify = discord.utils.get(guild.roles, name = 'Please Identify Yourself!')
        listOfRoles: map[discord.Role] = map(lambda roleName: discord.utils.get(guild.roles, name = roleName), ['Alumni', 'Grade 12', 'Grade 11', 'Grade 10', 'Grade 9', 'Other Schools', 'Bot'])
        identifiedRoles = []
        for r in listOfRoles:
            identifiedRoles.append(r)
        for member in guild.members:
            identified = False
            for identifiedRole in identifiedRoles:
                if identifiedRole in member.roles:
                    identified = True
                    break
            if identified == False and ((discord.utils.utcnow() - member.joined_at) > datetime.timedelta(hours = 4)):
                await member.add_roles(roleIdentify)

#7 day check
    @tasks.loop(hours = 4)
    async def identification_message(self):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(BotConfig.lcss_identify())
        message_id = mongo.get(self, self.task, "ID_Message", "message")
        message = await channel.fetch_message(int(message_id))
        if (discord.utils.utcnow() - message.created_at) > datetime.timedelta(days = 7):
            msg = await channel.send("<@&775418642946064494> Please go to <#700563120690561024> to choose a grade role. This identification role will be removed after that, thank you :slight_smile:")
            mongo.update(self, self.task, "ID_Message", "message", value = msg.id)

#Mute Checking
    @tasks.loop(minutes = 5)
    async def mute_checker(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(BotConfig.lcss_id())
        logs = self.client.get_channel(BotConfig.lcss_logs())
        muted = discord.utils.get(guild.roles, name = 'Muted')
        date = datetime.datetime.now()
        for x in self.mute.find({}):
            member = await guild.fetch_member(int(x["_id"]))
            channel = self.client.get_channel(int(x["channel"]))
            if datetime.datetime.now() >= x["time"]:
                await member.remove_roles(muted)
                mongo.delete_id(self, self.mute, member.id)

                embed = discord.Embed(color = BotConfig.color())
                embed.set_author(name = member.name + '#' + member.discriminator + ' has been unmuted', icon_url = member.display_avatar.url)
                embed.set_footer(text = f'{date:%B %d, %Y} at {date:%H:%M} EST', icon_url = BotConfig.footer())

                embed_logs = discord.Embed(color = BotConfig.color())
                embed_logs.set_author(name = self.client.user.name, icon_url = self.client.user.display_avatar.url)
                embed_logs.add_field(name = 'Unmuted', value = member.mention, inline = True)
                embed_logs.set_footer(text = f'{date:%B %d, %Y} at {date:%H:%M} EST', icon_url = BotConfig.footer())

                await channel.send(embed = embed)
                await logs.send(embed = embed_logs)

#Member Count Update
    @tasks.loop(hours = 1)
    async def memberCount(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(BotConfig.lcss_id())
        vc = self.client.get_channel(BotConfig.lcss_membercount())
        members = len([m for m in guild.members if not m.bot])
        await vc.edit(reason = 'New User Joined', name = '👻 Member Count: ' + str(members))

#SHUT UP BOYUAN
    @commands.Cog.listener()
    async def on_typing(self, channel: discord.TextChannel, member: discord.Member, when):
        try:
            if channel.guild.id == BotConfig.lcss_id():
                if member.id == 412316765918461955:
                    await channel.send('SHUT THE UP BOYUAN, DONT EVEN FINISH TYPING', delete_after = 8.0)
        except AttributeError:
            pass

#Reaction Roles
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        for x in self.rr.find({}):
            message = x["_id"]
            emote = x["emote"]
            id = x["role"]
            r = member.guild.get_role(id)
            if int(reaction.message.id) == int(message) and str(reaction.emoji) == str(emote):
                await member.add_roles(r)

#You have failed counting
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == '❌' and user.id == 510016054391734273:
            await reaction.message.channel.send(reaction.message.author.mention)
            await reaction.message.channel.send(file = discord.File('youhavefailedthiscity.gif'))

#Rick Roll
    #@commands.Cog.listener()
    #async def on_voice_state_update(self, member, before, after):
        #guild = self.client.get_guild(BotConfig.lcss_id)
        #if member.guild == guild and not member.bot:
            #if not before.channel and after.channel:
                #vc = member.voice.channel
                #await vc.connect()
                #voice = discord.utils.get(self.client.voice_clients, guild = guild)
                #ytdl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192',}],}
                #ytdl = youtube_dl.YoutubeDL(ytdl_opts)
                #extract = ytdl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download = False)
                #content = discord.FFmpegOpusAudio(extract['formats'][0]['url'], executable = 'C:/ffmpeg/ffmpeg.exe', options = '-vn', before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
                #voice.play(content)
                #while voice.is_playing():
                    #await asyncio.sleep(230)
                #else:
                    #await voice.disconnect()
            #if before.channel and not after.channel:
                #voice = discord.utils.get(self.client.voice_clients, guild = guild)
                #if voice != None:
                    #voice = discord.utils.get(self.client.voice_clients, guild = guild)
                    #await voice.disconnect()

#Counting
    #@commands.Cog.listener()
    #async def on_member_update(self, before, after):
        #guild = self.client.get_guild(BotConfig.lcss_id)
        #counting = self.client.get_channel(BotConfig.lcss_counting)
        #if before.id == 510016054391734273:
            #if before.raw_status != 'offline' and after.raw_status == 'offline':
                #await counting.send('The Counting bot is offline. The channel will be locked for the time being.')
                #await counting.set_permissions(guild.default_role, send_message = False)

    #@commands.Cog.listener()
    #async def on_member_update(self, before, after):
        #guild = self.client.get_guild(BotConfig.lcss_id)
        #counting = self.client.get_channel(BotConfig.lcss_counting)
        #if before.id == 510016054391734273:
            #if before.raw_status == 'offline' and after.raw_status != 'offline':
                #await counting.send('The Counting bot is back online. The channel is now unlocked.')
                #await counting.set_permissions(guild.default_role, send_message = True)

async def setup(client):
    await client.add_cog(events(client))