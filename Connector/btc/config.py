#!/usr/bin/python3
from json import JSONEncoder
from utils import utils


class Config:

    def __init__(self, coin, networkName):

        self._coin = coin
        self._networkName = networkName

        self._bitcoincoreProtocol = ""
        self._bitcoincoreHost = ""
        self._bitcoincorePort = 0
        self._bitcoincoreUser = ""
        self._bitcoincorePassword = ""
        self._bitcoincoreZmqProtocol = ""
        self._bitcoincoreZmqPort = 0
        self._electrumProtocol = ""
        self._electrumHost = ""
        self._electrumPort = 0
        self._electrumUser = ""
        self._electrumPassword = ""
        self._bitcoincoreCallbackProtocol = ""
        self._bitcoincoreCallbackHost = ""

    def loadConfig(self, config):

        defaultConfig, err = utils.loadDefaultPackageConf(self.coin)
        if err is not None:
            return False, err

        self.bitcoincoreProtocol = config["bitcoincoreProtocol"] if "bitcoincoreProtocol" in config \
            else defaultConfig["bitcoincoreProtocol"]
        self.bitcoincoreHost = config["bitcoincoreHost"] if "bitcoincoreHost" in config \
            else defaultConfig["bitcoincoreHost"]
        self.bitcoincorePort = config["bitcoincorePort"] if "bitcoincorePort" in config \
            else defaultConfig["bitcoincorePort"]
        self.bitcoincoreUser = config["bitcoincoreUser"] if "bitcoincoreUser" in config \
            else defaultConfig["bitcoincoreUser"]
        self.bitcoincorePassword = config["bitcoincorePassword"] if "bitcoincorePassword" in config \
            else defaultConfig["bitcoincorePassword"]
        self.bitcoincoreZmqProtocol = config["bitcoincoreZmqProtocol"] if "bitcoincoreZmqProtocol" in config \
            else defaultConfig["bitcoincoreZmqProtocol"]
        self.bitcoincoreZmqPort = config["bitcoincoreZmqPort"] if "bitcoincoreZmqPort" in config \
            else defaultConfig["bitcoincoreZmqPort"]
        self.electrumProtocol = config["electrumProtocol"] if "electrumProtocol" in config \
            else defaultConfig["electrumProtocol"]
        self.electrumHost = config["electrumHost"] if "electrumHost" in config else defaultConfig["electrumHost"]
        self.electrumPort = config["electrumPort"] if "electrumPort" in config else defaultConfig["electrumPort"]
        self.electrumUser = config["electrumUser"] if "electrumUser" in config else defaultConfig["electrumUser"]
        self.electrumPassword = config["electrumPassword"] if "electrumPassword" in config \
            else defaultConfig["electrumPassword"]
        self.bitcoincoreCallbackProtocol = config["bitcoincoreCallbackProtocol"] \
            if "bitcoincoreCallbackProtocol" in config \
            else defaultConfig["bitcoincoreCallbackProtocol"]
        self.bitcoincoreCallbackHost = config["bitcoincoreCallbackHost"] if "bitcoincoreCallbackHost" in config \
            else defaultConfig["bitcoincoreCallbackHost"]

        return True, None

    @property
    def coin(self):
        return self._coin

    @property
    def networkName(self):
        return self._networkName

    @networkName.setter
    def networkName(self, value):
        self._networkName = value

    @property
    def bitcoincoreProtocol(self):
        return self._bitcoincoreProtocol

    @bitcoincoreProtocol.setter
    def bitcoincoreProtocol(self, value):
        self._bitcoincoreProtocol = value

    @property
    def bitcoincoreHost(self):
        return self._bitcoincoreHost

    @bitcoincoreHost.setter
    def bitcoincoreHost(self, value):
        self._bitcoincoreHost = value

    @property
    def bitcoincorePort(self):
        return self._bitcoincorePort

    @bitcoincorePort.setter
    def bitcoincorePort(self, value):
        self._bitcoincorePort = value

    @property
    def bitcoincoreUser(self):
        return self._bitcoincoreUser

    @bitcoincoreUser.setter
    def bitcoincoreUser(self, value):
        self._bitcoincoreUser = value

    @property
    def bitcoincorePassword(self):
        return self._bitcoincorePassword

    @bitcoincorePassword.setter
    def bitcoincorePassword(self, value):
        self._bitcoincorePassword = value

    @property
    def bitcoincoreZmqProtocol(self):
        return self._bitcoincoreZmqProtocol

    @bitcoincoreZmqProtocol.setter
    def bitcoincoreZmqProtocol(self, value):
        self._bitcoincoreZmqProtocol = value

    @property
    def bitcoincoreZmqPort(self):
        return self._bitcoincoreZmqPort

    @bitcoincoreZmqPort.setter
    def bitcoincoreZmqPort(self, value):
        self._bitcoincoreZmqPort = value

    @property
    def electrumProtocol(self):
        return self._electrumProtocol

    @electrumProtocol.setter
    def electrumProtocol(self, value):
        self._electrumProtocol = value

    @property
    def electrumHost(self):
        return self._electrumHost

    @electrumHost.setter
    def electrumHost(self, value):
        self._electrumHost = value

    @property
    def electrumPort(self):
        return self._electrumPort

    @electrumPort.setter
    def electrumPort(self, value):
        self._electrumPort = value

    @property
    def electrumUser(self):
        return self._electrumUser

    @electrumUser.setter
    def electrumUser(self, value):
        self._electrumUser = value

    @property
    def electrumPassword(self):
        return self._electrumPassword

    @electrumPassword.setter
    def electrumPassword(self, value):
        self._electrumPassword = value

    @property
    def bitcoincoreCallbackProtocol(self):
        return self._bitcoincoreCallbackProtocol

    @bitcoincoreCallbackProtocol.setter
    def bitcoincoreCallbackProtocol(self, value):
        self._bitcoincoreCallbackProtocol = value

    @property
    def bitcoincoreCallbackHost(self):
        return self._bitcoincoreCallbackHost

    @bitcoincoreCallbackHost.setter
    def bitcoincoreCallbackHost(self, value):
        self._bitcoincoreCallbackHost = value

    @property
    def bitcoincoreRpcEndpoint(self):
        return f"{self.bitcoincoreProtocol}://" \
               f"{self.bitcoincoreUser}:{self.bitcoincorePassword}@" \
               f"{self.bitcoincoreHost}:{self.bitcoincorePort}"

    @property
    def electrumRpcEndpoint(self):
        return f"{self.electrumProtocol}://" \
               f"{self.electrumUser}:{self.electrumPassword}@" \
               f"{self.electrumHost}:{self.electrumPort}"

    @property
    def bitcoincoreZmqEndpoint(self):
        return f"{self.bitcoincoreZmqProtocol}://" \
               f"{self.bitcoincoreHost}:{self.bitcoincoreZmqPort}"

    @property
    def bitcoinAddressCallbackHost(self):
        return f"{self.bitcoincoreCallbackProtocol}://" \
               f"{self.bitcoincoreCallbackHost}:80"

    def jsonEncode(self):
        return ConfigEncoder().encode(self)


class ConfigEncoder(JSONEncoder):
    def encode(self, o):
        return {
            "bitcoincoreProtocol": o.bitcoincoreProtocol,
            "bitcoincoreHost": o.bitcoincoreHost,
            "bitcoincorePort": o.bitcoincorePort,
            "bitcoincoreUser": o.bitcoincoreUser,
            "bitcoincorePassword": o.bitcoincorePassword,
            "bitcoincoreZmqProtocol": o.bitcoincoreZmqProtocol,
            "bitcoincoreZmqPort": o.bitcoincoreZmqPort,
            "bitcoincoreCallbackProtocol": o.bitcoincoreCallbackProtocol,
            "bitcoincoreCallbackHost": o.bitcoincoreCallbackHost,
            "electrumProtocol": o.electrumProtocol,
            "electrumHost": o.electrumHost,
            "electrumPort": o.electrumPort,
            "electrumUser": o.electrumUser,
            "electrumPassword": o.electrumPassword
        }
