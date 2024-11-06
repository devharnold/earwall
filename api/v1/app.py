#!/usr/bin/env python3

"""Flask API application"""
from engine import db_storage
from flask import Flask
import graphene
from graphene import relay
from engine.db_storage import get_db_connection
from models import Account, Transactions, User
from models.wallets import cashwallet
from models.linkpaypal import PaypalConfig

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()

class Account(graphene.ObjectType):
    id = graphene.ID()
    account_number = graphene.String()

class Transactions(graphene.ObjectType):
    id = graphene.ID()
    transaction_id = graphene.Int()

class PaypalConfig(graphene.ObjectType):
    id = graphene.ID()
    paypalconfig_id = graphene.String()

    