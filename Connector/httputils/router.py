#!/usr/bin/python
from aiohttp import web
import json
from logger import logger
from patterns import Singleton
from utils import utils
from . import error

currenciesHandler = {}


class Router(object, metaclass=Singleton.Singleton):

    def __init__(self):
        self._availableCoins = {}

    async def doRoute(self, request):

        coin = request.match_info["coin"]
        network = request.match_info["network"]
        method = request.match_info["method"]

        self.checkIsAvailableRoute(
            coin=coin,
            network=network
        )

        coinHandler = currenciesHandler[coin]

        response = await coinHandler.handleRequest(
            network=network,
            method=method,
            request=request
        )

        return web.Response(
            text=json.dumps(response)
        )

    async def doWsRoute(self, request):

        coin = request.match_info["coin"]
        network = request.match_info["network"]

        self.checkIsAvailableRoute(
            coin=coin,
            network=network
        )

        coinHandler = currenciesHandler[coin]
        return await coinHandler.handleWsRequest(
            network=network,
            request=request
        )

    async def handleCallback(self, request):

        coin = request.match_info["coin"]
        network = request.match_info["network"]
        callbackName = request.match_info["callbackName"]

        self.checkIsAvailableRoute(
            coin=coin,
            network=network
        )

        coinHandler = currenciesHandler[coin]
        response = await coinHandler.handleCallback(
            network=network,
            callbackName=callbackName,
            request=request
        )

        return web.Response(
            text=json.dumps(response)
        )

    def addCoin(self, coin, network, config):

        if not utils.isAvailableCurrency(coin):
            logger.printError(f"Currency {coin} is not supported")
            raise error.BadRequestError(f"Currency {coin} is not supported")

        if coin in self._availableCoins:
            if network in self._availableCoins[coin]:
                logger.printError(f"Can not add {network} network for {coin} because it is already added")
                return {
                    "success": False,
                    "message": f"Can not add {network} network for {coin} because it is already added"
                }

        if not utils.isAvailableNetworkForCurrency(coin, network):
            logger.printError(f"{network} network not supported for currency {coin}")
            return {
                "success": False,
                "message": f"{network} network not supported for currency {coin}"
            }

        coinHandler = currenciesHandler[coin]
        ok, err = coinHandler.addConfig(network=network, config=config)
        if not ok:
            return {
                "success": False,
                "message": err
            }

        self._availableCoins[coin] = {
            network: True
        }

        return {
            "success": True,
            "message": f"{network} network added for currency {coin}"
        }

    async def removeCoin(self, coin, network):

        if not utils.isAvailableCurrency(coin):
            logger.printError(f"Currency {coin} is not supported")
            raise error.BadRequestError(f"Currency {coin} is not supported")

        if coin not in self._availableCoins:
            logger.printError(f"Currency {coin} has not been previously added")
            return {
                "success": False,
                "message": f"Currency {coin} has not been previously added"
            }

        if network not in self._availableCoins[coin]:
            logger.printError(f"{network} network has not been previously added for currency {coin}")
            return {
                "success": False,
                "message": f"{network} network has not been previously added for currency {coin}"
            }

        logger.printInfo(f"Removing {network} network for currency {coin}")

        del self._availableCoins[coin][network]
        coinHandler = currenciesHandler[coin]
        ok, err = await coinHandler.removeConfig(network)

        return {
            "success": ok,
            "message": f"{network} network removed for currency {coin}" if ok else err
        }

    def getCoin(self, coin, network):

        if not utils.isAvailableCurrency(coin):
            logger.printError(f"Currency {coin} is not supported")
            raise error.BadRequestError(f"Currency {coin} is not supported")

        if coin not in self._availableCoins:
            logger.printError(f"Currency {coin} has not been previously added")
            return {
                "success": False,
                "message": f"Currency {coin} has not been previously added"
            }

        if network not in self._availableCoins[coin]:
            logger.printError(f"{network} network has not been previously added for currency {coin}")
            return {
                "success": False,
                "message": f"{network} network has not been previously added for currency {coin}"
            }

        logger.printInfo(f"Returning configuration for {network} network for currency {coin}")

        coinHandler = currenciesHandler[coin]
        config, err = coinHandler.getConfig(network)
        if err is not None:
            return {
                "success": False,
                "message": err
            }

        return {
            "success": True,
            "message": f"Config configuration for {network} network for currency {coin} retrieved successfully",
            "coin": coin,
            "network": network,
            "config": config
        }

    async def updateCoin(self, coin, network, config):

        if not utils.isAvailableCurrency(coin):
            logger.printError(f"Currency {coin} is not supported")
            raise error.BadRequestError(f"Currency {coin} is not supported")

        if coin not in self._availableCoins:
            logger.printError(f"Currency {coin} has not been previously added")
            return {
                "success": False,
                "message": f"Currency {coin} has not been previously added"
            }

        if network not in self._availableCoins[coin]:
            logger.printError(f"Network {network} has not been previously added for currency {coin}")
            return {
                "success": False,
                "message": f"Network {network} has not been previously added for currency {coin}"
            }

        logger.printInfo(f"Updating configuration for network {network} for currency {coin}")

        coinHandler = currenciesHandler[coin]
        ok, err = await coinHandler.updateConfig(network, config)

        return {
            "success": ok,
            "message": err if not ok else
            f"Configuration for {network} network for currency {coin} updated successfully"
        }

    def checkIsAvailableRoute(self, coin, network):

        if coin not in self._availableCoins:
            logger.printError(f"Currency {coin} has not been previously added")
            raise error.NotFoundError(f"Currency {coin} has not been previously added")

        if network not in self._availableCoins[coin]:
            logger.printError(f"{network} network for {coin} has not been previously added")
            raise error.NotFoundError(f"{network} network for {coin} has not been previously added")


class CurrencyHandler:

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, coin):

        def addConfig(network, config):
            pass

        def getConfig(network):
            pass

        def removeConfig(network):
            pass

        def updateConfig(network, config):
            pass

        async def handleRequest(network, method, request):
            pass

        async def handleWsRequest(network, request):
            pass

        def handleCallback(network, callbackName, request):
            pass

        self.handler.addConfig = addConfig \
            if not hasattr(self.handler, "addConfig") or not callable(self.handler.addConfig) \
            else self.handler.addConfig

        self.handler.getConfig = getConfig \
            if not hasattr(self.handler, "getConfig") or not callable(self.handler.getConfig) \
            else self.handler.getConfig

        self.handler.removeConfig = removeConfig \
            if not hasattr(self.handler, "removeConfig") or not callable(self.handler.removeConfig) \
            else self.handler.removeConfig

        self.handler.updateConfig = updateConfig \
            if not hasattr(self.handler, "updateConfig") or not callable(self.handler.updateConfig) \
            else self.handler.updateConfig

        self.handler.handleRequest = handleRequest \
            if not hasattr(self.handler, "handleRequest") or not callable(self.handler.handleRequest) \
            else self.handler.handleRequest

        self.handler.handleWsRequest = handleWsRequest \
            if not hasattr(self.handler, "handleRequest") or not callable(self.handler.handleWsRequest) \
            else self.handler.handleWsRequest

        self.handler.handleCallback = handleCallback \
            if not hasattr(self.handler, "handleCallback") or not callable(self.handler.handleCallback) \
            else self.handler.handleCallback

        obj = self.handler(coin)
        currenciesHandler[coin] = obj

        return obj
