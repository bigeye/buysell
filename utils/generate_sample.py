#!/usr/bin/python
import csv
import random
import json

num_users = 100
num_posts = 200

users = []
posts = []

status_type = ['available', 'reserved', 'finished']
private_type = [True, False]



def gen_users():
    with open('userdata', 'rU') as csvfile:
        u500 = list(csv.reader(csvfile, delimiter=',', quotechar='"'))[1:]
        random.shuffle(u500)
        # print u500
        for i in range(1, num_users + 1):
            u = u500[i]
            users.append({'uid': i,
                          'username': (u[0] + u[1]).lower(),
                          'phone': u[8],
                          'email': u[10],
                          'first_name': u[0],
                          'last_name': u[1],})

def gen_posts():
    with open('productdata', 'r') as file:
        lines = file.read()
        products = lines.split('\n')
        random.shuffle(products)
        for i in range(1, num_posts + 1):
            u = random.choice(users)
            dsrt = random.choice(products)
            posts.append({'pid': i,
                          'writer': u['uid'],
                          'type': 'SELL',
                          'status': random.choice(status_type),
                          'is_private': random.choice(private_type),
                          'tags': None,
                          'content': '%s is very delicious! I want to sell this dessert!' % dsrt,
                          'title': '%s\'s %s' % (u['first_name'], dsrt)});
                      

if __name__ == "__main__":
    gen_users()
    gen_posts()
    with open('users.json', 'w') as file:
        file.write(json.dumps(users))
    with open('posts.json', 'w') as file:
        file.write(json.dumps(posts))
