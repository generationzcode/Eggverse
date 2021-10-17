import time
import django
import json



from random import randint
import string
import random



django.setup()
from .models import Planets,Player




NUM_TREES = 100
WORLD_RANGE = 100 #EXTREMELY CAREFUL WITH THIS. For the planets. 
X_RANGE_SPACE = 100000#for the void
Y_RANGE_SPACE = 100000#for the void
NUM_PLANETS = 100 #each planet takes 10,000 Bytes of data(and some more) so be careful...



def make_string():
  N = 10
  res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N))
  return res


  



class planet_class:
  def __init__(self):
    if Planets.objects.count() == 0:
        self.planet_making()


  
  def add_to_planets(self,name, coordinates, landscape_arr, collision_arr):
    p=Planets(planet_name=name, planet_coordinates=json.dumps(coordinates),planet_chat=json.dumps([]),planet_landscape=json.dumps(landscape_arr),planet_players=json.dumps([]),planet_collisions=json.dumps(collision_arr),planet_owner="None",taxation=".25",description="")
    p.save()



  def move_in_space(self,username,coords):
    p=Player.objects.get(username=username)
    p.space = json.dumps(coords)
    p.save()
  


  def enter_space(self,username):
    p=Player.objects.get(username=username)
    p.space = json.dumps([Planets.objects.get(planet_name=p.planet).planet_coordinates[0]+300,Planets.objects.get(planet_name=p.planet).planet_coordinates[1]+300])

  

  def get_space_obj(self):
    planets = []
    for i in Planets.objects.all().iterator():
      planets.append(json.loads(i.planet_coordinates))
    return planets

  def get_space_people(self,username):
    players_in_space = []
    s=json.loads(Player.objects.get(username=username).space)
    p=Player.objects.filter(online="true")
    for i in p.iterator():
      players_in_space.append([i.username,[500+json.loads(i.space)[0]-s[0],500+json.loads(i.space)[1]-s[1]]])
    return players_in_space



  def new_player(self,name,username):
    obj = {"username":username,
    "quadrant":Player.objects.get(username=username).quadrant,
    "time":time.time(),"coordinates":[500,500]}
    p=Player.objects.get(username=username)
    p.planet = name
    p.save()
    self.edit_player_info(username,name,"none",[500,500],"none")
    p=Planets.objects.get(planet_name=name)
    arr = json.loads(p.planet_players)
    arr.append(obj)
    p.planet_players = json.dumps(arr)
    p.save()



  def edit_player_info(self,username,name,quadrant,game_coords,online):
    """
    none for any of them indicates no change and if it is other than none, a change is made.
    """
    player_obj = Player.objects.get(username=username)
    planet_obj = Planets.objects.get(planet_name=name)
    if quadrant != "none":
      arr_players = json.loads(planet_obj.planet_players)
      for v,i in enumerate(arr_players):
        if i["username"] == username:
          arr_players[v]['time'] = time.time()
          arr_players[v]['quadrant'] = quadrant
      player_obj.quadrant=json.dumps(quadrant)
      planet_obj.planet_players = json.dumps(arr_players)
      player_obj.save()
      planet_obj.save()
    if game_coords != "none":
      arr_players = json.loads(planet_obj.planet_players)
      for v,i in enumerate(arr_players):
        if i["username"] == username:
          arr_players[v]['time'] = time.time()
          arr_players[v]['coordinates'] = game_coords
      planet_obj.planet_players = json.dumps(arr_players)
      planet_obj.save()
    if online != "none":
      player_obj = Player.objects.get(username=username)
      player_obj.online = online
      player_obj.save()



  def get_quadrant_players(self,name,x,y):
    player_data = json.loads(Planets.objects.get(planet_name=name).planet_players)
    player_return = []
    for v,i in enumerate(player_data):
      if (time.time()-int(i["time"]))>20:
        player_data.pop(v)
        s=Player.objects.get(username=i['username'])
        s.online = "false"
        s.save()
      if i["quadrant"] == [x,y]:
        player_return.append(i["username"],i["coordinates"])
    p=Planets.objects.get(planet_name=name)
    p.planet_players = json.dumps(player_data)
    p.save()
    return player_return

  

  def add_chat(self,name,username,text):
    chats = json.loads(Planets.objects.get(planet_name=name).planet_chat)
    chats.append("["+username+"]: "+text)
    if len(chats)>10:
      chats.pop(0)
    p=Planets.objects.get(planet_name=name)
    p.planet_chat = json.dumps(chats)
    p.save()



  def edit_quadrant(self,name,X1,Y1,x2,y2,num):
    x_coord = X1*10+x2
    y_coord = Y1*10+y2
    arr = json.loads(Planets.objects.get(planet_name=name).planet_landscape)
    arr[y_coord][x_coord] = num
    p=Planets.objects.get(planet_name=name)
    p.planet_landscape = json.dumps(arr)
    p.save()



  def add_collision(self,name,X1,Y1,x2,y2,size):
    x_coord = X1*10+x2
    y_coord = Y1*10+y2
    arr = json.loads(Planets.objects.get(planet_name=name).planet_collisions)
    arr.append([x_coord,y_coord,size])
    p=Planets.objects.get(planet_name=name)
    p.planet_collisions = json.dumps(arr)
    p.save()



  def delete_collision(self,name,X1,Y1,x2,y2):
    x_coord = X1*10+x2
    y_coord = Y1*10+y2
    arr = json.loads(Planets.objects.get(planet_name=name).planet_collisions)
    for v,i in enumerate(arr):
      if (i[0] == x_coord) and (i[1]==y_coord):
        arr.pop(v)
    p=Planets.objects.get(planet_name=name)
    p.planet_collisions = json.dumps(arr)
    p.save()



  def get_quadrant(self,name,x,y):
    landscape_arr = json.loads(Planets.objects.get(planet_name=name).planet_landscape)
    collision_arr = json.loads(Planets.objects.get(planet_name=name).planet_collisions)
    collision_return = []
    for i in collision_arr:
      if (i[0]>=(x*10)) and (i[0]<=((x+1)*10)):
        if (i[1]>=(y*10)) and (i[1]<=((y+1)*10)):
          collision_return.append(i)
    landscape_return = []
    for i in range(y,(y+11)):
      landscape_return.append(landscape_arr[x:x+10])
    return [landscape_return,collision_return]



  def planet_making(self):
    for i in range(NUM_PLANETS+1):
      coords = [randint(1,X_RANGE_SPACE),randint(1,Y_RANGE_SPACE)]
      name=make_string()
      landscape = self.make_landscape()
      landscape_arr = landscape[0]
      collision_arr = landscape[1]
      self.add_to_planets(name,coords,landscape_arr,collision_arr)
    return True
    


  def make_landscape(self):
    """
    1 is green grass
    2 is red grass
    3 is sand
    4 is gold
    5 is brick
    6 is bush
    7 is tree
    8 is road
    9 is neon pink
    10 is neon blue
    11 is neon orange
    """
    landscape = []
    row=[]
    start_choice = random.choice([1,2,3])
    row.append(start_choice)
    for i in range(WORLD_RANGE):
      random_number = randint(1,10)
      if random_number < 8:
        row.append(row[i])
      else:
        row.append(randint(1,11))
    landscape.append(row)
    for i in range(WORLD_RANGE):
      row = []
      row.append(random.choice([1,2,3]))
      for v in range(WORLD_RANGE):
        random_number = randint(1,10)
        if random_number<7:
          random_number = randint(1,10)
          if random_number < 7:
            row.append(landscape[i][v+1])
          else:
            row.append(randint(1,11))
        else:
          random_number = randint(1,10)
          if random_number < 8:
            row.append(row[v])
          else:
            row.append(randint(1,11))
      landscape.append(row)
    collision_arr = []
    for i in range(NUM_TREES):
      x = randint(1,WORLD_RANGE-1)
      y = randint(1,WORLD_RANGE-1)
      landscape[y][x] = 7
      landscape[y][x+1] = 7
      landscape[y+1][x] = 7
      landscape[y-1][x] = 7
      landscape[y][x-1] = 7
      collision_arr.append([x,y,150])
    return [landscape,collision_arr]


