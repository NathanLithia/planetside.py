import random
from discord.ext import commands
import discord
import json
import urllib.request
import requests
from discord import app_commands

class ps2v2(commands.Cog):
    def __init__(self, client):
        self.client = client

        #Default Variables, Probably better way to do this?
        # TODO: export all of the following into a seperate config file and read in
        self.donation = "<https://nathanlithia.github.io/>"
        self.EasterEggs = ["https://media.discordapp.net/attachments/723022911589580832/801699761933123634/Chimken_Sandwhich.gif", "https://media.discordapp.net/attachments/783545628964814848/800146289190895656/image0-42.gif", "https://media.discordapp.net/attachments/670519800400969749/818012605641261056/1596954736144.gif", "https://media.discordapp.net/attachments/814384891730198538/819929709973995610/giphy_-_2020-08-11T154220.479.gif", "https://media.discordapp.net/attachments/296056831514509312/791652552826814464/image0-448.gif", "https://media.discordapp.net/attachments/193278651020738561/779947007670222848/which.gif"]
        self.PS2Images = ["https://cdn.discordapp.com/app-assets/309600524125339659/517514078227398677.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514073433309194.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514062985428993.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514065401217036.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514084455809034.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514083352969216.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514082136358916.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514072778866688.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514073055821825.png","https://cdn.discordapp.com/app-assets/309600524125339659/517514077812293643.png"]
        self.multiPopQueryUrlBase = "https://wt.honu.pw/api/population/multiple?"
        self.multiPopQueryParamToken = "worldID="
        self.multiPopQueryDelimiterToken = "&"

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
        self.PS2_Loading_Embed.add_field(name='Planetside 2', value=f'``🔵`` ``...`` ``⚪`` ``...``\n``🟣`` ``...`` ``⚪`` ``...``\n``🔴`` ``...`` ``⚪`` ``...``', inline=True)
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


    def JsonGrab(self, URL, seconds = 15):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            result = requests.get(URL, headers=headers)
            print(result.content.decode())
        except urllib.error.URLError:
            print("Error: Could not connect to API")
            return 'URLERROR'
        else:
            return json.loads(result.content.decode())


    def PS2WorldGrab(self, *WorldIDs):
        params = ""
        for ids in WorldIDs:
            params += self.multiPopQueryDelimiterToken
            params += self.multiPopQueryParamToken
            params += ids

        params = params[1:] # removes the first unneeded delimiter

        print(f"{self.multiPopQueryUrlBase}{params}")
        return self.JsonGrab(f"{self.multiPopQueryUrlBase}{params}")


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
            ps2embed.add_field(name='Teams', value=f'``🔵`` ``{NC}``\n``🟣`` ``{VS}``\n``🔴`` ``{TR}``', inline=True)
            ps2embed.add_field(name='Bots', value=f'``⚪`` ``{NSNC}``\n``⚪`` ``{NSVS}``\n``⚪`` ``{NSTR}``', inline=True)
            ps2embed.add_field(name='Statistics', value=f'``{ServerName.upper()}``\n``🌍`` ``{total}``\n``🤖`` ``{NS}``', inline=True)


        else:
            return f"{ServerName.upper()} Population:\nNC: {NC}\nTR: {TR}\nVS: {VS}\nTOTAL: {total}"
            
        #Return a generated embed.
        return ps2embed
    
    # this function shall be responsible for parsing, verification of inputs, and minor processing
    # returns valid server names in lowercase
    def ParseServerNames(self, ctx, *args):
        requestedServers = []
        requestedServers.append(ctx.message.content.split()[0][1:]) 
        requestedServers.extend(args)

        # verify and process
        for server in requestedServers:
            server = server.lower()
            if not (server in self.servers):
                requestedServers.remove(server)

        return requestedServers

    # after reading the discord docs, this is alias abuse lmao
    # hack way to allow for ">connery emerald miller" using first term as command and rest as params
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(pass_context=True, aliases=['jaeger', 'Jaeger', 'connery', 'Connery', 'miller', 'Miller', 'emerald', 'Emerald', 'cobalt', 'Cobalt', 'soltech', 'Soltech', 'apex', 'Apex', 'briggs', 'Briggs'])
    async def PS2_Serverv2(self, ctx, *args):
        """
        Checks the status of a Planetside2 Server.
        Usage, one or more of: {ServerName}
        """
        requestedServers = self.ParseServerNames(ctx, args)
        requestedServerIds = map(lambda serverName : self.servernum[serverName], requestedServers)
        
        try:
            popData = self.PS2WorldGrab(requestedServerIds)
            for server, serverPopData in requestedServers, popData:
                if ctx.author.bot == False:
                    if server == 'connery':
                        header = str(self.client.get_channel(998406090729476159).name).replace('Connery:', '')
                    else:
                        header = self.donation
                    MSG = await ctx.reply(f'{header}', embed=self.PS2_Loading_Embed)
                    setattr(self, f"{server}Data", self.PS2EmbedGen(serverPopData, server))
                    await MSG.edit(content=f'{header}',embed=getattr(self, f"{server}Data"))
                else:
                    MSG = await ctx.reply(f'{self.PS2EmbedGen(serverPopData, server, True)}')
        except Exception as e: 
            await ctx.send(f'Could not connect to API. Please try again later.')

    @app_commands.command(name = "connery", description = "Connery Population") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
    async def first_command(self, interaction):
        await interaction.response.send_message(self.PS2EmbedGen(self.PS2WorldGrab(self.servernum["connery"])))

async def setup(client):
    await client.add_cog(ps2v2(client))