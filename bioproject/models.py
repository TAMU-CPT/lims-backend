from __future__ import unicode_literals

from django.db import models
from lims.models import Phage
from django.contrib.auth.models import User, Group
# Create your models here.

ROLES = (
    (0, 'Viewer'),
    (1, 'Editor'),
    (2, 'Administrator')
)

ROLES_VERBS = {
    0: 'view',
    1: 'edit',
    2: 'administer',
}


class Bioproject(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    sample = models.ManyToManyField(Phage, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    # Can change project sharing
    access_user = models.ManyToManyField(User, blank=True, through='EditingRoleUser')
    access_group = models.ManyToManyField(Group, blank=True, through='EditingRoleGroup')

    def __str__(self):
        return self.name

    def perform_create(self, serializer):
        owner = self.request.user
        serializer.save(owner=owner)


class EditingRoleUser(models.Model):
    user = models.ForeignKey(User)
    bioproject = models.ForeignKey(Bioproject)
    role = models.IntegerField(choices=ROLES)

    def __str__(self):
        return '%s can %s %s' % (
            self.user.username,
            ROLES_VERBS[self.role],
            self.bioproject
        )


class EditingRoleGroup(models.Model):
    group = models.ForeignKey(Group)
    bioproject = models.ForeignKey(Bioproject)
    role = models.IntegerField(choices=ROLES)

    def __str__(self):
        return '%s can %s %s' % (
            self.group.name,
            ROLES_VERBS[self.role],
            self.bioproject
        )
