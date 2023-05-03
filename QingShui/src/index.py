import json
import time  # 调用时间模块

import psutil
from khl import *  # 调用khl.py所有内容

import CommandObject
import DataManipulation as dm
import KookApiRequests
# 前置工作
from QS.QingShui.src import EventObject

dm.Config.reloadConfig()


# 创建主类Robot
class Robot:  # 创建主类Robot
    class Constant:  # 设置常量类
        coldPlayerMinute: int = 120  # 设置冷却常量(单位:秒)
        sysShow: str = '■'
        sysOther: str = '_'

    class Variable:  # 设置常变量类
        hhColdPlayerDict: dict = {}  # 设置冷却人员字典
        teamUpText: dict = {}  # 组队消息
        sysRunningMessageId: dict = {}

    class EventFunction:  # 设置用于KOOK事件的功能函数
        def __init__(self):  # 设置基类
            self.__constant = Robot.Constant  # 设置常量读取
            self.__variable = Robot.Variable  # 设置变量读取
            self.log = dm.Logging

        async def coldUser(self):  # 设置冷却功能
            if len(self.__variable.hhColdPlayerDict) == 0:  # 判断常变量冷却人员字典是否为空
                pass  # 忽略
            else:  # 否则
                for one in list(self.__variable.hhColdPlayerDict):  # 循环遍历列表化字典
                    value = self.__variable.hhColdPlayerDict[one]  # 获取信息
                    if value['data_time'] + self.__constant.coldPlayerMinute == int(time.time()):  # 判断用户冷却时间是否终止
                        del self.__variable.hhColdPlayerDict[one]  # 删除用户冷却缓存
                    else:  # 否则
                        continue  # 开启下一轮循环

        async def addTeamUpVoiceChannel(self, channel_id: str, message_dict):  # 定义添加组队频道常变量方法
            if message_dict is None:  # 判断消息无返回
                pass  # 放弃
            else:  # 否则
                if channel_id in self.__variable.teamUpText:  # 判断频道是否已经处于常变量
                    pass  # 放弃
                else:  # 否则
                    self.__variable.teamUpText[channel_id] = {"id": message_dict['msg_id']}  # 添加数据

        async def deleteTeamUpVoiceChannel(self, channel_id: str, running_to_bot):  # 定义删除组队频道常变量方法
            if channel_id in self.__variable.teamUpText:  # 判断频道是否已经处于常变量
                voice = KookApiRequests.BasicObject.ChannelApi  # 定义频道数据
                user_list = await KookApiRequests.BasicObject.requests(running_to_bot,
                                                                       voice.channel_user_list,
                                                                       {"channel_id": channel_id})  # 获取用户频道列表
                if len(user_list) == 0:  # 判断用户列表用户数量
                    messages = KookApiRequests.BasicObject.MessageApi  # 获取MessageApi
                    await KookApiRequests.BasicObject.requests(running_to_bot, messages.message_delete,
                                                               {"msg_id": self.__variable.teamUpText[channel_id][
                                                                   'id']})  # 参数KOOK消息
                    del self.__variable.teamUpText[channel_id]  # 删除常变量数据
                else:  # 否则
                    pass  # 放弃
            else:  # 否则
                pass  # 放弃

        async def sysLoad(self, running_to_bot):
            memory = int(psutil.virtual_memory().percent)  # 获取内存比率
            cpu = int(psutil.cpu_percent())  # 获取cpu比率
            system_list = [[memory // 10, 10 - memory // 10], [cpu // 10, 10 - cpu // 10]]  # 计算内存和cpu显示数
            cpu_show = f"[{system_list[1][0] * self.__constant.sysShow}" \
                       f"{system_list[1][1] * self.__constant.sysOther}]  {cpu}%"  # 设定输出样式
            memory_show = f"[{system_list[0][0] * self.__constant.sysShow}" \
                          f"{system_list[0][1] * self.__constant.sysOther}]" \
                          f"  {memory}%"  # 设定输出样式
            card_context = [
                {
                    "type": "card",
                    "theme": "none",
                    "size": "lg",
                    "modules": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain-text",
                                "content": "机器人负载"
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "kmarkdown",
                                "content": f"> CPU {cpu_show} \n 内存 {memory_show}"
                            }
                        }
                    ]
                }
            ]  # 卡片样式
            if len(self.__variable.sysRunningMessageId) == 0:  # 判断是否发送过卡片
                send_to = await KookApiRequests.Send(running_to_bot).ChannelSendCard(card_context,
                                                                                     dm.Config.kook_server_cfg[
                                                                                         'channel']
                                                                                     ['text_channel']
                                                                                     ['robot_system_load'])  # 发送卡片
                self.__variable.sysRunningMessageId['msg_id'] = send_to['msg_id']  # 添加数据
            else:  # 否则
                if memory > 90:  # 如果内存爆炸就发送警告
                    self.log.warnLog('High memory usage')  # 发送警告
                if cpu > 90:  # 如果cpu爆炸就发送警告
                    self.log.warnLog('High CPU usage')  # 发送警告
                messages = KookApiRequests.BasicObject.MessageApi  # 获取messageApi的数据
                await KookApiRequests.BasicObject.requests(running_to_bot, messages.message_update,
                                                           {"msg_id": self.__variable.sysRunningMessageId['msg_id'],
                                                            "content": json.dumps(card_context)})  # 更新消息

    def __init__(self):  # 设置基类
        self.token = dm.Config.bot_cfg['token']  # 读取机器人token
        self.command = dm.Config.command_cfg  # 读取机器人指令配置文件
        self.eventFunction = Robot.EventFunction()  # 链接运行事件
        self.log = dm.Logging  # 定义日志模块
        self.cmd = CommandObject  # 定义指令基类

    def botRunning(self):  # 设置机器人运行总函数
        self.log.infoLog('Bot Running')  # 打印运行通知
        run_bot = Bot(self.token)  # 设置机器人
        # noinspection PyBroadException
        try:
            # 指令
            # 帮助指令
            @run_bot.command(name=self.command['help']['register_command'])  # 创建指令
            async def helpCard(msg: Message, *args):  # 定义异步函数并设置参数
                await self.cmd.HelpCard(args=args, msg=msg).main()

            @run_bot.command(name=self.command['mainCard']['register_command'])  # 创建主菜单指令
            async def mainCard(msg: Message, *args):  # 创建主菜单异步函数
                await self.cmd.MainCard(args, msg).main()

            @run_bot.command(name=self.command['shout']['register_command'])
            async def shout(msg: Message, *args):
                await self.cmd.Shout(args, run_bot, msg).main()

            @run_bot.command(name=self.command['serverBind']['register_command'])
            async def serverBind(msg: Message, *args):
                await self.cmd.Gbind(args, msg, run_bot).main()

            @run_bot.command(name=self.command['voiceSet']['register_command'])
            async def voiceSet(msg: Message, *args):
                await self.cmd.VoiceSet(args, msg, run_bot, self.Variable.teamUpText).main()

            @run_bot.command(name='cs')
            async def cs(msg: Message):
                msg_information = await KookApiRequests.MessageInformation(msg).messageInformation()  # 获取消息信息
                all_channel = await KookApiRequests.BasicObject.requests(run_bot,
                                                                         KookApiRequests.BasicObject.ChannelApi.
                                                                         channel_list,
                                                                         {"guild_id": msg_information['guild_id'],
                                                                          "type": 1})
                for into in all_channel['items']:
                    print(into)

            # 事件
            # 创建每秒定时任务
            @run_bot.task.add_interval(seconds=1, timezone="Asia/Shanghai")
            async def secondTask():  # 定义秒时间函数
                await self.eventFunction.coldUser()  # 调用事件类的冷却函数

            @run_bot.task.add_interval(minutes=1, timezone="Asia/Shanghai")
            async def minuteTask():  # 定义分钟时间函数
                await self.eventFunction.sysLoad(run_bot)

            # 创建每天定时任务
            @run_bot.task.add_cron(hour=0)  # 定义每天时间函数
            async def dayTask():  # 定义每日任务
                pass

            # 加入语音频道事件
            @run_bot.on_event(EventTypes.JOINED_CHANNEL)  # 加入语音频道事件
            async def joinChannel(b: Bot, e: Event):  # 创建异步方法
                channel_id = e.body['channel_id']  # 获取频道ID
                user_id = e.body['user_id']  # 获取用户ID
                player_room = EventObject.PlayerRoom(run_bot)  # 实例化玩家房间类
                send_msg = await player_room.createTeamUpRoom(user_id, channel_id,
                                                              down_var=self.Variable.teamUpText)  # 使用创建房间函数
                await self.EventFunction().addTeamUpVoiceChannel(channel_id=channel_id,
                                                                 message_dict=send_msg)  # 创建组队消息常变量
                await player_room.updateTeamUpRoom(channel_id, user_id, self.Variable.teamUpText, "JOIN")  # 更新房间信息

            # 退出语音频道事件
            @run_bot.on_event(EventTypes.EXITED_CHANNEL)
            async def ExitChannel(b: Bot, e: Event):
                user_id = e.body['user_id']  # 获取用户ID
                channel_id = e.body['channel_id']  # 获取频道ID
                player_room = EventObject.PlayerRoom(run_bot)  # 实例化玩家房间类
                await self.EventFunction().deleteTeamUpVoiceChannel(channel_id=channel_id,
                                                                    running_to_bot=b)  # 删除组队消息常变量
                await player_room.deleteTeamUpRoom(channel_id)  # 删除频道
                await player_room.updateTeamUpRoom(channel_id, user_id, self.Variable.teamUpText, "EXIT")  # 更新房间信息

            run_bot.run()  # 运行机器人

        except:
            self.log.errorLog('机器人异常')


run = Robot()  # 实例化类
run.botRunning()  # 运行机器人
