import os
from disnake.ext import commands
from utils import statcord

class StatcordPost(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.api = statcord.Client(self.bot, os.environ.get('statcord'))
      self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self,ctx):
      return
      self.api.command_run(ctx)

def setup(bot):
    bot.add_cog(StatcordPost(bot))