import aiohttp, os
from disnake.ext import commands, tasks

class Topgg(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.topgg_stats.start()
    self.session = aiohttp.ClientSession()

  @tasks.loop(minutes=30)
  async def topgg_stats(self):
    await self.bot.wait_until_ready()
    try:
      headers = {'Authorization': os.environ.get('topgg')}
      payload = {'server_count': len(self.bot.guilds)}

      await self.session.post('https://top.gg/api/bots/904903467590619157/stats', headers=headers, json=payload)
      print('Bot stats posted')
    except Exception as e:
      print('Failed to Post Stats', "The [topgg](https://top.gg/bot/730594098695635014) stats have failed to be posted\n > **Error:** {}: {}".format(type(e).__name__, e))  


def setup(bot):
  bot.add_cog(Topgg(bot))    