import json

import DataManipulation as dm
# 玩家房间类
from QS.QingShui.src import KookApiRequests


class PlayerRoom:  # 定义玩家房间类
    def __init__(self, bot):  # 创建基类
        self.bot = bot  # 获取传参
        self.channel_cfg = dm.Config.kook_server_cfg['channel']  # 获取频道配置文件
        self.send = KookApiRequests.Send(bot)  # 定义发送消息类
        self.channel_api = KookApiRequests.BasicObject.ChannelApi
        self.channel_user_api = KookApiRequests.BasicObject.ChannelUserApi
        self.user_api = KookApiRequests.BasicObject.UserApi
        self.message_api = KookApiRequests.BasicObject.MessageApi

    async def createTeamUpRoom(self, user_id: str, channel_id: str, down_var: dict):  # 创建创建组队房间函数
        down = await KookApiRequests.BasicObject.requests(self.bot,
                                                          self.channel_user_api.channel_user_get_joined_channel,
                                                          {"guild_id": dm.Config.kook_server_cfg['guild']['guild_id'],
                                                           "user_id": user_id})  # 获取用户所在语音频道信息
        post = await KookApiRequests.BasicObject.requests(self.bot,
                                                          self.user_api.user_view,
                                                          {"user_id": user_id})  # 发送请求
        channel_person_numbers = await KookApiRequests.BasicObject.requests(self.bot,
                                                                            self.channel_api.channel_user_list,
                                                                            {"channel_id": channel_id})  # 获取用户频道列表
        if down['items'][0]['id'] == "6770879098699231":  # 如果频道是组队频道
            user_name = post['username']  # 获取用户名
            identity = post['identify_num']  # 获取用户注册编号
            ret = await KookApiRequests.BasicObject.requests(self.bot, self.channel_api.channel_create,
                                                             {"guild_id": dm.Config.kook_server_cfg['guild']['guild_id'],
                                                              "parent_id": "8204985620621587",
                                                              "name": f"{user_name}#{identity}的开黑频道",
                                                              "voice_quality": "3",
                                                              "type": 2,
                                                              "limit_amount": 5})  # 创建频道
            await KookApiRequests.BasicObject.requests(self.bot, self.channel_api.channel_move_user,
                                                       {"target_id": ret['id'],
                                                        "user_ids[]": user_id})  # 移动用户
        else:  # 否则
            channel_id = down['items'][0]['id']  # 获取频道ID
            if channel_id in self.channel_cfg['voice_channel']['false_team_up_channel']:  # 如果ID在非组队频道中
                pass  # 放弃
            else:  # 否则
                if channel_id in down_var:  # 判断是否处于常变量
                    pass  # 放弃
                else:  # 否则
                    items = down['items'][0]  # 获取信息
                    inf = {'channel_information':
                               {'channel_id': items['id'],
                                'guild_id': items['guild_id'],
                                'limit_amount': items['limit_amount'],
                                'channel_name': items['name']}}  # 获取指定信息
                    card = [
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
                                        "content": "组队消息"
                                    }
                                },
                                {
                                    "type": "context",
                                    "elements": [
                                        {
                                            "type": "image",
                                            "src": f"{post['avatar']}"
                                        },
                                        {
                                            "type": "plain-text",
                                            "content": f"{post['username']}"
                                        }
                                    ]
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "kmarkdown",
                                        "content": "> 组队信息:\n人数:%s/%s" % (len(channel_person_numbers),
                                                                          inf['channel_information']['limit_amount'])
                                    }
                                }
                            ]
                        }
                    ]  # 设置卡片消息样式表
                    msg = await self.send.ChannelSendCard(card, "4481485386328544")  # 发送组队消息
                    return msg  # 返回消息数据

    async def updateTeamUpRoom(self, channel_id: str, user_id, team_up_text: dict, user_state: str):
        if len(team_up_text) == 0:  # 如果组队为空
            pass  # 放弃
        elif channel_id not in team_up_text:  # 如果频道不再组队里
            pass  # 放弃
        else:  # 否则
            if channel_id in team_up_text:
                if user_state == "JOIN":
                    player_list = await KookApiRequests.BasicObject.requests(self.bot,
                                                                             self.channel_api.channel_user_list,
                                                                             {"channel_id": channel_id})  # 获取用户列表
                    down = await KookApiRequests.BasicObject.requests(self.bot,
                                                                      self.channel_user_api.
                                                                      channel_user_get_joined_channel,
                                                                      {"guild_id": dm.Config.kook_server_cfg['guild'][
                                                                          'guild_id'],
                                                                       "user_id": user_id})  # 获取用户所在语音频道信息
                    post = await KookApiRequests.BasicObject.requests(self.bot,
                                                                      self.user_api.user_view,
                                                                      {"user_id": user_id})  # 发送请求
                    if len(down['items']) == 0:
                        pass
                    else:
                        items = down['items'][0]  # 获取信息
                        inf = {'channel_information':
                                   {'channel_id': items['id'],
                                    'guild_id': items['guild_id'],
                                    'limit_amount': items['limit_amount'],
                                    'channel_name': items['name']}}  # 获取指定信息
                        card = [
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
                                            "content": "组队消息"
                                        }
                                    },
                                    {
                                        "type": "context",
                                        "elements": [
                                            {
                                                "type": "image",
                                                "src": f"{post['avatar']}"
                                            },
                                            {
                                                "type": "plain-text",
                                                "content": f"{post['username']}"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "section",
                                        "text": {
                                            "type": "kmarkdown",
                                            "content": "> 组队信息:\n人数:%s/%s" % (len(player_list),
                                                                              inf['channel_information'][
                                                                                  'limit_amount'])
                                        }
                                    }
                                ]
                            }
                        ]  # 设置卡片消息样式表
                        await KookApiRequests.BasicObject.requests(self.bot,
                                                                   self.message_api.message_update,
                                                                   {"msg_id": team_up_text[channel_id]['id'],
                                                                    "content": json.dumps(card)})
                elif user_state == "EXIT":
                    post = await KookApiRequests.BasicObject.requests(self.bot,
                                                                      self.user_api.user_view,
                                                                      {"user_id": user_id})  # 发送请求
                    player_list = await KookApiRequests.BasicObject.requests(self.bot,
                                                                             self.channel_api.channel_user_list,
                                                                             {"channel_id": channel_id})  # 获取用户列表
                    channel_view = await KookApiRequests.BasicObject.requests(self.bot,
                                                                              self.channel_api.channel_view,
                                                                              {"target_id": channel_id})
                    card = [
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
                                        "content": "组队消息"
                                    }
                                },
                                {
                                    "type": "context",
                                    "elements": [
                                        {
                                            "type": "image",
                                            "src": f"{post['avatar']}"
                                        },
                                        {
                                            "type": "plain-text",
                                            "content": f"{post['username']}"
                                        }
                                    ]
                                },
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "kmarkdown",
                                        "content": "> 组队信息:\n人数:%s/%s" % (len(player_list),
                                                                          channel_view['limit_amount'])
                                    }
                                }
                            ]
                        }
                    ]  # 设置卡片消息样式表
                    await KookApiRequests.BasicObject.requests(self.bot,
                                                               self.message_api.message_update,
                                                               {"msg_id": team_up_text[channel_id]['id'],
                                                                "content": json.dumps(card)})
                else:
                    pass
            else:
                pass

    async def deleteTeamUpRoom(self, channel_id: str):  # 创建删除组队频道
        channel_person_numbers = await KookApiRequests.BasicObject.requests(self.bot,
                                                                            self.channel_api.channel_user_list,
                                                                            {"channel_id": channel_id})  # 获取用户频道列表
        if len(channel_person_numbers) == 0:  # 如果人数为0
            if channel_id in self.channel_cfg['voice_channel']['false_team_up_channel']:  # 如果在禁止组队频道
                pass  # 放弃
            else:  # 否则
                await KookApiRequests.BasicObject.requests(self.bot, self.channel_api.channel_delete,
                                                           {"channel_id": channel_id})  # 删除频道
        else:  # 否则
            pass  # 放弃
