from khl import *

import Command
import KookRequest
from PublicFunction import *


class QingShuiBot:
    class Variable:
        pass

    class Constant:
        pass

    class IndexFunction:
        def __init__(self):
            self.__var = QingShuiBot.Variable
            self.__con = QingShuiBot.Constant

    class BotRunning:
        def __init__(self):
            self.__var = QingShuiBot.Variable
            self.__con = QingShuiBot.Constant
            self.cfg = Config
            self.send = KookRequest.Send

        def indexRunning(self):
            run_bot = Bot(token=self.cfg.config['Bot']['token'])
            command_cfg = self.cfg.config['Command']
            # noinspection PyBroadException
            try:
                @run_bot.command(name=command_cfg['help']['reg_name'])
                async def helps(msg: Message, *args):
                    await Command.Help.main(msg, args)

                @run_bot.command(name=command_cfg['main']['reg_name'])
                async def main(msg: Message, *args):
                    pass
            except:
                Log.errorLog("Bot Error")
            run_bot.run()


if __name__ == '__main__':
    runningBot = QingShuiBot().BotRunning()
    runningBot.indexRunning()
