import DataManipulation as dm
import EventObject as eo
import KookApiRequests as kar


# Help指令类
class HelpCard:  # 创建help指令使用类
    def __init__(self, msg, args):  # 创建基类
        self.msg = msg
        self.args = args

    @staticmethod
    async def turnCommandHelp(command_dict: dict, book_number: int) -> list:  # 创建指令数据获取函数
        all_list: list = []  # 定义列表
        for pointer in command_dict:  # 循环遍历字典传参
            all_list.append(command_dict[pointer])  # 将信息传递进列表
        start: int = book_number * 5 - 5  # 设置初始值
        end: int = book_number * 5  # 设置结束值
        lang: int = len(all_list)  # 获取列表长度（元素数量）
        end_list: list = []  # 设置返回列表
        if lang < end:  # 判断数量
            for pointer_low in range(start, lang):  # 数量少就循环遍历添加数据
                end_list.append(all_list[pointer_low])  # 添加数据
        else:  # 否则
            for pointer_more in range(start, end):  # 循环遍历添加指定数据
                end_list.append(all_list[pointer_more])  # 添加数据
        return end_list  # 返回数据

    async def reducedInstruction(self, command_dict: dict, book_number: int) -> list:  # 创建简化指令函数
        get_list_command = await self.turnCommandHelp(command_dict, book_number)  # 获取返回值
        return_list: list = []  # 定义返回列表
        for pointer in get_list_command:  # 指针遍历列表
            return_list.append([pointer['name'], pointer['parameter'], pointer['context']])  # 获取信息并添加至返回列表
        return return_list  # 返回数据

    async def toString(self, book_number: int, command_dict: dict) -> str:  # 创建命令转化为字符串函数
        get_list_command = await self.reducedInstruction(command_dict, book_number)  # 获取函数返回值
        end_string: str = ""  # 定义返回字符串
        for pointer in get_list_command:  # 指针循环遍历
            end_string += f"> **{pointer[2]}**\n`{pointer[0]} {pointer[1]}`\n"  # 返回字符串添加数据
        return end_string  # 返回字符串

    async def main(self):
        inf = await kar.MessageInformation(self.msg).messageInformation()  # 读取信息
        send = kar.Send(None, self.msg)  # 设置发送消息功能
        pmr = dm.Parameter(self.args).indexParameter()  # 定义参数方法
        if pmr['length'] > 1:  # 判断参数长度
            await dm.ErrorParameter(self.msg).parameterErrorPrompt()  # 发出警告
        else:  # 否则
            if pmr['length'] == 0:  # 如果长度为0
                pmr['args'].append(1)  # 添加一项数据
            helps_commands: str = await self.toString(int(pmr['args'][0]), dm.Config.command_cfg)  # 设置文本
            prompt = [
                {
                    "type": "card",
                    "theme": "secondary",
                    "size": "lg",
                    "color": "#4169E1",
                    "modules": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain-text",
                                "content": f"| 获取帮助 | - {int(pmr['args'][0])}"
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "kmarkdown",
                                "content": f"{helps_commands}"
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "plain-text",
                                    "content": "-由清云工作室强力支持"
                                }
                            ]
                        }
                    ]
                }
            ]  # 设置卡片消息样式
            await send.SendCard(prompt, False, inf['user_id'])  # 发送消息


# MainCard类
class MainCard:  # 创建经验值类
    def __init__(self, args, msg):  # 设置基类
        self.experience_dict: dict = dm.Config.exp_cfg  # 获取
        self.args = args
        self.msg = msg

    # 转换经验值
    async def conversionLevel(self, experience: int) -> dict:  # 创建判定方法
        exp_str: str = 'level-'  # 设置读取方式
        ret_dict: dict = {}  # 创建空字典方便读取
        for i in range(1, len(self.experience_dict)):  # 循环遍历配置文件中经验值数值
            l_exp = self.experience_dict[exp_str + f'{i - 1}']  # 获取上一个经验值数据
            r_exp = self.experience_dict[exp_str + f'{i}']  # 获取当前经验值数据
            l_level = i - 1  # 赋值给上一个等级
            r_level = i  # 赋值给当前等级
            if l_exp < experience <= r_exp:  # 判断经验值是否大于上一个经验值且小于等于下一个经验值
                ret_dict['exp'] = experience  # 给返回字典添加数据
                ret_dict['level'] = r_level  # 给返回字典添加数据
            elif experience == l_exp:  # 判断经验值是否等于上一个经验值
                ret_dict['exp'] = experience  # 给返回字典添加数据
                ret_dict['level'] = l_level  # 给返回字典添加数据
        if ret_dict == {}:  # 判断是否出现问题
            return {"exp": "Error", "level": "Error"}  # 发生错误返回错误
        else:  # 否则
            return ret_dict  # 返回等级以及经验值

    async def main(self):  # 设置主函数
        inf = await kar.MessageInformation(self.msg).messageInformation()  # 获取消息信息
        pmr = dm.Parameter(self.args).indexParameter()  # 获取参数信息
        if pmr['length'] > 0:  # 判断参数长度
            await dm.ErrorParameter(self.msg).parameterErrorPrompt()  # 参数建议
        else:  # 否则
            card_context = [
                {
                    "type": "card",
                    "theme": "secondary",
                    "size": "lg",
                    "color": "#6495ED",
                    "modules": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain-text",
                                "content": "清风游戏社区"
                            }
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "plain-text",
                                    "content": "当前用户:"
                                },
                                {
                                    "type": "image",
                                    "src": f"{inf['user_avatar']}"
                                },
                                {
                                    "type": "plain-text",
                                    "content": f"{inf['user_name']}#{inf['identity_group']}"
                                }
                            ]
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "paragraph",
                                "cols": 2,
                                "fields": [
                                    {
                                        "type": "kmarkdown",
                                        "content": f"**当前等级:**12"
                                    },
                                    {
                                        "type": "kmarkdown",
                                        "content": f"**经验值:**10/12"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "paragraph",
                                "cols": 2,
                                "fields": [
                                    {
                                        "type": "kmarkdown",
                                        "content": f"**积分:**10"
                                    },
                                    {
                                        "type": "kmarkdown",
                                        "content": f"**清云账号:**已绑定"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "plain-text",
                                    "content": "日常功能"
                                }
                            ]
                        },
                        {
                            "type": "action-group",
                            "elements": [
                                {
                                    "type": "button",
                                    "theme": "primary",
                                    "value": "签到",
                                    "text": {
                                        "type": "plain-text",
                                        "content": "签到"
                                    }
                                },
                                {
                                    "type": "button",
                                    "theme": "primary",
                                    "value": "前往官网",
                                    "text": {
                                        "type": "plain-text",
                                        "content": "前往官网"
                                    }
                                },
                                {
                                    "type": "button",
                                    "theme": "primary",
                                    "value": "绑定清云账号",
                                    "text": {
                                        "type": "plain-text",
                                        "content": "绑定清云账号"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]  # 设置卡片消息
            await kar.Send(None, self.msg).SendCard(card_context, True, inf['user_id'])  # 发送消息


class Shout:  # 定义喊话类
    def __init__(self, args: tuple, bot, msg):  # 定义类参数
        self.args = args  # 定义参数
        self.bot = bot  # 定义参数
        self.msg = msg  # 定义参数

    async def getCanSaysChannel(self) -> list:  # 定义类方法获取可以发送信息的频道
        msg_information = await kar.MessageInformation(self.msg).messageInformation()  # 获取消息信息
        all_channel = await kar.BasicObject.requests(self.bot,
                                                     kar.BasicObject.ChannelApi.channel_list,
                                                     {"guild_id": msg_information['guild_id'],
                                                      "type": 1})  # 发送频道列表请求
        guild_cfg = dm.Config.kook_server_cfg  # 获取配置文件
        stop_server_say = guild_cfg['guild']['stop_server_say']  # 获取禁言频道
        stop_list: list = []  # 定义空列表用来获取不可说话频道
        can_speak_channel: list = []  # 定义可说话频道
        for chn in stop_server_say:  # 循环遍历不可说话频道
            stop_list.append(chn['id'])  # 添加数据
        for into in all_channel['items']:  # 循环遍历所有频道
            if into['id'] in stop_list:  # 判断是否能说话
                pass  # 放弃
            else:  # 否则
                can_speak_channel.append(into['id'])  # 添加数据
        return can_speak_channel  # 返回列表

    async def shoutInformation(self) -> dict:  # 定义类方法用于获取参数信息
        inf = await kar.MessageInformation(self.msg).messageInformation()  # 获取消息信息
        arg = dm.Parameter(self.args).indexParameter()  # 获取参数信息
        if arg['length'] > 1:  # 判断参数长度
            await dm.ErrorParameter(self.msg).parameterErrorPrompt()  # 参数建议
        else:  # 否则
            if arg['length'] == 0:  # 如果参数为空
                arg['args'].append('来这里找我')  # 添加一条数据
            return {'username': inf['user_name'],
                    'text': arg['args'][0],
                    'avatar': inf['user_avatar'],
                    'channel_id': inf['channel_id']}  # 返回数据内容

    async def sendMessage(self, inf: dict, channel_id: str) -> None:  # 定义发送信息方法
        shout_card = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "color": "#6495ED",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "全服喊话"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain-text",
                                "content": f"{inf['username']}:"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": f"**{inf['text']}**"
                        },
                        "mode": "left",
                        "accessory": {
                            "type": "image",
                            "src": f"{inf['avatar']}",
                            "size": "lg"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "kmarkdown",
                                "content": f"(chn){inf['channel_id']}(chn)"
                            }
                        ]
                    }
                ]
            }
        ]  # 定义卡片消息样式
        await kar.Send(self.bot).ChannelSendCard(shout_card, channel_id)  # 发送卡片消息

    async def main(self):  # 定义主方法
        channel_id_list: list = await self.getCanSaysChannel()  # 获取频道信息
        information = await self.shoutInformation()  # 获取参数信息
        for it in channel_id_list:  # 循环遍历频道
            await self.sendMessage(information, it)  # 发送消息


class Gbind:  # 定义绑定类
    def __init__(self, args: tuple, msg, bot):  # 定义传参
        self.args = args  # 定义参数
        self.msg = msg  # 定义参数
        self.bot = bot  # 定义参数

    async def errorServerId(self):  # 反馈错误的服务器ID
        args = dm.Parameter(self.args).indexParameter()  # 格式化参数
        error_id = args['args'][0]  # 获取服务器ID
        user_id = (await kar.MessageInformation(self.msg).messageInformation())['user_id']  # 获取用户信息
        error_card = [
            {
                "type": "card",
                "theme": "none",
                "size": "lg",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "绑定失败"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain-text",
                                "content": f"{error_id}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": "**服务器ID并不存在**"
                        }
                    }
                ]
            }
        ]  # 设置卡片样式
        await kar.Send(self.bot, self.msg).SendCard(error_card, True, user_id)  # 发送消息

    async def parameterAnalysis(self):  # 判定函数
        args = dm.Parameter(self.args).indexParameter()  # 初始化函数
        if args['length'] != 2:  # 判定长度
            await dm.ErrorParameter(self.msg).parameterErrorPrompt()  # 发送错误
        else:  # 否则
            server_id_cfg = dm.Config.game_server_cfg
            if args['args'][0] in server_id_cfg:
                await self.requestsApi()
            else:
                await self.errorServerId()

    async def requestsApi(self):  # 请求函数
        args = dm.Parameter(self.args).indexParameter()  # 初始化参数
        api = dm.Config.game_server_cfg  # 获取配置文件内API
        will_req_api = api[args['args'][0]]  # 获取链接
        # 以下是请求代码

    async def main(self):  # 运行主函数
        await self.parameterAnalysis()  # 运行


class VoiceSet:  # 设置语音房间
    def __init__(self, args: tuple, msg, bot, team_up_text: dict):  # 定义传参
        self.args = args  # 定义参数
        self.msg = msg  # 定义参数
        self.bot = bot  # 定义参数
        self.team_up_dict = team_up_text

    async def analysisParameter(self) -> int:  # 配置玩家参数
        args = dm.Parameter(self.args).indexParameter()  # 初始化参数
        if args['length'] != 1:  # 获取长度
            await dm.ErrorParameter(self.msg).parameterErrorPrompt()  # 如果出错
            return 5  # 返回5
        else:  # 否则
            if 0 < int(args['args'][0]) < 99:
                return args['args'][0]  # 返回数据
            else:
                await dm.ErrorParameter(self.msg).parameterErrorPrompt()  # 如果出错
                return 5  # 返回5

    async def requestsKook(self):  # 请求KOOK
        msg_inf = await kar.MessageInformation(self.msg).messageInformation()  # 获取消息信息
        max_number = (await self.analysisParameter())  # 获取最大人数
        channel_id = (await kar.BasicObject.requests(self.bot,
                                                     kar.BasicObject.ChannelUserApi.channel_user_get_joined_channel,
                                                     {'guild_id': dm.Config.kook_server_cfg['guild']['guild_id'],
                                                      'user_id': msg_inf['user_id']}))['items'][0]['id']  # 获取频道人数
        await kar.BasicObject().requests(self.bot, kar.BasicObject.ChannelApi.channel_update,
                                         {'channel_id': channel_id,
                                          "limit_amount": max_number})  # 更新频道
        await kar.Send(self.bot, self.msg). \
            SendText(f'(met){msg_inf["user_id"]}(met) 语音房间人数已经设置为{max_number}',
                     True, msg_inf['user_id'])  # 发送消息
        event = eo.PlayerRoom(self.bot)
        await event.updateTeamUpRoom(channel_id, msg_inf['user_id'], self.team_up_dict, "JOIN")

    async def main(self):  # 设定主函数
        await self.requestsKook()  # 运行
