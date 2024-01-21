import random
from discord.ext import commands
import discord
import json
import urllib.request
import requests
from discord import app_commands
import aiohttp
from aiohttp.client import ClientTimeout
import traceback

class ps2v2(commands.Cog):
    def __init__(self, client):
        self.client = client

        #Default Variables, Probably better way to do this?
        self.donation = "<https://nathanlithia.github.io/>"
        self.EasterEggs = ["https://media.discordapp.net/attachments/723022911589580832/801699761933123634/Chimken_Sandwhich.gif", "https://media.discordapp.net/attachments/783545628964814848/800146289190895656/image0-42.gif", "https://media.discordapp.net/attachments/670519800400969749/818012605641261056/1596954736144.gif", "https://media.discordapp.net/attachments/814384891730198538/819929709973995610/giphy_-_2020-08-11T154220.479.gif", "https://media.discordapp.net/attachments/296056831514509312/791652552826814464/image0-448.gif", "https://media.discordapp.net/attachments/193278651020738561/779947007670222848/which.gif"]
        self.PS2Images = ["https://cdn.discordapp.com/app-assets/309600524125339659/517514078227398677.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514073433309194.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514062985428993.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514065401217036.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514084455809034.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514083352969216.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514082136358916.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514072778866688.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514073055821825.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514077812293643.png"]

        self.servernum = {
            'briggs':25,
            'jaeger':19,
            'connery':1,
            'miller':10,
            'emerald':17,
            'cobalt':13,
            'soltech':40,
            'apex':24,

            25:'briggs',
            19:'jaeger',
            1:'connery',
            10:'miller',
            17:'emerald',
            13:'cobalt',
            40:'soltech',
            24:'apex'
            }

        self.servers = [
        'briggs',
        'jaeger',
        'connery',
        'miller',
        'emerald',
        'cobalt',
        'soltech',
        'apex'
        ]

        self.ps2icon = "https://pbs.twimg.com/profile_images/883060220779532288/zViSqVuM_400x400.jpg"
        self.icons = {'nc':'<:NC:528718336180092938>','vs':'<:VS:528718387627687936>','tr':'<:TR:528718372192649237>','NS':'<:NS:740268320988725381>'}
        self.colors = {'nc':0x0080ff,'vs':0x740084,'tr':0xa40000}
        self.NewCheckTime = 300

        #Default loading Embed, Probably a better to put this inside the actual command?
        self.PS2_Loading_Embed=discord.Embed(color=0xc0c0c0)
        self.PS2_Loading_Embed.set_thumbnail(url=f"https://cdn.discordapp.com/attachments/802538687698567178/805190014588682270/planetside.webp")
        self.PS2_Loading_Embed.add_field(name=f'Planetside 2', value=f'``🔵`` ``...`` ``⚪`` ``...``\n``🟣`` ``...`` ``⚪`` ``...``\n``🔴`` ``...`` ``⚪`` ``...``', inline=True)
        self.PS2_Loading_Embed.add_field(name='Statistics', value=f'``Loading...``\n``🌍`` ``...``\n``⚪`` ``...``', inline=True)

        #Query cache variables, Not utilizing these right now.
        self.briggsTime   = None
        self.jaegerTime   = None
        self.conneryTime  = None
        self.millerTime   = None
        self.emeraldTime  = None
        self.colbaltTime  = None
        self.soltechTime  = None

        self.briggsData     = None
        self.jaegerData     = None
        self.conneryData    = None
        self.millerData     = None
        self.emeraldData    = None
        self.colbaltData    = None
        self.soltechData    = None


    async def JsonGrab(self, URL, seconds = 15):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            timeout = ClientTimeout(total=0)
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, headers=headers, timeout=timeout) as response:
                    return json.loads(await response.text())
        except urllib.error.URLError:
            print("Error: Could not connect to API")
            return 'URLERROR'


    async def PS2WorldGrab(self, WorldID):
        print(f"http://wt.honu.pw/api/population/{WorldID}")
        return await self.JsonGrab(f"http://wt.honu.pw/api/population/{WorldID}")


    def PS2EmbedGen(self, JData, ServerName = "Server_Name", textmode = False):
        """Generates Embeds from supplied data"""
        #Extracting data from JSON.
        NC = JData['nc']
        VS = JData['vs']
        TR = JData['tr']
        NS = JData['ns']
        NSNC = JData['ns_nc']
        NSVS = JData['ns_vs']
        NSTR = JData['ns_tr']
        total = JData['total'] #NC+VS+TR+NS
        if random.randint(0,100) < 5: EmbedImage = random.choice(self.EasterEggs)
        else: EmbedImage = random.choice(self.PS2Images)
        #Generating the Embed.
        if textmode == False:
            ps2embed=discord.Embed(color=0xc0c0c0)
            ps2embed.set_thumbnail(url=f"{EmbedImage}")
            ps2embed.add_field(name=f'Teams', value=f'``🔵`` ``{NC}``\n``🟣`` ``{VS}``\n``🔴`` ``{TR}``', inline=True)
            ps2embed.add_field(name=f'Bots', value=f'``⚪`` ``{NSNC}``\n``⚪`` ``{NSVS}``\n``⚪`` ``{NSTR}``', inline=True)
            ps2embed.add_field(name='Statistics', value=f'``{ServerName.upper()}``\n``🌍`` ``{total}``\n``🤖`` ``{NS}``', inline=True)


        else:
            return f"{ServerName.upper()} Population:\nNC: {NC}\nTR: {TR}\nVS: {VS}\nTOTAL: {total}"
            
        #Return a generated embed.
        return ps2embed

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(pass_context=True, aliases=['jaeger', 'Jaeger', 'connery', 'Connery', 'miller', 'Miller', 'emerald', 'Emerald', 'cobalt', 'Cobalt', 'soltech', 'Soltech', 'apex', 'Apex', 'briggs', 'Briggs'])
    async def PS2_Serverv2(self, ctx):
        """
        Checks the status of a Planetside2 Server.
        Usage: {ServerName}
        """
        server = ctx.message.content.split()[0][1:].lower()
        print(server)
        if server in self.servers:
            if ctx.author.bot == False:
                try:
                    if server.lower() == 'connery':
                        header = str(self.client.get_channel(998406090729476159).name).replace('Connery:', '')
                    else:
                        header = self.donation
                    MSG = await ctx.reply(f'{header}', embed=self.PS2_Loading_Embed)
                    setattr(self, f"{server}Data", self.PS2EmbedGen(await self.PS2WorldGrab(self.servernum[server]), server))
                    await MSG.edit(content=f'{header}',embed=getattr(self, f"{server}Data"))
                except Exception as e: await ctx.send(f'Could not connect to API. Please try again later.\n{e}\n{traceback.format_exc()}')
            else:
                    MSG = await ctx.reply(f'{self.PS2EmbedGen(self.PS2WorldGrab(self.servernum[server]), server, True)}')

    @app_commands.command(name = "connery", description = "Connery Population") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
    async def first_command(self, interaction):
        await interaction.response.send_message(self.PS2EmbedGen(self.PS2WorldGrab(self.servernum["connery"])))

async def setup(client):
    await client.add_cog(ps2v2(client))
