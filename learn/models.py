from django.db import models
from accounts import models as acc
from django.utils import timezone
# Create your models here.




class Classroom(models.Model):
    USER_TYPE_CHOICES = (
        ('public','Public'),
        ('private','Private')
    )
    name = models.CharField(max_length=250,blank=False)
    topic = models.CharField(max_length=250,blank=False,default='other')
    educator = models.ForeignKey(acc.EducatorProfile,on_delete=models.CASCADE,null=True, related_name='classrooms')

    additional_educators = models.ManyToManyField(acc.EducatorProfile, related_name='joined_classrooms', blank=True)

    student = models.ManyToManyField(acc.LearnerProfile,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250,blank=True)
    room_code = models.IntegerField(null=True,blank=True)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='public')


    # notes = models.ForeignKey(Notes,on_delete=models.CASCADE,null=True)
    # alerts = models.ForeignKey(Alerts,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.name}'



class Message(models.Model):
    sender = models.ForeignKey(acc.CustomUser,on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    content = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)


    def __str__(self):
        return f'{self.sender}--{self.content}'




class Notes(models.Model):
    name = models.CharField(max_length=255,blank=False,default='')
    content = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey('Classroom',  null=True,on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.content


class Alerts(models.Model):
    name = models.CharField(max_length=255,blank=False,default='')
    content = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey('Classroom', null=True, on_delete=models.CASCADE, related_name='alerts')

    def __str__(self):
        return self.content




class PersonalMessage(models.Model):
    sender = models.ForeignKey(acc.CustomUser,on_delete=models.CASCADE, related_name='user1_messages')
    receiver = models.ForeignKey(acc.CustomUser,on_delete=models.CASCADE, related_name='user2_messages')
    text = models.TextField(blank=True)  # or models.TextField for longer messages
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'From {self.sender} to {self.receiver}: {self.text[:50]}...'  # Display first 50 chars


class Requests(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted')
    ]

    requester = models.ForeignKey(acc.CustomUser,on_delete=models.CASCADE)
    content = models.CharField(max_length=500,blank=False)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester}"