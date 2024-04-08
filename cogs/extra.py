import disnake
from disnake.ext import commands

class ExtraCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.todo_video = "https://youtu.be/XHj7OjtvBY4"

  @commands.slash_command()
  async def help(self, inter):
    await inter.response.send_message(f"{self.todo_video}")
  
  @commands.slash_command()
  async def invite(self, inter):
    """Shows all the links you need for Todo bot"""
    embed = disnake.Embed(title='Important Links', description=f"**[Invite](https://discord.com/api/oauth2/authorize?client_id=904903467590619157&permissions=379968&scope=bot%20applications.commands)** | [Support](https://discord.gg/cT9rmtf) | **[Vote](https://top.gg/bot/904903467590619157/vote)**", color=inter.guild.me.color)
    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
    await inter.response.send_message(embed=embed)
    
  @commands.slash_command()
  async def stats(self, inter):
    """Shows stats and other random info about the Todo bot"""
    embed = disnake.Embed(title='Bot Stats', color=inter.guild.me.color)
    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
    embed.add_field(name=":computer: Commands", value=len([x.name for x in self.bot.slash_commands]), inline=False)
    embed.add_field(name="\u2694 Servers", value=str(len(self.bot.guilds)), inline=False)
    embed.add_field(name="🎂 Birthday", value="November 1")
    embed.add_field(name="🛠️ Owner",value="<@432689076626522132>", inline=False)
    await inter.response.send_message(embed=embed)

def setup(bot):
  bot.add_cog(ExtraCommands(bot))