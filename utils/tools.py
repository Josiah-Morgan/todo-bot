from replit import db

def GetData(table, guild_id):
  try:
    v = db[f"{table}"]
  except KeyError:
    return None 

  try: 
    if v[str(guild_id)] == []: # checks if its a empty list
      return None 
    #elif str(guild_id) not in v:
     # return None
    else:
      return v[str(guild_id)] 
  except TypeError:
    return None

  except KeyError:
    return None  

def RemoveData(table, guild_id):
  try:
    v = db[f"{table}"]
  except KeyError:
    return None  
  try:
    v.pop(str(guild_id))
  except KeyError:
    return None  

def AddData(table, guild_id, add): # strings 
  try:
    v = db[f"{table}"]
  except KeyError:
    v = db[f"{table}"] = {}  


  v[str(guild_id)] = add

  return True  
  
def AddAppend(event, table, guild_id, add): # list
  try:
    v = db[f"{table}"]
  except KeyError:
    v = db[f"{table}"] = {}  

  if event == "Add":
    try:
      db[f"{table}"][f"{guild_id}"].append(add)

    except KeyError:
      db[f"{table}"][f"{guild_id}"] = []
      db[f"{table}"][f"{guild_id}"].append(add)

  elif event == "Remove":
    try:
      v[f"{guild_id}"].remove(add)
    except KeyError:
      return None