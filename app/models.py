from django.db import models
from django.contrib.auth.models import User 

class Compte(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name
class Profile (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profil")
    adress = models.CharField(max_length=150)
    number = models.IntegerField(default=0)
    TYPE_CHOICES =[
        ("france", "France"),
        ("usa", "Usa"),
        ("rdc", "Rdc"),
        ("congo-brazza", "Congo-brazza"),
        ("sud-afrique", "Sud-afrique"),
         ("autres", "Autres"),
    ]
    TYPE_SEX =[
        ("m", "M"),
        ("m", "F"),
    ]
    TYPE_STATE =[
        ("marié(e)", "Marié(e)"),
        ("celibataire", "Celibaire"),
        ("veuf(ve)", "Veuf(ve)"),
        ("divorcé(e)", "divorcé(e)"),

    ]
    sex = models.CharField(max_length=1, choices=TYPE_SEX, default="")
    contry = models.CharField(max_length=15,choices=TYPE_CHOICES, default="rdc")
    birth = models.DateField(null=True, blank=False)
    state = models.CharField(max_length=50, choices=TYPE_STATE,default=50)
    email = models.EmailField()
    bio = models.TextField()
    image = models.ImageField(upload_to="image_profile")
    compte = models.OneToOneField(Compte,on_delete=models.CASCADE, related_name="comptes" , null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    facebook = models.URLField(blank=True, default="")
    whatsapp = models.URLField(blank=True, default="")
    instagram = models.URLField(blank=True, default="")

    def __str__(self):
        return f" {self.user.username} {self.user.last_name} {self.compte.name} "



class Categorie(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class Post (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post" )
    image = models.ImageField(upload_to="image_post")
    title = models.CharField(max_length=100)
    bio =  models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="categories", blank=True, null=True)
    like = models.ManyToManyField(User,related_name='post_like',blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def like_count(self):
        count = self.like.count()
        if count >= 1000000:
            return f" {count // 1000000}M "
        elif count >= 1000 : 
            return f"  {count // 1000}k"
        return str (count)

    def __str__(self):
        return f" {self.title} {self.date} "
    
class Comment_Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    bio = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,related_name='comment_like',blank=True)
    def like_count(self):
        count = self.like.count()
        if count >= 1000000:
            return f" {count // 1000000}M "
        elif count >= 1000 : 
            return f"  {count // 1000}k"
        return str (count)

    def __str__(self):
        return f" {self.user.user.username} {self.bio} {self.post.title} "

class Event (models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="event", null=False)
    image = models.ImageField(upload_to="image_evenement")
    title = models.CharField(max_length=100)
    bio =  models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,related_name='event_like',blank=True)
    date_event = models.DateTimeField()
    price = models.IntegerField()
    adress = models.CharField(max_length=150)
    def __str__(self):
        return f" {self.user.user.username} {self.title} {self.date} "
    def like_count(self):
        count = self.like.count()
        if count >= 1000000:
            return f" {count // 1000000}M "
        elif count >= 1000 : 
            return f"  {count // 1000}k"
        return str (count)
    
class Comment_Event(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comment_event")
    bio = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,related_name='post_event', blank=True)
    def __str__(self):
        return f" {self.user.user.username} {self.bio} {self.post.title} "
    def like_count(self):
        count = self.like.count()
        if count >= 1000000:
            return f" {count // 1000000}M "
        elif count >= 1000 : 
            return f"  {count // 1000}k"
        return str (count)

class NEWSLETTER (models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Mannequin(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='mannequin', limit_choices_to={'compte__name' : 'mannequin'})
    number = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f' {self.user.user.first_name} {self.user.user.last_name}'
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    def __str__(self):
        return f"{self.name} {self.price} "

class Reservation (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')
    date = models.DateTimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="services")
    bio = models.TextField()
    def __str__(self):
        return f" {self.user.first_name} - {self.user.last_name} - {self.service.name} - {self.date} "
    
class Agenda (models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    bio = models.TextField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rdv", null=True, blank=True)

    def __str__(self):
        return f"  {self.title} {self.client.first_name} {self.client.last_name} {self.date} "


class Client(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="client")
    pay = models.PositiveBigIntegerField()
    bio = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE,related_name="service_client", default="")
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f" {self.user.user.username} - {self.user.user.last_name} - {self.pay} -  {self.date} "


class Messagerie(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_message')
    text = models.TextField()
    image = models.ImageField(upload_to='message_picture',blank=True)
    date = models.DateTimeField(auto_now_add=True)
    view = models.BooleanField(default=False)
    def __str__(self):
        return f"From : {self.sender} - To: {self.receiver} -Content:{self.text} {self.date}"


class Notif(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifs')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_notif" )
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"  Notification pour {self.user.usernam} {self.post.title}  "