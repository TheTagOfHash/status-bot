import discord
from discord.utils import get
from discord.ext import commands

bot = commands.Bot(command_prefix="r?", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'Logged into {bot.user}')


@bot.command(aliases=['presence'])
@commands.has_permissions(administrator=True)
async def status(ctx, status_type: str, *, msg):
    if ctx.author == bot.user:
        return
    await ctx.message.delete()
    if status_type.lower() == 'p' or status_type.lower() == 'playing':
        await bot.change_presence(activity=discord.Game(name=msg))
        embed = discord.Embed(title='Status changed!', colour=discord.Colour.orange())
        embed.add_field(name=f'Status is now "Playing {msg}"!', value='Enjoy the beautiful new status!', inline=False)
        await ctx.send(embed=embed)
    elif status_type.lower() == 'l' or status_type.lower() == 'listening':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=msg))
        embed = discord.Embed(title='Status changed!', colour=discord.Colour.orange())
        embed.add_field(name=f'Status is now "Listening to {msg}"!', value='Enjoy the beautiful new status!',
                        inline=False)
        await ctx.send(embed=embed)
    elif status_type.lower() == 'w' or status_type.lower() == 'watching':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=msg))
        embed = discord.Embed(title='Status changed!', colour=discord.Colour.orange())
        embed.add_field(name=f'Status is now "Watching {msg}"!', value='Enjoy the beautiful new status!', inline=False)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def statusrole(ctx, checkstring: str, role: int):
    removeCount = 0
    if get(ctx.guild.roles, id=role):
        roleObj = get(ctx.guild.roles, id=role)
    else:
        await ctx.send(f":PepeHmm: I couldn't find a role with id `{role}`")
        return
    await ctx.send(":PepeOk: Please wait. This might take a bit")
    status_members = []
    for member in ctx.guild.members:
        for s in member.activities:
            if isinstance(s, discord.CustomActivity) and checkstring in str(s):
                status_members.append(member)
            elif roleObj in member.roles:
                await member.remove_roles(roleObj)
                removeCount += 1
    if len(status_members) == 0:
        await ctx.send(f":sadge: I couldn't find anybody with \"{checkstring}\" in their status")
        if removeCount > 0:
            await ctx.send(f":sadge: I removed role with id `{roleObj.id}` from {removeCount} members")
        return
    for member in status_members:
        await member.add_roles(roleObj)
    await ctx.send(f":AceHeadpat: Added role with id `{roleObj.id}` to {str(len(status_members))} member(s)")
    if removeCount > 0:
        await ctx.send(f":sadge: I removed role with id `{roleObj.id}` from {removeCount} members")

bot.run("token here")
