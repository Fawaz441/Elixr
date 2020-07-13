from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Ship(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='ships')
    views = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,null=True)
    launched_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    new = models.BooleanField(default=False)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse("ship_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.name

class Suit(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='suits')
    views = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,null=True)
    launched_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    new = models.BooleanField(default=False)

    
    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    
    def get_absolute_url(self):
        return reverse("suit_detail", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.name

class OrderedShip(models.Model):
    ship = models.ForeignKey(Ship,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.ship.name + "CART"
    

    def get_total(self):
        return self.ship.price * self.quantity


class OrderedSuit(models.Model):
    suit = models.ForeignKey(Suit,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total(self):
        return self.suit.price * self.quantity

    def __str__(self):
        return self.suit.name + "CART"


class Order(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    ord_ships = models.ManyToManyField(OrderedShip)
    ord_suits = models.ManyToManyField(OrderedSuit)
    ordered = models.BooleanField(default = False)
    paystack_ref_code = models.CharField(max_length=100,null=True,blank=True)
    paystack_amount = models.CharField(max_length=100,null=True,blank=True)
    delivered = models.BooleanField(default = False)

    def total(self):
        total = 0
        for ord_ship in self.ord_ships.all():
            total+=ord_ship.get_total()
        for ord_suit in self.ord_suits.all():
            total+=ord_suit.get_total()
        return total

    def ship_total(self):
        ship_total = 0
        for ship in self.ord_ships.all():
            ship_total+=ship.get_total()
        return ship_total

    def suit_total(self):
        suit_total = 0
        for suit in self.ord_suits.all():
            suit_total+=suit.get_total()
        return suit_total

    def __str__(self):
        return self.buyer.username
    

