#!/usr/bin/python
import sys
import os
sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'buysell.settings'

import django
django.setup()

import csv
import random
import json
from django.contrib.auth import hashers
from django.contrib.auth.models import User
from buysell.api.post.models import Post
from buysell.api.account.models import UserProfile

num_users = 100
num_posts = 200

users = []
posts = []
users_fixture = []
posts_fixture = []
userprofile_fixture = []

status_type = ['avail', 'reserved', 'finish']
private_type = [True, False]



def gen_users():
    with open('userdata', 'rU') as csvfile:
        u500 = list(csv.reader(csvfile, delimiter=',', quotechar='"'))[1:]
        random.shuffle(u500)
        # 1: superuser
        for i in range(2, num_users + 2):
            u = u500[i]

            user, created = User.objects.get_or_create(username = (u[0] + u[1]).lower(),
                                                       email = u[10],
                                                       password = hashers.make_password(u[10]),
                                                       first_name = u[0],
                                                       last_name = u[1],
                                                       is_active = True,
                                                       is_superuser = False,
                                                       is_staff = False)
            user.save()

            up, created = UserProfile.objects.get_or_create(user = user,
                                                            phone = u[8])
            if not created:
                up.save()
            users.append(user)


def gen_posts():
    with open('productdata', 'r') as file:
        lines = file.read()
        products = lines.split('\n')
        random.shuffle(products)
        for i in range(1, num_posts + 1):
            u = random.choice(users)
            dsrt = random.choice(products)
            post, created = Post.objects.get_or_create(writer = u,
                                              status_type = random.choice(status_type),
                                              is_private = random.choice(private_type),
                                              content = '%s is very delicious! I want to sell this dessert!' % dsrt,
                                              title = '%s\'s %s' % (u.first_name, dsrt))
            if not created:
                post.save()
            posts.append(post)
                      

if __name__ == "__main__":
    gen_users()
    gen_posts()
    with open('fixtures.json', 'w') as file:
        fixtures = []
        fixtures.extend(users_fixture)
        fixtures.extend(userprofile_fixture)
        fixtures.extend(posts_fixture)
        file.write(json.dumps(fixtures))
