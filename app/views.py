from django.shortcuts import render, redirect, get_object_or_404
from .models import Post,Profile,Categorie,Comment_Event,Comment_Post,Compte,Client,Notif,NEWSLETTER,Messagerie,Event,Agenda,Reservation,Service,Mannequin
from .forms import PostForm, ProfileForm,ProfilUserForm, CategorieForm, ClientForm,Comment_EventForm,PostMForm,MessageForm,Comment_PostForm,CompteForm,EventForm,NewsForm,SignUpForm,AgendaForm,ServiceForm,ReservationForm,MannequinForm
from django.contrib.auth import authenticate, login
from django.urls import reverse 
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.mail import send_mail
from django.contrib.auth import logout 

def home(request):
    posts = Categorie.objects.prefetch_related('categories').all().order_by('-name')
    post_profile = Post.objects.all()
    profile = Profile.objects.filter(compte__name = 'mannequin')
    return render (request, 'home.html',{'posts':posts, 'profile':profile, 'post_profile':post_profile})

def home_mannequin(request, compte_id):
    categorie = get_object_or_404(Compte, id=compte_id)
    posts = Profile.objects.filter(compte = categorie)
    return render (request, 'home_mannequin.html', {'categorie':categorie, 'posts':posts})
def home_mannequin_search(request):
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats = User.objects.filter(Q(username__icontains=query)) |  User.objects.filter(Q(last_name__icontains=query))
    return render (request, 'search_home_mannequin.html', {'query':query, 'resultats':resultats})
def profile_home(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    posts = Post.objects.filter(user=profile.user)
    return render (request, 'profile_home.html',{'profile':profile, 'posts':posts})



#Here I build a way to sign up in our app
def signup (request):
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, email=email)
            login(request, user)
            return redirect ('edit_profil')
    else :
        form = SignUpForm()
    return render (request, 'signup.html', {'form':form})

#Here is a way to edit a profile 
def edit_profil(request):
    profile,created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = ProfilUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and user_form.is_valid() : 
            form.save()
            user_form.save()
            return redirect ('profile')
    else :
        form = ProfileForm(instance= profile)
        user_form = ProfilUserForm(instance=request.user)
    return render (request, 'edit_profil.html', {'form':form, 'user_form':user_form,'profile':profile})

#here is an user's profile with all of informations
@login_required(login_url='/account/login/')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by('-date')[:4]
    comments = Comment_Post.objects.all().order_by('-date')[:4]
    clients = Comment_Post.objects.filter(user=profile).order_by('-date')[:4]
    notifs = request.user.notifs.filter(is_read=True)
    return render (request, 'profile.html', {'profile':profile,'posts':posts, 'clients':clients,'notifs':notifs,'comments':comments})
    

#here is a way to like or unlike a post
@login_required(login_url='/account/login/')
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.like.all():
        post.like.remove(request.user)
    else :
        post.like.add(request.user)
    return HttpResponseRedirect(f'/#post-{post_id}')

#here is a way to see a post detail 
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    commentaires = Comment_Post.objects.filter(post=post)
    posts = Post.objects.all().exclude(id=post_id).order_by('-date')[:5]
    return render (request, 'post_detail.html', {'post':post, 'commentaires':commentaires, 'posts':posts})


#heere is a way to comment a post 
@login_required(login_url='/account/login/')
def comment_post (request, post_id):
    if request.method == 'POST' : 
        post = get_object_or_404(Post, id=post_id)
        form = Comment_PostForm(request.POST)
        if form.is_valid():
            bio = form.cleaned_data['bio']
            profil = Profile.objects.get(user=request.user)
            comment = Comment_Post(bio=bio, post=post, user=profil)
            comment.save()
            return redirect (reverse('post_detail', kwargs={'post_id':post_id}))
    else : 
        form = Comment_PostForm()
    return render (request, 'post_detail.html', {'form':form, 'post':post})

#here is a way to like a comment
@login_required(login_url='/account/login/')
def like_comment(request, comment_post_id):
    comment = get_object_or_404(Comment_Post, id=comment_post_id)
    user = request.user
    if user in comment.like.all() : 
        comment.like.remove(user)
    else : 
        comment.like.add(user)
    return redirect ('post_detail', post_id=comment.post.id)

#here is way to see a categorie detail 
def categorie (request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    posts = categorie.categories.all()
    return render (request, 'categorie.html', {'categorie':categorie, 'posts':posts})

#here is way to search a field 
def search_home(request):
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats= Post.objects.filter(Q(title__icontains=query))
    return render (request, 'search_home.html', {'resultats':resultats, 'query':query})

#here is a way to see a link through categorie, post, event
def add(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by('-date')[:4]
    comments = Comment_Post.objects.all().order_by('-date')[:4]
    return render (request, 'add.html', {'profile':profile,'posts':posts, 'comments':comments})

#here is way to see post's performance, to add new post , to edit or delete a post
def post(request):
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by('-date')
    comments = Comment_Post.objects.all().order_by('-date')
    return render (request, 'post.html', {'profile':profile,'posts':posts, 'comments':comments})

#here is way to add a neww post
def post_form(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST' :
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect ('post')
    else :
        form = PostForm()
    return render (request, 'post_form.html', {'form':form,'profile':profile})

#here is a way to see a post_detail
def post_detail_profil(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = Profile.objects.get(user=request.user)
    likes = post.like.all()
    comments = Comment_Post.objects.filter(post=post)
    return render (request, 'post_detail_profil.html', {'post':post, 'profile':profile, 'likes':likes,'comments':comments})

#here is way to edit post 
def post_modif(request, post_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('post_detail', kwargs={'post_id':post_id}))
    else :
        form = PostForm(instance=post)
    return render (request, 'post_modif.html', {'post':post, 'form':form,'profile':profile})

#here is a way to delete a post
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post')

#here is way to search a post from profile
def search_post(request):
    profile =Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats = Post.objects.filter(Q(title__icontains=query))
    return render (request, 'search_post.html', {'query':query, 'resultats':resultats,'profile':profile})

#here is way to search a comment from profile
def search_comment_post(request):
    query = request.GET.get('q')
    profile =Profile.objects.get(user=request.user)
    resultats = []
    if query : 
        resultats = Comment_Post.objects.filter(Q(bio__icontains=query))
    return render (request, 'search_comment_post.html', {'query':query, 'resultats':resultats, 'profile':profile})

#here is a way to see a comment-detail from a post 
def comment_post_detail(request, comment_post_id):
    comment = get_object_or_404(Comment_Post, id=comment_post_id)
    profile = Profile.objects.get(user=request.user)
    return render (request, 'comment_post_detail.html', {'comment':comment, 'profile':profile})

#here is way to edit comment form post  
@login_required
def comment_post_modif(request, comment_post_id):
    comment = get_object_or_404(Comment_Post, id=comment_post_id)
    profile =Profile.objects.get(user=request.user)
    if request.user.is_superuser : 
        if request.method == 'POST':
            form = Comment_PostForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                return redirect(reverse('post_detail', kwargs={'post_id':comment.post.id}))
        else :
            form = Comment_PostForm(instance=comment)
        return render (request, 'comment_modif.html', {'comment':comment, 'form':form,'profile':profile})
    if profile == comment.user :
        if request.method == 'POST':
            form = Comment_PostForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                return redirect(reverse('post_detail', kwargs={'post_id':comment.post.id}))
        else :
            form = Comment_PostForm(instance=comment)
        return render (request, 'comment_modif.html', {'comment':comment, 'form':form,'profile':profile})
    else  :
        return redirect('profile')
        

#here is a way to delete  comment from a post
def comment_post_delete(request, comment_post_id):
    comment = get_object_or_404(Comment_Post, id=comment_post_id)
    comment.delete()
    return redirect(reverse('post_detail_profil', kwargs={'post_id':comment.post_id}))

#here is a way to add a new categorie
def categorie_form(request):
    profile =Profile.objects.get(user=request.user)
    if request.user.is_superuser : 
        if request.method == 'POST':
            form = CategorieForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect ('categorie_gestion')
        else :
            form = CategorieForm()
        return render (request, 'categorie_gestion.html', {'form':form, 'profile':profile})
    
#here is a way to see how to manage Categorie
def categorie_gestion(request):
    profile = Profile.objects.get(user=request.user)
    categories = Categorie.objects.all()
    return render (request, 'categorie_gestion.html', {'profile':profile, 'categories':categories, 'profile':profile})

#here is a way to edit a categorie name
def categorie_modif (request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid() :
            form.save()
            return redirect('categorie_gestion')
    else :
        form = CategorieForm(instance=categorie)
    return render (request, 'categorie_modif.html', {'form':form, 'categorie':categorie, 'profile':profile})

#here is a way to delete a categorie_id
def categorie_delete(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    categorie.delete()
    return redirect('categorie_gestion')

#here is a way to search a categorie
def search_categorie(request):
    query = request.GET.get('q')
    profile = Profile.objects.get(user=request.user)
    resultats = []
    if query : 
        resultats = Categorie.objects.filter(Q(name__icontains=query))
    return render (request, 'search_categorie.html', {'query':query,'resultats':resultats, 'profile':profile})

#here is way to add a new event
def event_form(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST' :
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('post')
    else :
        form = EventForm()
    return render (request, 'event_form.html', {'form':form,'profile':profile})

#here is a way to see a event_detail
def event_detail_profil(request, event_id):
    post = get_object_or_404(Event, id=event_id)
    profile = Profile.objects.get(user=request.user)
    likes = post.like.all()
    comments = Comment_Event.objects.filter(post=post)
    return render (request, 'event_detail_profil.html', {'post':post, 'profile':profile, 'likes':likes,'comments':comments})

#here is way to edit event
def event_modif(request,event_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('event_detail', kwargs={'event_id':event_id}))
    else :
        form = EventForm(instance=post)
    return render (request, 'event_modif.html', {'post':post, 'form':form,'profile':profile})

#here is a way to delete event
def event_delete(request, event_id):
    post = get_object_or_404(Event, id=event_id)
    post.delete()
    return redirect('post')

#here is way to search event from profile
def search_event(request):
    query = request.GET.get('q')
    profile =Profile.objects.get(user=request.user)
    resultats = []
    if query : 
        resultats = Event.objects.filter(Q(title__icontains=query))
    return render (request, 'search_event.html', {'query':query, 'resultats':resultats, 'profile':profile})

def event(request):
    profile= Profile.objects.get(user=request.user)
    events = Event.objects.all()
    comments = Comment_Event.objects.all()
    return render (request, 'event.html', {'profile':profile, 'events':events,'comments':comments})


#here is way to search a comment from profile
def search_comment_event(request):
    query = request.GET.get('q')
    profile = Profile.objects.get(user=request.user)
    resultats = []
    if query : 
        resultats = Comment_Event.objects.filter(Q(bio__icontains=query))
    return render (request, 'search_comment_event.html', {'query':query, 'resultats':resultats,'profile':profile})
#here is way to search a comment from profile
def search_comment_event_per_post(request, event_id):
    post = Event.objects.get(id=event_id)
    query = request.GET.get('q',''.strip)
    resultats = []
    if query : 
        resultats = post.comment_event.filter(bio__icontains = query) 
    else :
        ressultats = post.comment_event.all()
    profile = Profile.objects.get(user=request.user)
    return render (request, 'search_comment_event_per_post.html', {'query':query, 'resultats':resultats,'post':post,'profile':profile})

def search_comment_post_per_post(request, post_id):
    post = Post.objects.get(id=post_id)
    query = request.GET.get('q',''.strip)
    resultats = []
    if query : 
        resultats = post.comment.filter(bio__icontains = query) 
    else :
        ressultats = post.comment_.all()
    profile = Profile.objects.get(user=request.user)
    return render (request, 'search_comment_post_per_post.html', {'query':query, 'resultats':resultats,'post':post,'profile':profile})

#here is a way to see a comment-detail from an event 
def comment_event_detail(request, comment_event_id):
    comment = get_object_or_404(Comment_Event, id=comment_event_id)
    profile = Profile.objects.get(user=request.user)
    return render (request, 'comment_event_detail.html', {'comment':comment, 'profile':profile})


#here is way to edit comment form event  
@login_required
def comment_event_modif(request, comment_event_id):
    comment = get_object_or_404(Comment_Event, id=comment_event_id)
    profile = Profile.objects.get(user=request.user)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = Comment_EventForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                return redirect(reverse('event_detail_profil', kwargs={'event_id':comment.event.id}))
        else :
            form = Comment_EventForm(instance=comment)
        return render (request, 'comment_event_modif.html', {'comment':comment, 'form':form,'profile':profile})
    if profile == comment.user :
        if request.method == 'POST':
            form = Comment_EventForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                return redirect(reverse('event_detail_profil', kwargs={'event_id':comment.event.id}))
        else :
            form = Comment_EventForm(instance=comment)
        return render (request, 'comment_event_modif.html', {'comment':comment, 'form':form,'profile':profile})
    else :
        return redirect ('profile')
        

#here is a way to delete  comment from a event
def comment_event_delete(request, comment_event_id):
    comment = get_object_or_404(Comment_Event, id=comment_event_id)
    comment.delete()
    return redirect(reverse('event_detail_profil', kwargs={'event_id':comment.event_id}))


#here is a way to add someone, place or something in your agenda
def agenda_form(request):
    profile = Profile.objects.get(user=request.user)
    posts = Agenda.objects.all() 
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect (reverse('agenda_form'))
    else :
        form = AgendaForm()
    return render (request, 'agenda.html', {'profile':profile, 'form':form,'posts':posts})

#here is a way to edit a agenda's field
def agenda_modif(request, agenda_id):
    profile = Profile.objects.get(user=request.user)
    agenda = get_object_or_404(Agenda, id=agenda_id)
    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            return redirect ('agenda_form')
    else :
        form = AgendaForm(instance=agenda)
    return render (request, 'agenda_modif.html',{'profile':profile, 'agenda':agenda, 'form':form})

#here is a way to see a agenda's field
def agenda_detail(request, agenda_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Agenda, id=agenda_id)
    return render (request, 'agenda_detail.html',{'profile':profile, 'post':post})

#here is a way to delete a agenda's field
def agenda_delete(request, agenda_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Agenda, id=agenda_id)
    post.delete()
    return redirect('agenda_form')

#here is a way to search a agenda's field
def agenda_search(request):
    profile = Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats= []
    if query :
        resultats = Agenda.objects.filter(Q(title__icontains=query))
    return render (request, 'search_agenda.html',{'profile':profile, 'resultats':resultats})

#here is a way to search a agenda's field
def agenda_search_date(request):
    profile = Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats= []
    if query :
        resultats = Agenda.objects.filter(Q(date__icontains=query))
    return render (request, 'search_agenda.html',{'profile':profile, 'resultats':resultats})

#here is a way to see and add mannequin
def mannequin(request):
    profile = Profile.objects.get(user=request.user)
    posts = Profile.objects.filter(compte__name='mannequin')
    return render (request, 'mannequin.html',{"posts":posts, 'profile':profile})

#here is a way to edit it
def mannequin_modif(request, mannequin_id):
    post = Profile.objects.get(id=mannequin_id)
    user =post.user
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST' :
        form = ProfileForm(request.POST, instance=post) 
        user_form = ProfilUserForm(request.POST, instance=user)
        if form.is_valid() and user_form.is_valid() :
            form.save()
            return redirect ('mannequin')
    else :
        form = ProfileForm(instance=post) 
        user_form = ProfilUserForm( instance=user)
    return render (request, 'mannequin_modif.html', {'post':post, 'form':form, 'profile':profile,'user_form':user_form})

#here is a way to delete it
def mannequin_delete(request, mannequin_id):
    post = get_object_or_404(Profile, id=mannequin_id)
    post.delete()
    return redirect (reverse('mannequin'))

#here is way to search a mannequin's field
def mannequin_search(request):
    query = request.GET.get('q')
    resultats = []
    profile = Profile.objects.get(user=request.user)
    if query :
        resultats = Profile.objects.filter(Q(user__username__icontains=query))
    return render (request, 'mannequin_search.html', {'query':query, 'resultats':resultats,'profile':profile})

def mannequin_detail(request, mannequin_id):
    post = get_object_or_404(Profile, id=mannequin_id)
    profile = Profile.objects.get(user=request.user)
    user_form = post.user
    return render (request, 'mannequin_detail.html', {'post':post,'profile':profile, 'user_form':user_form})


#here is a way to add someone, place or something in your agenda
def client(request):
    profile = Profile.objects.get(user=request.user)
    posts = Client.objects.all() 
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect (reverse('client'))
    else :
        form = ClientForm()
    return render (request, 'client.html', {'profile':profile, 'form':form,'posts':posts})

#here is a way to edit a client's field
def client_modif(request, client_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect ('client')
    else :
        form = ClientForm(instance=post)
    return render (request, 'client_modif.html',{'profile':profile, 'post':post, 'form':form})

#here is a way to see a client's field
def client_detail(request, client_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Client, id=client_id)
    return render (request, 'client_detail.html',{'profile':profile, 'post':post})

#here is a way to delete a agenda's field
def client_delete(request, client_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Client, id=client_id)
    post.delete()
    return redirect('client')

#here is a way to search a client's field
def client_search(request):
    profile = Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats= []
    if query :
        resultats = User.objects.prefetch_related('client').filter(Q(username__icontains=query))
    return render (request, 'search_client.html',{'profile':profile, 'resultats':resultats})

def client_search_date(request):
    profile = Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats= []
    if query :
        resultats = Client.objects.filter(Q(date__icontains=query))
    return render (request, 'search_client.html',{'profile':profile, 'resultats':resultats})


#here is way to add a new reservation
def reservation_form(request):
    if request.user.is_authenticated  :
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST' :
            form = ReservationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect ('post')
        else :
            form = ReservationForm()
        return render (request, 'reservation_form.html', {'form':form,'profile':profile})
    else  :
        return redirect ('login')
        

#here is a way to see a reservation_detail
def reservation_detail(request, reservation_id):
    post = get_object_or_404(Reservation, id=reservation_id)
    profile = Profile.objects.get(user=request.user)
    return render (request, 'reservation_detail.html', {'post':post, 'profile':profile})

#here is way to edit reservation_id
def reservation_modif(request,reservation_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('reservation_detail', kwargs={'reservation_id':reservation_id}))
    else :
        form = ReservationForm(instance=post)
    return render (request, 'reservation_modif.html', {'post':post, 'form':form,'profile':profile})

#here is a way to delete event
def reservation_delete(request, reservation_id):
    post = get_object_or_404(Reservation, id=reservation_id)
    post.delete()
    return redirect('reservation')


#here is way to search event from profile
def search_reservation(request):
    profile= Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats = Reservation.objects.filter(Q(date__icontains=query))
    return render (request, 'search_reservation.html', {'query':query, 'resultats':resultats, 'profile':profile})

def reservation(request):
    profile= Profile.objects.get(user=request.user)
    posts = Reservation.objects.all().order_by('-date')
    return render (request, 'reservation.html', {'profile':profile, 'posts':posts})

#here is a way to see all of User account
def infos(request):
    posts = Profile.objects.filter(compte__name = 'professionnel') 
    posts_2 = Profile.objects.filter(compte__name = 'sponsor') 
    posts_3 = Profile.objects.filter(compte__name = 'mannequin')
    posts_4 = Profile.objects.filter(compte__name = 'client')  
    profile = Profile.objects.get(user=request.user)
    return render (request, 'infos.html', {'posts':posts, 'profile':profile,'posts_2':posts_2,'posts_3':posts_3,'posts_4':posts_4})

#here is a way to delete a account's user
def infos_delete(request, profile_id, user_id):
    post = get_object_or_404(Profile, id=profile_id )
    post_2 = get_object_or_404(User, id=user_id)
    post.delete()
    post_2.delete()
    return redirect ('infos')

#here is a way to delete a account's user
def infos_modif(request, profile_id):
    if request.user.is_superuser  :
        post = get_object_or_404(Profile, id=profile_id )
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST' :
            form = ProfileForm(request.POST, instance=post)
            user_form = ProfilUserForm(request.POST, instance=post.user)
            if form.is_valid():
                form.save()
                user_form.save()
                return redirect('infos')
        else :
            form = ProfileForm(instance=post)
            user_form = ProfilUserForm(instance=post.user)
        return render (request,'infos_modif.html', {'post':post, 'profile':profile, 'form':form, 'user_form':user_form})
    else :
        return HttpResponse('Vous essayez une action qui est illicite et contre nos reglements, après 3 tentatives votre compte sera bloqué ainsi que votre email de connexion.')
    
#here is a way to search a user
def infos_search(request):
    profile = Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats = User.objects.filter(Q(username=query))
    return render (request, 'search_infos.html', {'profile':profile, 'query':query}) 



def infos_detail(request, infos_id, infos_user_id):
    post = get_object_or_404(Profile, id=infos_id)
    profile = Profile.objects.get(user=request.user)
    user = User.objects.get(id=infos_user_id)
    return render (request, 'infos_detail.html', {'post':post,'profile':profile, 'user':user})

def messagerie (request):
    receiver = User.objects.filter(is_superuser=True).first()
    profile = Profile.objects.get(user=receiver)
    if request.method == 'POST':
        content = request.POST.get('text')
        image  = request.FILES.get('image')
        message = Messagerie.objects.create(sender=request.user, image=image,text=content, receiver=receiver)
        return redirect (reverse('messagerie'))
    else  :
        message_senders = Messagerie.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
        message_sender_detail = User.objects.filter(id__in=message_senders) 
        messages = Messagerie.objects.filter(sender=request.user, receiver=receiver).order_by('date') | Messagerie.objects.filter(sender=receiver, receiver=request.user).order_by('date')
    return render (request, 'messagerie.html', {'profile':profile,'receiver':receiver, 'message_sender': message_sender_detail, 'messages':messages})

def inbox(request, user_id):
    sender_id = Messagerie.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    senders = User.objects.filter(id__in=sender_id)
    receiver_id = Messagerie.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    receivers = User.objects.filter(id__in=receiver_id)
    messages = Messagerie.objects.filter(receiver=request.user).order_by('date')
    inbox_url = reverse('inbox', kwargs={'user_id':user_id})
    message_senders = Messagerie.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    message_sender_details = User.objects.filter(id__in=message_senders)
    message_sender = {}
    for sender in senders :
        messages = Messagerie.objects.filter(sender=request.user, receiver=sender)
        message_sender [sender] = messages
    context = {'senders':senders, 'message_senders':message_sender_details, 'inbox_url':inbox_url}
    return render (request, 'messagerie.html', context) 

def admin_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    profile = Profile.objects.get(user=receiver)
    if request.method == 'POST' :
        image = request.FILES.get('image')
        content = request.POST.get('text')
        receiver =User.objects.get(id=receiver_id)
        message = Messagerie.objects.create(image=image, receiver=receiver, text=content, sender=request.user)
        return redirect (reverse('admin_message', kwargs={'receiver_id':receiver_id}))
    else :
        receiver = User.objects.get(id=receiver_id)
        message_sender = Messagerie.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
        message_sender_detail = User.objects.filter(id__in=message_sender) 
        profiles = Profile.objects.filter(user=receiver)
        messages = Messagerie.objects.filter(sender=request.user, receiver=receiver).order_by('date') | Messagerie.objects.filter(sender=receiver, receiver=request.user).order_by('date')
    return render  (request, 'messagerie.html', {'profile':profile,'profiles':profiles,'receiver':receiver,'messages':messages, 'message_senders':message_sender_detail})

#ici je developpe le search message
def search_message(request):
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats =User.objects.filter(Q(username__icontains=query)) 
    return render (request,'search_message.html',  {'query':query, 'resultats':resultats})
#ici je developpe comment je peux modifier un message déjà envoyé
def modif_message(request, pk):
    messagerie = get_object_or_404(Messagerie,pk=pk,sender=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST,request.FILES, instance=messagerie)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_message', kwargs={'receiver_id':messagerie.receiver_id}))
    else : 
        form = MessageForm(instance=messagerie)
    return render (request, 'modif_message.html', {'form':form, 'messagerie':messagerie})


#here i created the way that i can delete 
def delete_message(request, messagerie_id):
    messagerie = get_object_or_404(Messagerie, id=messagerie_id, sender=request.user)
    messagerie.delete()
    if request.user.is_superuser :
        return redirect(reverse('admin_message', kwargs={'receiver_id':messagerie.receiver_id}))
    else :
        return redirect('messagerie')

#here i created the way that i can delete 
def delete_message_receiver(request, messagerie_id):
    messagerie = get_object_or_404(Messagerie, id=messagerie_id, receiver=request.user)
    messagerie.delete()
    if request.user.is_superuser :
        return redirect(reverse('admin_message', kwargs={'receiver_id':messagerie.receiver_id}))
    else :
        return redirect('messagerie')



@login_required
#here is way to edit reservation_id
def reservation_modif_client(request,reservation_id):
    profile = Profile.objects.get(user=request.user)
    post = get_object_or_404(Reservation, id=reservation_id)
    if post.user != request.user :
        return HttpResponseForbidden("Vous n'avez pas la permission, à modifier  cette reservation")
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('reservation_detail', kwargs={'reservation_id':reservation_id}))
    else :
        form = ReservationForm(instance=post)
    return render (request, 'reservation_modif.html', {'post':post, 'form':form,'profile':profile})
@login_required
#here is a way to delete event
def reservation_delete_client(request, reservation_id):
    post = get_object_or_404(Reservation, id=reservation_id)
    if post.user != request.user :
        return HttpResponseForbidden("Vous n'avez pas la permission, de supprimer cette reservation")
    if request.method == 'POST' :
        post.delete()
        return redirect('reservation_client')


#here is way to search event from profile
def search_reservation_client(request):
    profile= Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats = Reservation.objects.filter(Q(date__icontains=query)).order_by('-date').filter(user=request.user)
    return render (request, 'search_reservation.html', {'query':query, 'resultats':resultats, 'profile':profile})

def reservation_client(request):
    profile= Profile.objects.get(user=request.user)
    posts = Reservation.objects.all().order_by('-date').filter(user=request.user)
    return render (request, 'reservation.html', {'profile':profile, 'posts':posts})

@login_required
#here is way to see post's performance, to add new post , to edit or delete a post
def post_personnel(request):
    profile = Profile.objects.get(user=request.user)
    if profile.compte.name == 'mannequin' :
        posts = Post.objects.filter(user=request.user).order_by('-date')
        comments = Comment_Post.objects.filter(user=profile).order_by('-date')
        return render (request, 'post.html', {'profile':profile,'posts':posts, 'comments':comments})
    else :
        return redirect ('profile')

@login_required
#here is way to add a neww post
def post_form_personnel(request):
    profile = Profile.objects.get(user=request.user)
    if profile.compte.name == "mannequin":
        if request.method == 'POST' :
            form = PostMForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user =  request.user
                post.save()
                return redirect ('post_personnel')
        else :
            form = PostMForm()
        return render (request, 'post_form.html', {'form':form,'profile':profile})
    else :
        return redirect ('profile')

#here is a way to see a post_detail
def post_detail_personnel(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile = Profile.objects.get(user=request.user)
    likes = post.like.all()
    comments = Comment_Post.objects.filter(post=post)
    return render (request, 'post_detail_profil.html', {'post':post, 'profile':profile, 'likes':likes,'comments':comments})

#here is way to edit post 
def post_modif_personnel(request, post_id):
    profile = Profile.objects.get(user=request.user)
    if profile.compte.name == 'mannequin':
        post = get_object_or_404(Post, id=post_id)
        if request.method == 'POST':
            form = PostMForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect(reverse('post_detail_personnel', kwargs={'post_id':post_id}))
        else :
            form = PostMForm(instance=post)
        return render (request, 'post_modif.html', {'post':post, 'form':form,'profile':profile})

#here is a way to delete a post
def post_delete_personnel(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_personnel')

#here is way to search a post from profile
def search_post_personnel(request):
    profile =Profile.objects.get(user=request.user)
    query = request.GET.get('q')
    resultats = []
    if query : 
        resultats = Post.objects.filter(Q(title__icontains=query)).order_by('date').filter(user=request.user)
    return render (request, 'search_post.html', {"profile":profile, 'resultats':resultats, 'query':query})

@login_required(login_url='/account/login/')
def subscribe(request):
    if request.method == 'POST' : 
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "vous êtes inscrit à la newsletter")
            return redirect ('home')
    else :
        form = NewsForm()
    return render (request, 'home.html', {'form':form})

def send_newsletter(request):
    if request.user.is_superuser : 
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            recipients = NEWSLETTER.objects.values_list('email', flat=True)
            if subject and message : 
                send_mail(subject, message, 'therryconsu@gmail.com', recipients)
                messages.success(request, "La newsletter a été envoyée à tous les abonnés ")
                print("envoie d'email")
            else :
                messages.error(request, "sujet et message sont requis")
        return render (request, 'newsletter.html', {'profile':profile})
    else  :
        return redirect ('home')


def error(request, exception):
    return redirect ('home')

@login_required
def notif(request):
    notifs = Notif.objects.filter(is_read=False)
    return render (request, 'notif.html', {'notifs':notifs})

@login_required
def mark_as_read(request, notif_id):
    notif = get_object_or_404(Notif, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notif')


def logout_view(request):
    logout(request)
    return redirect ('login')