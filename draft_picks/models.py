from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

PICKS = (
    ('1', 'First Round'),
    ('2', 'Second Round'),
    ('3', 'Third Round'),
)


class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player_detail', kwargs={'pk': self.id})


class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mascot = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("team_detail", kwargs={"team_id": self.id})

class Draft(models.Model):
    pick = models.CharField(max_length=1, choices=PICKS, default=PICKS[0][0])
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_pick_display()} - {self.player.name} to {self.team.name}"

    class Meta:
        ordering = ['pick']