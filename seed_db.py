#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
import yaml

from rank.user.models import User


def seed_admin(admin_file):
    try:
        with open(admin_file, 'r') as file:
            admins = yaml.load(file)
            for admin in admins:
                User.create(username=admin['username'], password=admin['password'], is_admin=True, active=True)
    except IntegrityError:
        print("Some of those credentials already exist.")
        exit(0)
