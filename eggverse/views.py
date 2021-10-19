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
  message = json.loads(json.loads(request.body.decode("utf-8"))['coordinates'])




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
  if collision_delete != []:
    planet_instance.delete_collision(player_planet,player_quadrant[0],player_quadrant[1], collision_delete[0], collision_delete[1])
  if collision_create != []:
    planet_instance.add_collision(player_planet,player_quadrant[0],player_quadrant[1], collision_create[0], collision_create[1],collision_create[2])
  planet_instance.edit_player_info(username,player_planet,"none",coordinates,"none")
  user = Player.objects.get(username=username)
  return HttpResponse(json.dumps([planet_instance.get_quadrant(user.planet,json.loads(user.quadrant)[0],json.loads(user.quadrant)[1]),planet_instance.get_quadrant_players(user.planet,json.loads(user.quadrant)[0],json.loads(user.quadrant)[1],username)]))



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
  planet = Player.objects.get(username=username).planet
  planet_instance.remove_player_from_planet(username,planet)
  p = Player.objects.get(username=username)
  p.planet = planet_instance.get_first_planet()
  p.quadrant=json.dumps([1,1])
  p.save()



def space_game_loop(request):
  username=json.loads(request.body.decode("utf-8"))['username']
  coordinates=json.loads(request.body.decode("utf-8"))['coordinates']
  planet_instance.move_in_space(username,coordinates)
  return HttpResponse(json.dumps(planet_instance.get_space_people(username)))
  


def enter_space(request):
  username=json.loads(request.body.decode("utf-8"))['username']
  planet_instance.enter_space(username)
  return HttpResponse(json.dumps(planet_instance.get_space_obj()))
    


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
  return HttpResponse("hi, stop hacking. STOP IT!")
