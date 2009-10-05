from django.db import models
from django.forms import ModelForm, RegexField

import uuid

class Team(models.Model):
    TeamTypes = (
        ('Corporate', 'Corporate'),
        ('Group', 'Group'),
        ('Honorarium', 'Honorarium'),
    )
    type = models.CharField(max_length=10, choices=TeamTypes)
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Person(models.Model):
    ShirtSizes = (
        ('Youth-M', 'Youth-M'),
        ('Youth-L', 'Youth-L'),
        ('Adult-Small', 'Adult-Small'),
        ('Adult-Medium', 'Adult-Medium'),
        ('Adult-Large', 'Adult-Large'),
        ('Adult-XL', 'Adult-XL'),
        ('Adult-2X', 'Adult-2X'),
    )
    username = models.CharField(max_length=30, unique=True)
    shirt_size = models.CharField(max_length=15, choices=ShirtSizes)
    team = models.ForeignKey(Team, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_captain = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    emergency_name = models.CharField(max_length=30)
    emergency_phone = models.CharField(max_length=50)
    uuid = models.CharField(max_length=50, editable=False)
    goal = models.IntegerField(blank=True, null=True)
    
    def save(self):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(Person, self).save()
    
    def __unicode__(self):
        return self.last_name+' '+self.first_name


class Sponsor(models.Model):
    walker = models.ForeignKey(Person)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    pre_paid = models.BooleanField(default=False, blank=True)
    paid = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return self.last_name+' '+self.first_name

class SponsorForm(ModelForm):
    class Meta:
        model = Sponsor
        exclude = ('walker','pre_paid')

class WalkerForm(ModelForm):
    username = RegexField(label="Username", max_length=30, regex=r'^\w+$',
        help_text = "This is your public ID that others will see; up to 30 charactors, no spaces or special characters.",
        error_message = "This value must contain only letters, numbers and underscores.")
    goal = RegexField(label="Goal", regex=r'^\w+$',
        help_text = "Your Personal Goal",
        error_message = "Whole numbers only")
    
    class Meta:
        model = Person
        exclude = ('team','is_staff','is_captain')

class WalkerSettingsForm(ModelForm):
    class Meta:
        model = Person
        fields = ('shirt_size', 'first_name', 'last_name', 'phone', 'email', 'emergency_name', 'emergency_phone', 'goal')

class TeamForm(ModelForm):
    class Meta:
        model = Team

from walk.utils import decorate_bound_field
decorate_bound_field()

