from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
import django
django.setup()
import re
from .models import Player,Planets
from .planets import planet_class
import json
# Create your views here.



QUADRANT=5
WORLD=100


logged_in_header=[{'name':'home','url':'/'},{'name':'sign out','url':'/logout'}]
logged_out_header=[{'name':'home','url':'/'},{'name':'sign up','url':'/signUpF'}, {'name':'sign in','url':'signInF'}]

planet_instance = planet_class()
def index(request):
  planet_instance = planet_class()
  return HttpResponse("hi there you caught me in construction!")



def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))



def signUp(request):
    redirect_to = request.GET["redirect_to"]
    #try:
    username=request.POST['username']
    password=request.POST['password']
    emailr=request.POST['email']
    if valid_email(emailr):
      user = User.objects.create_user(username, emailr, password)
      user.save()
      p=Player(username=username,email=emailr,inventory="[]",space="[1,1]",quadrant="[1,1]",planet=planet_instance.get_first_planet(),balance="5000",online="false",owned_planets="[]")
      p.save()
      login(request,user)
      """
      username = models.CharField(max_length=200)
      email = models.CharField(max_length=500)
      inventory = models.TextField()
      space = models.CharField(max_length=200)
      quadrant = models.TextField()
      planet = models.CharField(max_length=200)
      balance = models.TextField()
      online = models.CharField(max_length=200)
      owned_planets = models.TextField()
      """
      
      return redirect("/"+redirect_to)
    else:
      return redirect('/signUpF')
    #except:
    #  return redirect('/signUpF')



def signIn(request):
  redirect_to = request.GET["redirect_to"]
  try:
    username=request.POST['username']
    password=request.POST['password']
    userCurr = authenticate(request, username=username, password=password)
    if userCurr is not None:
        login(request, userCurr)
        return redirect("/"+redirect_to)
    else:
        return redirect('/signInF')
  except:
    return redirect('/signInF')



def signUpF(request):
  logged_out_header_sign_in = logged_out_header
  try:
    redirect_to = request.GET['redirect_to']
  except:
    redirect_to = ""
  logged_out_header_sign_in[1]["url"] = "/signUpF?redirect_to="+redirect_to
  logged_out_header_sign_in[2]["url"] = "/signInF?redirect_to="+redirect_to
  if request.user.is_authenticated:
    return redirect('/'+redirect_to)
  else:
    context={'header':logged_out_header,'user':request.user,"redirect":redirect_to}
    return render(request,'signUpF.html',context)



def signInF(request):
  logged_out_header_sign_in = logged_out_header
  try:
    redirect_to = request.GET['redirect_to']
  except:
    redirect_to = ""
  logged_out_header_sign_in[1]["url"] = "/signUpF?redirect_to="+redirect_to
  logged_out_header_sign_in[2]["url"] = "/signInF?redirect_to="+redirect_to
  if request.user.is_authenticated:
    return redirect("/"+redirect_to)
  else:
    context={'header':logged_out_header,'user':request.user,"redirect":redirect_to}
    return render(request,'signInF.html',context)



def logout_view(request):
    logout(request)
    return redirect('/')



def joined_game(request):
  username = json.loads(request.body.decode("utf-8"))["username"]

  user = Player.objects.get(username=username)
  user.space="false"
  user.online = "true"
  user.save()
  planet_instance.new_player(user.planet,username)  
  return HttpResponse(json.dumps(planet_instance.get_quadrant(user.planet,json.loads(user.quadrant)[0],json.loads(user.quadrant)[1])))



def planet_chat_make(request):
  username = json.loads(request.body.decode("utf-8"))["username"]
  message = json.loads(request.body.decode("utf-8"))['message']
  name = Player.objects.get(username=username).planet
  planet_instance.add_chat(name,username,message)
  return HttpResponse("The eggs know of your presence and will hunt you along with the carrots! the great salad war has ended but we still want ALL carrots to die!!!!")



def planet_chat_get(request):
  username = json.loads(request.body.decode("utf-8"))["username"]
  name = Player.objects.get(username=username).planet
  return HttpResponse(json.dumps(planet_instance.get_chat(name)))



def planet_game_loop(request):
  username = json.loads(request.body.decode("utf-8"))["username"]
  coordinates = json.loads(json.loads(request.body.decode("utf-8"))['coordinates'])
  landscape_edit = json.loads(json.loads(request.body.decode("utf-8"))['landscape_edits'])
  collision_delete = json.loads(json.loads(request.body.decode("utf-8"))['collision_delete'])
  collision_create = json.loads(json.loads(request.body.decode("utf-8"))['collision_create'])
  player_quadrant = json.loads(Player.objects.get(username=username).quadrant)
  collision_create = json.loads(json.loads(request.body.decode("utf-8"))['collision_create'])
  player_planet = Player.objects.get(username=username).planet
  if landscape_edit != []:
    planet_instance.edit_quadrant(player_planet,player_quadrant[0],player_quadrant[1],landscape_edit[0],landscape_edit[1],landscape_edit[2])
    p=Player.objects.get(username=username)
    p.balance = str(int(p.balance)+50)
    p.save()
  if collision_delete != []:
    planet_instance.delete_collision(player_planet,player_quadrant[0],player_quadrant[1], collision_delete[0], collision_delete[1])
  if collision_create != []:
    p=Player.objects.get(username=username)
    if int(p.balance)>0:
      p.balance = str(int(p.balance)-50)
      p.save()
      planet_instance.add_collision(player_planet,player_quadrant[0],player_quadrant[1], collision_create[0], collision_create[1],collision_create[2])
  planet_instance.edit_player_info(username,player_planet,"none",coordinates,"none")
  user = Player.objects.get(username=username)
  return HttpResponse(json.dumps([planet_instance.get_quadrant(user.planet,json.loads(user.quadrant)[0],json.loads(user.quadrant)[1]),planet_instance.get_quadrant_players(user.planet,json.loads(user.quadrant)[0],json.loads(user.quadrant)[1],username),user.quadrant,user.planet,user.balance]))



def change_quadrant(request):
  """direction can be up ,down, left or right"""
  username=json.loads(request.body.decode("utf-8"))['username']
  new_quadrant_dir=json.loads(request.body.decode("utf-8"))['direction']
  player_quadrant = json.loads(Player.objects.get(username=username).quadrant)
  player_planet = Player.objects.get(username=username).planet
  if new_quadrant_dir == "up":
    try:
      if player_quadrant[1]+1 <(WORLD/QUADRANT +1):
        planet_instance.edit_player_info(username,player_planet,[player_quadrant[0],player_quadrant[1]+1],"none","none")
        planet_instance.edit_player_info(username,player_planet,"none",[500,500],"none")
    except:
      pass
  elif new_quadrant_dir == "down":
    if player_quadrant[1]-1 >0:
      planet_instance.edit_player_info(username,player_planet,[player_quadrant[0],player_quadrant[1]-1],"none","none")
      planet_instance.edit_player_info(username,player_planet,"none",[500,500],"none")
  elif new_quadrant_dir == "right":
    if player_quadrant[0]+1 <(WORLD/QUADRANT +1):
      planet_instance.edit_player_info(username,player_planet,[player_quadrant[0]+1,player_quadrant[1]],"none","none")
      planet_instance.edit_player_info(username,player_planet,"none",[500,500],"none")
  else:
    if player_quadrant[0]-1 > 0:
      planet_instance.edit_player_info(username,player_planet,[player_quadrant[0]-1,player_quadrant[1]],"none","none")
      planet_instance.edit_player_info(username,player_planet,"none",[500,500],"none")
  return HttpResponse("hi, stop hacking. STOP IT!")
  #ur reading through this so i want to say that your mother is fat!
  


def handle_death(request):
  username = json.loads(request.body.decode("utf-8"))['username']
  username_of_killer = json.loads(request.body.decode("utf-8"))['username_killer']
  planet = Player.objects.get(username=username).planet
  planet_instance.remove_player_from_planet(username,planet)
  v = Player.objects.get(username=username_of_killer)
  p = Player.objects.get(username=username)
  p.planet = planet_instance.get_first_planet()
  killer_planets = json.loads(v.owned_planets)
  for i in json.loads(p.owned_planets):
    killer_planets.append(i)
    m = Planets.objects.get(planet_name=i)
    m.planet_owner = username_of_killer
  p.owned_planets="[]"
  v.owned_planets = json.dumps(killer_planets)
  killer_inventory = json.loads(v.inventory)
  for i in json.loads(p.inventory):
    killer_inventory.append(i)
  p.inventory="[]"
  v.inventory = json.dumps(killer_inventory)
  p.quadrant=json.dumps([1,1])
  p.save()
  v.save()
  return HttpResponse("literally stop")



def handle_transaction(request):
  try:
    username = json.loads(request.body.decode("utf-8"))['username']
    username_recipient = json.loads(request.body.decode("utf-8"))['username_recipient']
    index_inventory = int(json.loads(request.body.decode("utf-8"))['index'])
    v = Player.objects.get(username=username_recipient)
    p = Player.objects.get(username=username)
    recipient_inv = json.loads(v.inventory)
    player_inv = json.loads(p.inventory)
    recipient_inv.append(player_inv[index_inventory])
    player_inv.pop(index_inventory)
    v.inventory = json.dumps(recipient_inv)
    p.inventory = json.dumps(player_inv)
    p.save()
    v.save()
    return HttpResponse("true")
  except:
    return HttpResponse("false")



def handle_money(request):
  username = json.loads(request.body.decode("utf-8"))['username']
  username_recipient = json.loads(request.body.decode("utf-8"))['username_recipient']
  value_sent = int(json.loads(request.body.decode("utf-8"))['value'])
  v = Player.objects.get(username=username_recipient)
  p = Player.objects.get(username=username)
  if int(p.balance)>=value_sent:
    p.balance = str(int(p.balance)-value_sent)
    v.balance = str(int(v.balance)+value_sent)
    p.save()
    v.save()
    return HttpResponse("true")
  else:
    return HttpResponse("false")


def space_game_loop(request):
  username=json.loads(request.body.decode("utf-8"))['username']
  coordinates=json.loads(request.body.decode("utf-8"))['coordinates']
  planet_instance.move_in_space(username,coordinates)
  return HttpResponse(json.dumps(planet_instance.get_space_people(username)))
  


def enter_space(request):
  username=json.loads(request.body.decode("utf-8"))['username']
  planet_instance.enter_space(username)
  return HttpResponse(json.dumps([planet_instance.get_space_obj(),planet_instance.get_own_coords_space(username)]))
    


def planet_player(request):
  if request.user.is_authenticated:
    username = request.user.username
    return render(request,"planet_player.html",{"username":username})
  else:
    return redirect("/")
  


def enter_planet(request):
  username = json.loads(request.body.decode("utf-8"))['username']
  coords = json.loads(json.loads(request.body.decode("utf-8"))['coordinates'])
  name = planet_instance.get_planet_from_coords(coords[0],coords[1])
  planet_instance.enter_space(username)
  p = Player.objects.get(username=username)
  p.planet = name
  p.save()
  if Planets.objects.get(planet_name=name).planet_owner == "None":
    p=Planets.objects.get(planet_name=name)
    p.planet_owner=username
    p.save()
  players_space = planet_instance.player_coords_space
  for v,i in enumerate(players_space):
    if i["username"] == username:
      players_space.pop(v)
  planet_instance.player_coords_space = players_space
  return HttpResponse("hi, stop hacking. STOP IT!")



def space_player(request):
  if request.user.is_authenticated:
    username = request.user.username
    return render(request,"space_player.html",{"username":username})
  else:
    return redirect("/")



def player_list(request):
  if request.user.is_authenticated:
    username = request.user.username
    return render(request,"player_list.html",{"username":username,"players":planet_instance.player_coords_planet})
  else:
    return redirect("/")



def join_player(request):
  username = json.loads(request.body.decode("utf-8"))['username']
  username_player = json.loads(request.body.decode("utf-8"))['username_player']
  p = Player.objects.get(username=username)
  v = Player.objects.get(username=username_player)
  p.planet = v.planet
  p.quadrant = v.quadrant
  p.save()
  return HttpResponse("epic")



def planet_list(request):
  if request.user.is_authenticated:
    username = request.user.username
    return render(request,"planet_list.html",{"username":username,"planets":planet_instance.get_all_owned_planets()})
  else:
    return redirect("/")



def join_planet(request):
  username = json.loads(request.body.decode("utf-8"))['username']
  planet_name = json.loads(request.body.decode("utf-8"))['planet']
  p = Player.objects.get(username=username)
  p.planet = planet_name
  p.save()
  return HttpResponse("epic")