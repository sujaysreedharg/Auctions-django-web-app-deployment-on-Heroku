from django.contrib.auth.models import AbstractUser
from django.db import models


# this is the model for users and it inherits AbstractUser
class User(AbstractUser):
    pass


# model for listings
class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.CharField(max_length=64)
    image_link = models.CharField(
        max_length=250, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)





class Watchlistssme(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class addcomment(models.Model):
    user = models.CharField(max_length=64)
    content = models.CharField(max_length=128)
    listingid = models.PositiveIntegerField()



class addbid(models.Model):
    listingid = models.IntegerField()
    amount= models.IntegerField()
    user = models.CharField(max_length=64)



# model to store the winners
class bidwinner(models.Model):
    seller = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.PositiveIntegerField()
    finalbid = models.IntegerField()

