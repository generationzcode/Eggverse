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



logged_in_header=[{'name':'home','url':'/'},{'name':'sign out','url':'/logout'}]
logged_out_header=[{'name':'home','url':'/'},{'name':'sign up','url':'/signUpF'}, {'name':'sign in','url':'signInF'}]

planet_instance=None

def index(request):
  planet_instance = planet_class()
  return HttpResponse("hi there you caught me in construction!")



def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))



def signUp(request):
  redirect_to = request.GET["redirect_to"]
  try:
    username=request.POST['username']
    password=request.POST['password']
    emailr=request.POST['email']
    if valid_email(emailr):
      user = User.objects.create_user(username, emailr, password)
      user.save()
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
      Player(username=username,email=emailr,inventory="[]",space=Planets.objects.get(id=1).planet_coordinates,quadrant="[1,1]",planet=Planets.objects.get(id=1).planet_name,balance="5000",online="false",owned_planets="[]").save()
      return redirect("/"+redirect_to)
    else:
      return redirect('/signUpF')
  except:
    return redirect('/signUpF')



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
  username = request.POST["username"]
  user = Player.objects.get(username=username)
  user.space="false"
  user.online = "true"
  user.save()  
  return json.dumps(planet_instance.get_quadrant(user.planet,json.loads(user.quadrant)[0],json.loads(user.quadrant)[1]))



def planet_game_loop(request):
  username=request.POST['username']
  coordinates = json.loads(request.POST['coordinates'])
  landscape_edit = json.loads(request.POST['landscape_edits'])
  collision_delete = json.loads(request.POST['collision_delete'])
  collision_create = json.loads(request.POST['collision_create'])
  player_quadrant = json.loads(Player.objects.get(username=username).quadrant)
  collision_create = json.loads(request.POST['collision_create'])
  player_planet = Player.objects.get(username=username).planet
  if landscape_edit != "none":
    planet_instance.edit_quadrant(player_planet,player_quadrant[0],player_quadrant[1],landscape_edit[0],landscape_edit[1],landscape_edit[2])
  if collision_delete != "none":
    planet_instance.delete_collision(player_planet,player_quadrant[0],player_quadrant[1], collision_delete[0], collision_delete[1])
  if collision_create != "none":
    planet_instance.add_collision(player_planet,player_quadrant[0],player_quadrant[1], collision_delete[0], collision_delete[1],collision_create)