#!/usr/bin/python3
from decimal import Decimal
import random
import sys
from logger import logger
from rpcutils import errorhandler as rpcerrorhandler
from wsutils import topics
from .constants import *
from . import apirpc


def convertToSatoshi(strAmount):
    return str(Decimal(strAmount) * 100000000)


def getMethodSchemas(name):
    return getRequestMethodSchema(name), getResponseMethodSchema(name)


def getRequestMethodSchema(name):
    return RPC_JSON_SCHEMA_FOLDER + name + SCHEMA_CHAR_SEPARATOR + REQUEST + SCHEMA_EXTENSION


def getResponseMethodSchema(name):
    return RPC_JSON_SCHEMA_FOLDER + name + SCHEMA_CHAR_SEPARATOR + RESPONSE + SCHEMA_EXTENSION


def getWSMethodSchemas(name):
    return getWSRequestMethodSchema(name), getWSResponseMethodSchema(name)


def getWSRequestMethodSchema(name):
    return WS_JSON_SCHEMA_FOLDER + name + SCHEMA_CHAR_SEPARATOR + REQUEST + SCHEMA_EXTENSION


def getWSResponseMethodSchema(name):
    return WS_JSON_SCHEMA_FOLDER + name + SCHEMA_CHAR_SEPARATOR + RESPONSE + SCHEMA_EXTENSION


def closeAddrBalanceTopic(topicName):

    addrTopicSplitted = topicName.split(topics.TOPIC_SEPARATOR)

    if len(addrTopicSplitted) <= 1:
        logger.printError(f"Topic name [{topicName}] not valid for Address Balance WS")
        raise rpcerrorhandler.InternalServerError(f"Can not unsubscribe {topicName} to node")

    id = random.randint(1, sys.maxsize)

    response = apirpc.notify(
        id,
        {
            ADDRESS: addrTopicSplitted[1],
            CALLBACK_ENDPOINT: ""
        }
    )

    if not response[SUCCESS]:
        logger.printError(f"Can not unsubscribe {topicName} to node")
        raise rpcerrorhandler.BadRequestError(f"Can not unsubscribe {topicName} to node")
