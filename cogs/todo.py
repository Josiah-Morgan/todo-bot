import disnake
from disnake.ext import commands
from utils.tools import RemoveData, GetData, AddAppend

class Todo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command() 
  async def todo(self, inter):
    return

  @todo.sub_command(options=[disnake.Option('user', "The user to see the list of", type=disnake.OptionType.user)])
  async def list(self, inter, user=None):
    """List all your todo's"""

    if user == None: user = inter.author
    
    # Actual list stuff

    todo = GetData('todo', user.id)
    if not todo:
        return await inter.response.send_message('You don\'t have anything on your list.', ephemeral=True)
    else:
      
      # Building embed
      
      description = ''
      for index, td in enumerate(todo):
        description += f'\n `{index + 1}` {td}'
      
      #title = f"Todo list"

      embed = disnake.Embed(title='Todo List', description=description, color=user.color)
      embed.set_author(name = f'{user.display_name}', icon_url = user.display_avatar)
      await inter.response.send_message(embed=embed)   

  @todo.sub_command()
  async def add(self, inter, content: str):
    """Add to your todo list

    Parameters
    ----------
    content: Example: todo add Get 100 members
    ...
    """
    if len(content) > 150:
      return await inter.response.send_message("Text has to be below 150 characters", ephemeral=True)    

    todo_count = GetData('todo', inter.author.id)
    if todo_count == None: todo_count = '0'
    if len(todo_count) >= 15:
      return await inter.response.send_message('You can only have up to 15 todos at a time', ephemeral=True)
    else:
      AddAppend('Add', 'todo', inter.author.id, str(content))
      embed = disnake.Embed(title='Added a todo', color=inter.author.color, description=content)
      embed.set_author(name = f'{inter.author.display_name}', icon_url = inter.author.display_avatar)
      await inter.response.send_message(embed=embed)

  @todo.sub_command()
  async def remove(self, inter, *, ids: str):
    """Remove a todo from the list.

    Parameters
    ----------
    ids: Example: todo remove 1, Example: todo remove 4 7 13
    ...
    """
    todo = GetData("todo", inter.author.id)
    # No todos

    if not todo:
      return await inter.response.send_message('You have nothing in your todo list.', ephemeral=True)

    todo = {f'{index + 1}': todo for index, todo in enumerate(todo)}
    todos_to_remove = []

    # Checking id's provided

    ids = ids.split(' ')
    for todo_id in ids:
      if not todo_id.isdigit():
        return await inter.response.send_message(f'`{todo_id}` is not a valid todo id. (need a number)', ephemeral=True)
      if todo_id not in todo.keys():
        return await inter.response.send_message(f'You don\'t have a todo with id `{todo_id}`.', ephemeral=True)
      if todo_id in todos_to_remove:
        return await inter.response.send_message(f'You provided todo id `{todo_id}` more than once.', ephemeral=True)
      todos_to_remove.append(todo_id)


    entries = [(todo[todo_id]) for todo_id in todos_to_remove]
    contents = '\n'.join([f'`{todo_id}` {todo[todo_id]}' for todo_id in todos_to_remove])

    for thing in entries:
      AddAppend('Remove', 'todo', inter.author.id, thing)

    # Building embed
    embed = disnake.Embed(title=f'Deleted {len(todos_to_remove)} todo(s)', color=inter.author.color)
    embed.set_author(name = f'{inter.author.display_name}', icon_url = inter.author.display_avatar)
    embed.add_field(name='Content', value=contents)

    
    await inter.response.send_message(embed=embed)

  @todo.sub_command()
  async def clear(self, inter):
    """
    Clears your todo list.

    """
    try:
      todo = GetData("todo", inter.author.id)

      # No todos

      if not todo:
        return await inter.response.send_message('You have nothing in your todo list.', ephemeral=True)

      RemoveData('todo', inter.author.id)
      
      embed = disnake.Embed(title=f'Cleared {len(todo)} todo(s)', color=inter.author.color)
      embed.set_author(name = f'{inter.author.display_name}', icon_url = inter.author.display_avatar)
    except Exception as e:
      return await inter.response.send_message(e, ephemeral=True)
    
    await inter.response.send_message(embed=embed)


def setup(bot):
  bot.add_cog(Todo(bot))    