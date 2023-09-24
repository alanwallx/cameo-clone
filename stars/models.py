from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Video(models.Model):
    name = models.CharField(max_length=500)
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)


class Photo(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class Star(models.Model):
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32, blank=True)
    price = models.IntegerField()
    occupation = models.CharField(max_length=32)
    owner = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="owned_by")
    # this will become the URL for the star profile
    username = models.CharField(max_length=32)
    cover = models.ImageField(upload_to='images/')
    application_letter = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('RETURNED', 'Returned with request for further details'),
        ('RESUBMITTED', 'Resubmitted'),
        ('SUSPENDED', 'Suspended'),
        ('RESUB_SUSPENDED', 'Resubmitted after being suspended'),
        ('DECLINED', 'Declined'),
        ('RESUB_DECLINED', 'Resubmitted after being declined'),
        ('PENDING', 'Pending'),
    ]
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='PENDING',
    )
    reason_for_status_change = models.TextField(blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.occupation}) - {self.status}"


# the following are in case we want to remove a user, the orders will remain but the user or star will be replaced with a default ID
ANONYMOUS_USER_ID = 1
ANONYMOUS_STAR_ID = 1


class Order(models.Model):
    customer = models.ForeignKey(User,
                                 default=ANONYMOUS_USER_ID,
                                 on_delete=models.SET_DEFAULT)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    starbooked = models.ForeignKey(Star,
                                   default=ANONYMOUS_STAR_ID,
                                   on_delete=models.SET_DEFAULT)
    completed = models.BooleanField(default=False)
    custommessage = models.TextField(max_length=500, default="")
    recipient = models.CharField(max_length=32, default="")
    messagefrom = models.CharField(max_length=32, default="")

    def __str__(self):
        return f"Order number: {self.id} {self.starbooked.firstname} {self.starbooked.lastname} booked by {self.customer}"


class Ignored(models.Model):
    customer = models.ForeignKey(User,
                                 default=ANONYMOUS_USER_ID,
                                 on_delete=models.SET_DEFAULT)
    star = models.ForeignKey(Star, blank=True, related_name="ignored",
                             default=ANONYMOUS_STAR_ID,
                             on_delete=models.SET_DEFAULT)

    def __str__(self):
        return f"{self.customer}"
