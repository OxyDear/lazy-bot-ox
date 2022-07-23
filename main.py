import io
import discord
import config
from discord import utils
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
import database
from PIL import Image, ImageFont, ImageDraw
from datetime import timedelta, datetime
from youtube_dl import YoutubeDL
import requests

intents = discord.Intents.all()
intents.members = True
intents.presences = True
status = 'Pycharm'
prefix = '.'
music_list = ['https://www.youtube.com/watch?v=8nXqcugV2Y4&t=4s', 'https://www.youtube.com/watch?v=jfKfPfyJRdk', 'https://www.youtube.com/watch?v=rUxyKA_-grg']
bots = [959147697586180167, 159985870458322944, 172002275412279296, 228537642583588864, 995784855365365831, 962656998049079366]
client_com = commands.Bot(command_prefix=prefix)
# database.cur.execute('''DROP TABLE poopsiki''')

with open('BadWords.txt', 'r') as file:
    words = file.read()
    bad_words = words.split()


class MyClient(commands.Bot, discord.Client, commands.Cog):
    def __init__(self, command_prefix, self_bot, intents):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=intents)
        commands.Cog.__init__(self)
        self.add_commands()

    @client_com.event
    async def on_ready(self):
        DiscordComponents(client_com)
        print('Logged on as {0}'.format(self.user))

        await discord.Client.change_presence(self, status=discord.Status.do_not_disturb, activity=discord.Game(status))

    @client_com.event
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in config.POST_ID:
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = utils.find(lambda i: i.id == payload.user_id, message.guild.members)
            print(member)

            try:
                emoji = str(payload.emoji)
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])

                # i f guild.id == 964585613066133644:
                #     await payload.member.add_roles(role)
                # if len([j for j in member.roles if j.id not in config.EX_ROLES]) <= config.MAX_ROLES_PER_USER:
                for j in member.roles:
                    j = str(j)

                    if j == 'Python':
                        config.ADVANCED['Java'] = False
                    if j == 'Java':
                        config.ADVANCED['Python'] = False
                    if j == 'Wanderer':
                        config.ADVANCED['Guest'] = False
                        config.ADVANCED['Uncertain'] = False
                    if j == 'Guest':
                        config.ADVANCED['Wanderer'] = False
                        config.ADVANCED['Uncertain'] = False
                    if j == 'Uncertain':
                        config.ADVANCED['Wanderer'] = False
                        config.ADVANCED['Guest'] = False
                    if j == 'Boy':
                        config.ADVANCED['Girl'] = False
                    if j == 'Girl':
                        config.ADVANCED['Boy'] = False

                if config.ADVANCED[str(role)]:
                    await payload.member.add_roles(role)
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('ERROR {0.display_name}'.format(member))
                print('SUCCESS {0.display_name} granted {1.name}'.format(payload.member, payload.role))
            # else:
            #     await message.remove_reaction(payload.emoji, member)
            #     print('ERROR {0.display_name}'.format(member))

            except KeyError:
                print('NOT FOUND ' + emoji)
            except Exception as e:
                print(repr(e))

    @client_com.event
    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.find(lambda i: i.id == payload.user_id, message.guild.members)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])
            role_str = str(role)

            if role_str == 'Python':
                config.ADVANCED['Java'] = True
            if role_str == 'Java':
                config.ADVANCED['Python'] = True
            if role_str == 'Wanderer':
                config.ADVANCED['Guest'] = True
                config.ADVANCED['Uncertain'] = True
            if role_str == 'Guest':
                config.ADVANCED['Wanderer'] = True
                config.ADVANCED['Uncertain'] = True
            if role_str == 'Uncertain':
                config.ADVANCED['Wanderer'] = True
                config.ADVANCED['Guest'] = True
            if role_str == 'Boy':
                config.ADVANCED['Girl'] = True
            if role_str == 'Girl':
                config.ADVANCED['Boy'] = True

            await member.remove_roles(role)
            print('SUCCESS {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError:
            print('NOT FOUND ' + emoji)
        except Exception as e:
            print(repr(e))

    @client_com.event
    async def on_member_join(self, member):
        role = utils.get(member.guild.roles, id=999291982759338044)
        # roleAdmin = utils.get(member.guild.roles, id=796025109634613318)
        #
        # if member.id == 764860374893461504:
        #     await member.add_roles(roleAdmin)

        if member.id not in bots:
            database.cur.execute(f'''
                                INSERT INTO poopsiki VALUES('{str(member).split('#')[0]}', 1, {datetime.now()})
                                ''')
            await member.send(f'Your game in raccoons started, {member.mention} barn now has 1 poops')
            database.bd.commit()

        await member.add_roles(role)
        await member.send(embed=discord.Embed(title=f'Welcome {member.mention}',
                                              description=f'Go to channel verification to verify your account. \n Send .helpme to a global chat for knew all info'))

    @client_com.event
    async def on_member_leave(self, member):

        if member.id not in bots:
            database.cur.execute(f'''DELETE FROM poopsiki WHERE raccoon == '{str(member).split('#')[0]}' ''')
            database.bd.commit()

    @client_com.event
    async def on_message(self, message):
        await self.process_commands(message)

        msg = message.content.lower()

        for word in bad_words:
            if word in msg:
                await message.delete()
                await message.author.send(f'{message.author.name} not need to write like that')

    def add_commands(self):

        @self.command(name='clear', pass_context=True, aliases=['cl'])
        @commands.has_permissions(administrator=True)
        async def clear(ctx, amount=1000000):
            await ctx.channel.purge(limit=amount)

        @self.command(name='hello', pass_context=True)
        async def hello(ctx, member):
            await ctx.channel.purge(limit=1)

            await ctx.send(f'Hello {member.mention}')

        @self.command(name='kick', pass_context=True)
        @commands.has_permissions(administrator=True)
        async def kick(ctx, member: discord.Member, reason=None):
            emb = discord.Embed(title='Kick', colour=discord.Color.red())
            await ctx.channel.purge(limit=1)

            await member.kick(reason=reason)
            emb.set_author(name=member.name, icon_url=member.avatar_url)
            emb.add_field(name='Kick user', value='Kicked user : {}'.format(member.mention))
            emb.set_footer(text='Was kicked by {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)

            await ctx.send(embed=emb)

        @self.command(name='ban', pass_context=True)
        @commands.has_permissions(administrator=True)
        async def ban(ctx, member: discord.Member, reason=None):
            emb = discord.Embed(title='Ban', colour=discord.Color.red())
            await ctx.channel.purge(limit=1)

            await member.ban(reason=reason)
            emb.set_author(name=member.name, icon_url=member.avatar_url)
            emb.add_field(name='Ban user', value='Banned user : {}'.format(member.mention))
            emb.set_footer(text='Was banned by {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)

            await ctx.send(embed=emb)

        @self.command(name='unban', pass_context=True)
        @commands.has_permissions(administrator=True)
        async def unban(ctx):
            await ctx.channel.purge(limit=1)

            banned_users = await ctx.guild.bans()

            for e in banned_users:
                user = e.user

                await ctx.guild.unban(user)
                await ctx.send(f'Member was unbanned {user.mention}')

                return

        @self.command(name='help_me', pass_context=True, aliases=['helpme'])
        async def help_me(ctx):

            await ctx.channel.purge(limit=1)
            emb = discord.Embed(title='Navigation', colour=discord.Color.blue())

            emb.add_field(name='{}clear'.format(prefix), value='Chat cleanup')
            emb.add_field(name='{}kick'.format(prefix), value='Kick member')
            emb.add_field(name='{}ban'.format(prefix), value='Ban member')
            emb.add_field(name='{}time'.format(prefix), value='Find out the time')
            emb.add_field(name='{}mute'.format(prefix), value='Mute member')
            emb.add_field(name='{}send'.format(prefix), value='Send message to member')
            emb.add_field(name='{}calc'.format(prefix), value='Calculator')
            emb.add_field(name='{}join'.format(prefix), value='Join chat')
            emb.add_field(name='{}leave'.format(prefix), value='Leave chat')
            emb.add_field(name='{}add <url_utube>'.format(prefix), value='Add in follow list url')
            emb.add_field(name='{}fol <number>'.format(prefix), value='Play song number')
            emb.add_field(name='{}rac'.format(prefix), value='Play in game "RACCOON"')
            emb.add_field(name='{}list'.format(prefix), value='Show all favorite songs')
            emb.add_field(name='{}card'.format(prefix), value='Show own card of member')

            await ctx.send(embed=emb)

        @self.command(name='time', pass_context=True)
        async def time(ctx):
            emb = discord.Embed(title='TIME', description='Тут должен быть текст', colour=discord.Color.green(),
                                url='https://www.timeserver.ru/', )

            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            emb.set_footer(text='Попуск, который написал это', icon_url=ctx.author.avatar_url)
            emb.set_image(
                url='https://transcode-v2.app.engoo.com/image/fetch/f_auto,c_lfill,w_300,dpr_3/https://assets.app.engoo.com/images/CGPkj72Wn3gPmu9ebqmpS1nGQNOZQlR70NilqMAWUBm.png')
            emb.set_thumbnail(
                url='https://transcode-v2.app.engoo.com/image/fetch/f_auto,c_lfill,w_300,dpr_3/https://assets.app.engoo.com/images/CGPkj72Wn3gPmu9ebqmpS1nGQNOZQlR70NilqMAWUBm.png')

            now = datetime.now().replace(microsecond=0)

            emb.add_field(name='Time', value='Time : {}'.format(now))

            await ctx.author.send(embed=emb)

        @self.command(name='mute')
        @commands.has_permissions(administrator=True)
        async def mute(ctx, member: discord.Member):
            await ctx.channel.purge(limit=1)

            mute_role = utils.get(ctx.message.guild.roles, name='mute')
            await member.add_roles(mute_role)
            await ctx.send(f'{member.mention} was muted')

        @self.command(name='send')
        async def send(ctx, member: discord.Member):
            await member.send('Что робишь? P.s. By {}'.format(ctx.author.name))

        @self.command(name='calc')
        async def calc(ctx, a: int, arg, b: int):
            if arg == '+':
                await ctx.send(f'{a + b}')
            elif arg == '*':
                await ctx.send(f'{a * b}')
            elif arg == '-':
                await ctx.send(f'{a - b}')
            elif arg == '/':
                if a / b == int(a / b):
                    await ctx.send(f'{int(a / b)}')
                else:
                    await ctx.send(f'{a / b}')

        @self.command(name='join')
        async def join(ctx):
            # global voice
            # channel = ctx.message.author.voice.channel
            # voice = get(client_com.voice_clients, guild=ctx.guild)
            #
            # if voice and voice.is_connected():
            #     await voice.move_to(channel)
            # else:
            #     voice = await channel.connect()
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f'Bot joined the channel: {channel}')

        @self.command(name='leave')
        async def leave(ctx):
            channel = ctx.message.author.voice.channel
            # voice = get(client_com.voice_clients, guild=ctx.guild)
            #
            # if voice and voice.is_connected():
            #     await voice.disconnect()
            # else:
            #     voice = await channel.connect()
            await ctx.voice_client.disconnect()
            await ctx.send(f'Bot leaved the channel: {channel}')

        # @self.command(name='play')
        # async def play(ctx, *, url: str):
        #
        #     await ctx.channel.purge(limit=1)
        #
        #     ydl_op = {
        #         'format': 'worstaudio/best',
        #         'noplaylist': 'False',
        #         'simulate': 'False',
        #         'key': 'FFmpegExtractAudio',
        #         'preferredcodec': 'mp3',
        #         'preferredquality': '192',
        #     }
        #     FFmpeg_op = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        #                  'options': '-vn'}
        #
        #     voice = await ctx.message.author.voice.channel.connect()
        #
        #     with YoutubeDL(ydl_op) as ydl:
        #         if 'https://' in url:
        #             info = ydl.extract_info(url, download=False)
        #         else:
        #             info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
        #
        #     url = info['formats'][0]['url']
        #
        #     voice.play(discord.FFmpegPCMAudio(executable=r"C:\ffmpeg\bin\ffmpeg.exe", source=url, **FFmpeg_op))
        #     voice.source = discord.PCMVolumeTransformer(voice.source)
        #     voice.source.volume = 0.28
        #
        #     @self.command(aliases=['vol'])
        #     async def volume(ctx, amount: float):
        #         await ctx.channel.purge(limit=1)
        #
        #         voice.source.volume = amount
        #         await ctx.send('Volume: {}'.format(voice.source.volume))
        #
        #     @volume.error
        #     async def vol_error(ctx, error):
        #         if isinstance(error, commands.BadArgument):
        #             await ctx.send('Enter the argument as a number')

        @self.command(name='follow', aliases=['fol'])
        async def follow(ctx, num: int):

            await ctx.channel.purge(limit=1)

            ydl_opt = {
                'format': 'worstaudio/best',
                'noplaylist': 'False',
                'simulate': 'False',
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
            FFmpeg_opt = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

            voice = await ctx.message.author.voice.channel.connect()
            print(music_list)

            print('OK')
            url = music_list[int(num) - 1]

            print(url)

            with YoutubeDL(ydl_opt) as ydl:
                if 'https://' in url:
                    info = ydl.extract_info(url, download=False)
                else:
                    info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]

            url = info['formats'][0]['url']

            voice.play(discord.FFmpegPCMAudio(executable=r"C:\ffmpeg\bin\ffmpeg.exe", source=url, **FFmpeg_opt))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.28

            @self.command(aliases=['vol'])
            async def volume(ctx, amount: float):
                await ctx.channel.purge(limit=1)

                voice.source.volume = amount
                await ctx.send('Volume: {}'.format(voice.source.volume))

            @volume.error
            async def vol_error(ctx, error):
                if isinstance(error, commands.BadArgument):
                    await ctx.send('Enter the argument as a number')

        @self.command(aliases=['add'])
        async def add_list_of_music(ctx, url_music: str):
            await ctx.channel.purge(limit=1)

            music_list.append(url_music)
            await ctx.send('Your music added in favorites')

            return music_list

        @self.command(aliases=['list'])
        async def list_of_music(ctx):
            await ctx.channel.purge(limit=1)

            await ctx.send(f'{music_list}')

        @self.command(name='card', aliases=['i'])
        async def card(ctx):
            await ctx.channel.purge(limit=1)

            img = Image.new('RGBA', (400, 200), '#232529')
            url = str(ctx.author.avatar_url)[:-10]

            response = requests.get(url, stream=True)
            response = Image.open(io.BytesIO(response.content))
            response = response.convert('RGBA')
            response = response.resize((100, 100), Image.ANTIALIAS)

            img.paste(response, (15, 15, 115, 115))

            idraw = ImageDraw.Draw(img)
            name = ctx.author.name
            tag = ctx.author.discriminator
            active = ctx.author.activity

            headline = ImageFont.truetype('arial.ttf', size=30)
            undertext = ImageFont.truetype('arial.ttf', size=20)

            idraw.text((145, 20), f'{name}#{tag}', font=headline)
            idraw.text((145, 60), f'ID: {ctx.author.id}', font=undertext)
            idraw.text((145, 85), f'{active}', font=undertext)

            img.save('user_card.png')

            await ctx.send(file=discord.File(fp='user_card.png'))

        @self.command(name='test')
        async def test(ctx):
            await ctx.send(embed=discord.Embed(title='Invite to party'), components=[
                Button(style=ButtonStyle.green, label='Accept'),
                Button(style=ButtonStyle.red, label='Decline'),
                Button(style=ButtonStyle.URL, label='Youtube', url='https://www.youtube.com/'),
            ]
                           )

            print('OK')
            response = await client_com.wait_for('button_click')
            print(response)
            if response.channel == ctx.channel:
                print('OK')
                if response.component.label == 'Accept':
                    print('OK')
                    await response.respond(content='Great!')
                else:
                    await response.respond(embed=discord.Embed(title='Are you sure?'),
                                           components=[
                                               Button(style=ButtonStyle.green, label='YES'),
                                               Button(style=ButtonStyle.red, label='NO'),
                                               Button(style=ButtonStyle.blue, label="I'll think..."),
                                           ])

        @self.command(name='raccoon', aliases=['rac', 'poops', 'poop'])
        async def raccoon(ctx):
            global date

            await ctx.channel.purge(limit=1)

            database.cur.execute('''
                                CREATE TABLE if not exists poopsiki
                                (raccoon text, poops integer, time text)
                                ''')

            print(list(database.cur.execute('''SELECT * FROM poopsiki''')))

            for i in list(database.cur.execute('''SELECT * FROM poopsiki''')):
                print(str(ctx.message.author).split('#')[0], i[0])
                if list(database.cur.execute('''SELECT * FROM poopsiki'''))[-1] == i:
                    if str(ctx.message.author).split('#')[0] in i:
                        print(str(i[2]).split())
                        years_with = str(i[2]).split()[0]
                        days_with = str(i[2]).split()[1]
                        years = int(years_with.split('-')[0])
                        months = int(years_with.split('-')[1])
                        days = int(years_with.split('-')[2])
                        hours = int(days_with.split(':')[0])
                        minutes = int(days_with.split(':')[1])
                        seconds = int(float(days_with.split(':')[2]))
                        time_date = datetime(year=years, month=months, day=days, hour=hours, minute=minutes, second=seconds)

                        delta = datetime.now() - time_date
                        if delta > timedelta(hours=6):
                            print('OK TIME')
                            poops = int(i[1])
                            print(str(ctx.message.author).split('#')[0], poops)
                            poops += 1
                            date = datetime.now()
                            database.cur.execute(f'''
                                                UPDATE poopsiki SET poops = {poops}, time = '{date}' WHERE raccoon = '{str(ctx.message.author).split('#')[0]}'
                                                ''')
                            database.bd.commit()

                            if poops == 1:
                                await ctx.send(f'{ctx.message.author.mention} pit now has {poops} poop')
                            else:
                                await ctx.send(f'{ctx.message.author.mention} pit now has {poops} poops')

                            return
                        else:
                            timeYet = str(timedelta(hours=6) - delta)
                            micro_without = timeYet.split('.')[0]
                            await ctx.send(f"Time has not yet passed: {micro_without}, you have {int(list(database.cur.execute(f'''SELECT poops FROM poopsiki WHERE raccoon = '{str(ctx.message.author).split('#')[0]}' '''))[0][0])} poops")
                            return

                    else:
                        print('INSERT')
                        date = datetime.now()
                        database.cur.execute(f'''
                                            INSERT INTO poopsiki VALUES('{str(ctx.message.author).split('#')[0]}', 1, '{date}')
                                            ''')
                    database.bd.commit()

                    await ctx.send(f'{ctx.message.author.mention} pit now has 1 poop')
                    return

                elif str(ctx.message.author).split('#')[0] != i[0]:
                    continue

                elif str(ctx.message.author).split('#')[0] == i[0]:
                    print(str(i[2]).split())
                    years_with = str(i[2]).split()[0]
                    days_with = str(i[2]).split()[1]
                    years = int(years_with.split('-')[0])
                    months = int(years_with.split('-')[1])
                    days = int(years_with.split('-')[2])
                    hours = int(days_with.split(':')[0])
                    minutes = int(days_with.split(':')[1])
                    seconds = int(float(days_with.split(':')[2]))
                    time_date = datetime(year=years, month=months, day=days, hour=hours, minute=minutes, second=seconds)

                    delta = datetime.now() - time_date
                    if delta > timedelta(days=1):
                        print('OK TIME')
                        poops = int(i[1])
                        print(str(ctx.message.author).split('#')[0], poops)
                        poops += 1
                        date = datetime.now()
                        database.cur.execute(f'''
                                            UPDATE poopsiki SET poops = {poops}, time = '{date}' WHERE raccoon = '{str(ctx.message.author).split('#')[0]}'
                                            ''')
                        database.bd.commit()

                        if poops == 1:
                            await ctx.send(f'{ctx.message.author.mention} pit now has {poops} poops')
                        else:
                            await ctx.send(f'{ctx.message.author.mention} pit now has {poops} poops')

                        return
                    else:
                        timeYet = str(timedelta(days=1) - delta)
                        micro_without = timeYet.split('.')[0]
                        await ctx.send(
                            f"Time has not yet passed: {micro_without}, you have {int(list(database.cur.execute(f'''SELECT poops FROM poopsiki WHERE raccoon = '{str(ctx.message.author).split('#')[0]}' '''))[0][0])} poops")
                        return

            if len(list(database.cur.execute('''SELECT * FROM poopsiki'''))) == 0:
                date = datetime.now()
                database.cur.execute(f'''
                                    INSERT INTO poopsiki VALUES('{str(ctx.message.author).split('#')[0]}', 1, '{date}')
                                    ''')
                database.bd.commit()

                await ctx.send(f'{ctx.message.author.mention} pit now has 1 poops')

                return

        @clear.error
        async def clear_error(ctx, error):
            if isinstance(error, commands.BadArgument):
                await ctx.send('Enter the argument as a number')

            if isinstance(error, commands.MissingPermissions):
                await ctx.send('You have no rights')

        @join.error
        async def join_error(ctx, error):
            if isinstance(error, commands.CommandInvokeError):
                await ctx.send('Bot is already chatting')

        @leave.error
        async def leave_error(ctx, error):
            if isinstance(error, commands.CommandInvokeError):
                await ctx.send('Bot is no longer chatting')


client = MyClient(command_prefix=prefix, self_bot=False, intents=intents)
client.run(config.TOKEN)
