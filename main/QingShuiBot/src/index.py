from khl import *

import Command
import KookRequest
import RunEvent
import RunEvent as ret
from PublicFunction import *


class QingShuiBot:
    class Variable:
        roomList: dict = {}

    class Constant:
        pass

    class EventFunction:
        class PublicFunction:
            @classmethod
            async def addCold(cls, insert_dict, msg, cold_time):
                data = await KookRequest.MessageInformation.messageInformation(msg=msg)
                if data.user_id in list(insert_dict):
                    pass
                else:
                    on_time = int(time.time())
                    end_time = on_time + cold_time
                    insert_dict[data.user_id] = [end_time]

            @classmethod
            async def deleteCold(cls, cold_list: list):
                on_time = int(time.time())
                for pt in cold_list:
                    if len(list(pt)) == 0:
                        pass
                    else:
                        key: str = list(pt)[0]
                        if pt[key][0] == on_time:
                            del pt[key]
                        else:
                            pass

        class JoinChannel:
            class TeamUp:
                class AddRoom:
                    @classmethod
                    async def dataJudgment(cls, event_data: dict):
                        if event_data['type'] == "create_room":
                            return True
                        else:
                            return False

                    @classmethod
                    async def index(cls, event_data):
                        data = await cls.dataJudgment(event_data)
                        if data:
                            var = QingShuiBot.Variable.roomList
                            var[event_data['data']['number']] = {
                                "people": 0,
                                "user_list": [
                                    {
                                        "username": event_data['data']['leader'],
                                        "user_id": event_data['data']['leader_id'],
                                    }
                                ],
                                "leader_name": event_data['data']['leader'],
                                "leader_id": event_data['data']['leader_id'],
                                "msg_id": event_data['data']['msg_id'],
                                "channel_id": event_data['data']['channel_id']
                            }

                class UpdateRoom:
                    @classmethod
                    async def joinChannelJudgment(cls, channel_id: str):
                        room_number: str = Processing.halfString(channel_id)
                        var = QingShuiBot.Variable.roomList
                        if room_number in var:
                            return True
                        else:
                            return False

                    @classmethod
                    async def getUserView(cls, run_bot, user_id):
                        kook = KookRequest.Requests
                        req = await kook.requests(run_bot, kook.userApi.user_view,
                                                  {"user_id": user_id})
                        return req

                    @classmethod
                    async def index(cls, run_bot, channel_id: str, user_id: str):
                        join_channel = await cls.joinChannelJudgment(channel_id)
                        if join_channel:
                            room_number: str = Processing.halfString(channel_id)
                            var = QingShuiBot.Variable.roomList
                            user_view = await cls.getUserView(run_bot, user_id)
                            var[room_number]['people'] = var[room_number]['people'] + 1
                            if {"username": user_view['username'], "user_id": user_id} not in \
                                    var[room_number]['user_list']:
                                var[room_number]['user_list'].append({"username": user_view['username'],
                                                                      "user_id": user_id})

        class ExitChannel:
            class TeamUp:
                class DeleteRoom:
                    @classmethod
                    async def exitChannelJudgment(cls, channel_id: str):
                        room_number = Processing.halfString(channel_id)
                        var = QingShuiBot.Variable.roomList
                        if room_number in var:
                            return True
                        else:
                            return False

                    @classmethod
                    async def index(cls, channel_id: str, data):
                        exit_channel = await cls.exitChannelJudgment(channel_id)
                        var = QingShuiBot.Variable.roomList
                        room_number: str = Processing.halfString(channel_id)
                        if exit_channel:
                            if data['type'] != 'none':
                                if data['type'] == 'delete_room':
                                    del var[room_number]
                                elif data['type'] == 'update_room':
                                    if data['new_leader']:
                                        var['people'] = var['people'] - 1
                                        var['user_list'].pop(0)
                                        var['leader_name'] = var['user_list'][0]['username']
                                        var['leader_id'] = var['user_list'][0]['user_id']
                                    else:
                                        var['people'] = var['people'] - 1
                            else:
                                pass
                        else:
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
            self.func = QingShuiBot.EventFunction

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

                @run_bot.command(name=command_cfg['hypixel']['reg_name'])
                async def hypixel(msg: Message, *args):
                    kok = KookRequest.Requests
                    await kok.requests(run_bot, kok.userApi.user_offline)

                @run_bot.command(name=command_cfg['auth']['reg_name'])
                async def auth(msg: Message, *args):
                    send = KookRequest.Requests
                    await send.requests(run_bot, send.guildRoleApi.guild_role_grant,
                                        {"guild_id": "8329917220869199",
                                         "user_id": "1626878697",
                                         "role_id": 10146913})

                # 事件部分
                @run_bot.on_event(EventTypes.JOINED_GUILD)
                async def join_guild(b: Bot, e: Event):
                    user_id = e.body['joined_at']
                    await ret.JoinGuild.AddUserUntrustedGrant.index(run_bot, user_id)

                @run_bot.on_event(EventTypes.JOINED_CHANNEL)
                async def join_channel(b: Bot, e: Event):
                    user_id = e.body['user_id']
                    channel_id = e.body['channel_id']
                    inf = await RunEvent.JoinChannel.TeamUp. \
                        index(run_bot, user_id, channel_id)
                    await self.func.JoinChannel.TeamUp.AddRoom.index(inf)
                    await self.func.JoinChannel.TeamUp.UpdateRoom.index(run_bot, channel_id, user_id)

                @run_bot.on_event(EventTypes.EXITED_CHANNEL)
                async def exited_channel(b: Bot, e: Event):
                    user_id = e.body['user_id']
                    channel_id = e.body['channel_id']
                    inf = await RunEvent.ExitChannel.TeamUp.index(run_bot, self.__var.roomList,
                                                                  channel_id, user_id)
                    await self.func.ExitChannel.TeamUp.DeleteRoom.index(channel_id, inf)

                # 定时任务
                @run_bot.task.add_cron(second=1, timezone="Asia/Shanghai")
                async def secondFunction():
                    pass
            except:
                Log.errorLog("Bot Error")
            run_bot.run()


if __name__ == '__main__':
    runningBot = QingShuiBot().BotRunning()
    runningBot.indexRunning()
