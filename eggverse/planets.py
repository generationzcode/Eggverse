import time
import django
import json
import math



from random import randint
import string
import random



django.setup()
from .models import Planets,Player



QUADRANT = 5
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
    self.player_coords_planet = []
    self.player_coords_space=[]


  
  def add_to_planets(self,name, coordinates, landscape_arr, collision_arr):
    p=Planets(planet_name=name, planet_coordinates=json.dumps(coordinates),planet_chat=json.dumps([]),planet_landscape=json.dumps(landscape_arr),planet_players=json.dumps([]),planet_collisions=json.dumps(collision_arr),planet_owner="None",taxation=".25",description="")
    p.save()



  def get_planet_from_coords(self,x,y):
    for i in Planets.objects.all().iterator():
      if (json.loads(i.planet_coordinates)[0]==x) and (json.loads(i.planet_coordinates)[1]==y):
        return i.planet_name
    return False



  def move_in_space(self,username,coords):
    for v,i in enumerate(self.player_coords_space):
      if i["username"] == username:
        self.player_coords_space[v]={"username":username,"coordinates":json.loads(coords),"time":time.time()}
      if (time.time()-i["time"])>20:
        self.player_coords_space.pop(v)



  def enter_space(self,username):
    p=Player.objects.get(username=username)
    p.space = json.dumps([int(json.loads(Planets.objects.get(planet_name=p.planet).planet_coordinates)[0])+300,int(json.loads(Planets.objects.get(planet_name=p.planet).planet_coordinates)[1])+300])
    existence = False
    for v,i in enumerate(self.player_coords_space):
      if i["username"] == username:
        existence=True
    if existence == False:
      self.player_coords_space.append({"username":username,"coordinates":[int(json.loads(Planets.objects.get(planet_name=p.planet).planet_coordinates)[0])+300,int(json.loads(Planets.objects.get(planet_name=p.planet).planet_coordinates)[1])+300],"time":time.time()})  
  

  def get_space_obj(self):
    planets = []
    for i in Planets.objects.all().iterator():
      planets.append(json.loads(i.planet_coordinates))
    return planets
  


  def get_own_coords_space(self,username):
    for i in self.player_coords_space:
      if i["username"] == username:
        return i["coordinates"]



  def get_space_people(self,username):
    ret_coords = []
    for i in self.player_coords_space:
      if i["username"]!=username:
        ret_coords.append(i)
    return ret_coords



  def new_player(self,name,username):
    obj = {"username":username,
    "quadrant":Player.objects.get(username=username).quadrant,
    "time":time.time(),"coordinates":[500,500],"planet":name}
    p=Player.objects.get(username=username)
    p.planet = name
    p.save()
    self.edit_player_info(username,name,"none",[500,500],"none")
    reg = True
    for i in self.player_coords_planet:
      if i["username"] == username:
        reg = False
    if reg == True:
      self.player_coords_planet.append(obj)
    p=Planets.objects.get(planet_name=name)
    arr = json.loads(p.planet_players)
    print(self.player_coords_planet)
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
      arr_players = self.player_coords_planet
      for v,i in enumerate(arr_players):
        if i["username"] == username:
          arr_players[v]['time'] = time.time()
          arr_players[v]['quadrant'] = quadrant
      player_obj.quadrant=json.dumps(quadrant)
      self.player_coords_planet = arr_players
      player_obj.save()
      planet_obj.save()
    if game_coords != "none":
      arr_players = self.player_coords_planet
      for v,i in enumerate(arr_players):
        if i["username"] == username:
          arr_players[v]['time'] = time.time()
          arr_players[v]['coordinates'] = game_coords
      self.player_coords_planet = arr_players
      planet_obj.save()
    if online != "none":
      player_obj = Player.objects.get(username=username)
      player_obj.online = online
      player_obj.save()



  def get_first_planet(self):
    for i in Planets.objects.all().iterator():
      return i.planet_name



  def remove_player_from_planet(self,username,name):
    """
    none for any of them indicates no change and if it is other than none, a change is made.
    """
    planet_obj = Planets.objects.get(planet_name=name)
    arr_players = self.player_coords_planet
    for v,i in enumerate(arr_players):
      if i["username"] == username:
        arr_players.pop(v)
    self.player_coords_planet = arr_players
    planet_obj.save()
    """if game_coords != "none":
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
      player_obj.save()"""



  def get_quadrant_players(self,name,x,y,username):
    player_data = self.player_coords_planet
    player_return = []
    for v,i in enumerate(player_data):
      if (time.time()-int(i["time"]))>20:
        player_data.pop(v)
        s=Player.objects.get(username=i['username'])
        s.online = "false"
        s.save()
      try:
        if (json.loads(i["quadrant"]) == [x,y]) and (i["planet"]==name) and (i["username"]!=username):
          player_return.append([i["username"],i["coordinates"]])
      except:
        if (i["quadrant"] == [x,y]) and (i["planet"]==name) and (i["username"]!=username):
          player_return.append([i["username"],i["coordinates"]])
        
    self.player_coords_planet = player_data
    return player_return



  def get_chat(self,name):
    return json.loads(Planets.objects.get(planet_name=name).planet_chat)

  

  def add_chat(self,name,username,text):
    chats = json.loads(Planets.objects.get(planet_name=name).planet_chat)
    chats.append("["+username+"]: "+text)
    if len(chats)>10:
      chats.pop(0)
    p=Planets.objects.get(planet_name=name)
    p.planet_chat = json.dumps(chats)
    p.save()



  def edit_quadrant(self,name,X1,Y1,x2,y2,num):
    x_coord = int(X1)*QUADRANT+int(x2)
    y_coord = int(Y1)*QUADRANT+int(y2)
    print(x_coord)
    print(x_coord)
    arr = json.loads(Planets.objects.get(planet_name=name).planet_landscape)
    arr[y_coord][x_coord] = num
    p=Planets.objects.get(planet_name=name)
    p.planet_landscape = json.dumps(arr)
    p.save()
    print("saved")



  def add_collision(self,name,X1,Y1,x2,y2,size):
    x_coord = X1*QUADRANT+round(x2/200)
    y_coord = Y1*QUADRANT+round(y2/200)
    arr = json.loads(Planets.objects.get(planet_name=name).planet_collisions)
    arr.append([x_coord,y_coord,size])
    p=Planets.objects.get(planet_name=name)
    p.planet_collisions = json.dumps(arr)
    p.save()



  def delete_collision(self,name,X1,Y1,x2,y2):
    x_coord = X1*QUADRANT+x2
    y_coord = Y1*QUADRANT+y2
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
      if (i[0]>=(x*QUADRANT)) and (i[0]<=((x+1)*QUADRANT)):
        if (i[1]>=(y*QUADRANT)) and (i[1]<=((y+1)*QUADRANT)):
          collision_return.append([i[0]-x*QUADRANT,i[1]-y*QUADRANT,i[2]])
    landscape_return = []
    for i in range(y*QUADRANT,(y*QUADRANT+QUADRANT)):
      landscape_return.append(landscape_arr[i][x*QUADRANT:x*QUADRANT+QUADRANT])
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



  def get_all_owned_planets(self):
    return_planets=[]
    for i in Planets.objects.all().iterator():
      if i.planet_owner != "None":
        return_planets.append([i.planet_name,i.planet_owner])
    return return_planets
  


  def get_owned_planets(self,username):
    return_planets=[]
    for i in Planets.objects.all().iterator():
      if i.planet_owner == username:
        return_planets.append([i.planet_name,i.taxation])
    return return_planets