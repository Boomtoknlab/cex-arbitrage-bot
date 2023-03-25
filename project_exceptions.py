class NoRouteFoundError(Exception):
    "No route found for this token"
    pass

class LiquidityOverflowError(Exception):
    "Amount input is higher than liquidity provided"
    pass

class InvalidTokenError(Exception):
    "invalid pair parameter: pair must be all seperated by an underscore i.e ``BTC_USDT``"
    pass