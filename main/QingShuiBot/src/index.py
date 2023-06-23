from khl import *

import Command
import KookRequest
from PublicFunction import *
import RunEvent as ret

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
            Log.infoLog("Bot Running")
            # noinspection PyBroadException
            try:
                # 指令部分
                @run_bot.command(name=command_cfg['help']['reg_name'])
                async def helps(msg: Message, *args):
                    await Command.Help.main(msg, args)

                @run_bot.command(name=command_cfg['main']['reg_name'])
                async def main(msg: Message, *args):
                    pass

                @run_bot.command(name=command_cfg['query_server']['reg_name'])
                async def query_server(msg: Message, *args):
                    await Command.QueryServer.main(msg, args)

                @run_bot.command(name=command_cfg['auth']['reg_name'])
                async def auth(msg: Message, *args):
                    pass

                # 事件部分
                @run_bot.on_event(EventTypes.JOINED_GUILD)
                async def join_guild(b: Bot, e: Event):
                    user_id = e.body['joined_at']
                    await ret.JoinGuild.AddUserUntrustedGrant.index(run_bot, user_id)

            except:
                Log.errorLog("Bot Error")
            run_bot.run()


if __name__ == '__main__':
    runningBot = QingShuiBot().BotRunning()
    runningBot.indexRunning()
