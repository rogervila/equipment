from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Queue.AbstractQueue import AbstractQueue


class SQSQueue(AbstractQueue):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log
