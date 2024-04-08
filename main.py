import disnake, os
from utils import keep_alive
from disnake.ext import commands

class Todo(commands.InteractionBot):
  def __init__(self):
    super().__init__(reconnect=True, help_command=None, activity=disnake.Game(name="Todos | /help"))
    self.bot = self

  async def start(self, *args, **kwargs):
      
      for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
          self.bot.load_extension(f'cogs.{filename[:-3]}')
          print(filename + ' Loaded')

      await super().start(*args)

  async def on_ready(self):
    print('Bot Online')


#keep_alive.keep_alive()
#bot = Todo()
#bot.run(os.environ.get('TOKEN'))