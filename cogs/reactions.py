import discord
from discord.ext import commands
import config
from discord import utils


class Reaction(commands.Cog):
    def __init__(self, client):
        commands.Bot.__init__(self)
        commands.Cog.__init__(self)

    # for gui in self.guilds:
    #     for mem in gui.members:
    #         if gui.id == 795744870026707004 and mem.id not in bots:
    #             print(str(mem).split('#')[0])
    #             database.cur.execute(f'''
    #             INSERT INTO milk VALUES('{str(mem).split('#')[0]}', 0, '{datetime(year=1, month=1, day=1, hour=1, minute=1)}')
    #             ''')
    #             database.bd.commit()

    @commands.Cog.listener()
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

    @commands.Cog.listener()
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


def setup(client):
    client.add_cog(Reaction(client))
