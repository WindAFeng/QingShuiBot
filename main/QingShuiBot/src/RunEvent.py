import CardMessage as cm
import KookRequest
import PublicFunction as pf


class JoinGuild:
    class AddUserUntrustedGrant:
        cfg = pf.Config.config['Server']
        guild_cfg = cfg['Guild']
        channel_cfg = cfg['Channel']

        @classmethod
        async def index(cls, bot, user_id: str):
            kar = KookRequest.Requests
            await kar.requests(bot=bot, requests=kar.GuildRoleApi.guild_role_grant,
                               parameter={"guild_id": cls.guild_cfg['id'],
                                          "user_id": f"{user_id}",
                                          "role_id": 20161779})


class JoinChannel:
    class TeamUp:
        cfg = pf.Config.config['Server']
        guild_cfg = cfg['Guild']
        channel_cfg = cfg['Channel']

        @classmethod
        async def teamUpJudgment(cls, channel_id: str):
            if channel_id == cls.channel_cfg['voiceChannel']['create_room_channel_id']:
                return True
            else:
                return False

        @classmethod
        async def notPlayerRoom(cls, channel_id):
            if channel_id in cls.channel_cfg['voiceChannel']['non_shout_voice_channel_list']:
                return True
            else:
                return False

        @classmethod
        async def createRoom(cls, bot):
            kook = KookRequest.Requests
            req = await kook.requests(bot, kook.channelApi.channel_create,
                                      {"guild_id": cls.guild_cfg['id'],
                                       "name": "__----__",
                                       "parent_id": cls.channel_cfg['group']['teamUpGroup']['id'],
                                       "type": 2,
                                       "limit_amount": 8,
                                       "voice_quality": 2,
                                       })
            return req

        @classmethod
        async def updateRoom(cls, bot, channel_id: str, channel_name: str):
            kook = KookRequest.Requests
            await kook.requests(bot, kook.channelApi.channel_update,
                                {"channel_id": channel_id,
                                 "name": channel_name,
                                 "parent_id": cls.channel_cfg['group']['teamUpGroup']['id'],
                                 })

        @classmethod
        async def moveUser(cls, bot, user_id: str, target_id: str):
            kook = KookRequest.Requests
            await kook.requests(bot, kook.channelApi.channel_move_user,
                                {"target_id": target_id,
                                 "user_ids[]": user_id})

        @classmethod
        async def getJoinedChannel(cls, bot, user_id: str):
            kook = KookRequest.Requests
            kar = await kook.requests(bot, kook.channelUserApi.channel_user_get_joined_channel,
                                      {"guild_id": cls.guild_cfg['Guild']['id'],
                                       "user_id": user_id})
            return kar

        @classmethod
        async def getUserView(cls, bot, user_id: str):
            kook = KookRequest.Requests
            req = await kook.requests(bot, kook.userApi.user_view, {"user_id": user_id})
            return req

        @classmethod
        async def sendMessage(cls, bot, channel_id: str, player_number: int, leader_name: str):

            card_msg = cm.OtherCard.shoutOnCard(room_number=channel_id,
                                                player_number=player_number,
                                                leader=leader_name)
            send = KookRequest.Send
            msg = await send.sendMessage(bot=bot, messageObject=send.cardTo,
                                         content=card_msg,
                                         magic_id=cls.channel_cfg["textChannel"]['sendShoutCardChannel'])
            return msg

        @classmethod
        async def getGroupView(cls, bot, target_id: str):
            """
            :param bot: any
            :param target_id: str
            :return: kar: json
            """
            kook = KookRequest.Requests
            kar = await kook.requests(bot, kook.channelApi.channel_view,
                                      {"target_id": target_id})
            return kar

        @classmethod
        async def updateGroup(cls, bot, group_name: str):
            """
            更新分组
            :param bot: any
            :param group_name: str
            :return:
            """
            group_id: str = cls.channel_cfg['group']['teamUpGroup']['id']
            kook = KookRequest.Requests
            await kook.requests(bot, kook.channelApi.channel_update,
                                {"channel_id": group_id,
                                 "name": group_name})

        @classmethod
        async def index(cls, bot, user_id: str, channel_id: str):
            join_channel = await cls.teamUpJudgment(channel_id)
            if join_channel:  # 判断是否是组队频道
                create_room = await cls.createRoom(bot)
                news_room_name = pf.Processing.halfString(create_room['id'])
                await cls.updateRoom(bot, create_room['id'], news_room_name)
                user_view = await cls.getUserView(bot, user_id)
                await cls.moveUser(bot, user_id, create_room['id'])
                msg = await cls.sendMessage(bot, news_room_name, 1, user_view['username'])
                group_view = await cls.getGroupView(bot, cls.channel_cfg['group']['teamUpGroup']['id'])
                old_name = group_view['name']
                await cls.updateGroup(bot, f"开黑畅聊-当前开黑房间数：{int((old_name.split('：'))[1]) + 1}")
                return {"type": "create_room",
                        "data": {
                            "number": news_room_name,
                            "leader": user_view['username'],
                            "leader_id": user_id,
                            "channel_id": create_room['id'],
                            "msg_id": msg['msg_id']
                        }}
            else:  # 非组队频道
                return {"type": "none",
                        "msg_id": "none"}


class ExitChannel:
    class TeamUp:
        cfg = pf.Config.config['Server']
        guild_cfg = cfg['Guild']
        channel_cfg = cfg['Channel']

        @classmethod
        async def exitChannelJudgment(cls, channel_id: str):  # 判断是否是玩家频道
            if channel_id not in cls.channel_cfg['voiceChannel']['non_shout_voice_channel_list']:
                return True  # 是玩家频道
            else:
                return False  # 不是玩家频道

        @classmethod
        async def channelLeaderJudgment(cls, user_id, room):
            leader_id = room['leader_id']
            first_user_id = room['user_list'][0]['user_id']
            if leader_id == user_id == first_user_id:
                return True
            else:
                return False

        @classmethod
        async def deleteRoom(cls, bot, room):
            """
            删除频道
            :param bot: 机器人实例
            :param room: 房间数据
            :return:
            """
            kook = KookRequest.Requests
            await kook.requests(bot, kook.channelApi.channel_delete,
                                {"channel_id": room['channel_id']})

        @classmethod
        async def getGroupView(cls, bot, target_id: str):
            """
            :param bot: 机器人实例
            :param target_id: 目标ID
            :return: kar: 频道信息
            """
            kook = KookRequest.Requests
            kar = await kook.requests(bot, kook.channelApi.channel_view,
                                      {"target_id": target_id})
            return kar

        @classmethod
        async def updateGroup(cls, bot, group_name: str):
            """
            更新分组
            :param bot: any
            :param group_name: str
            :return:
            """
            group_id: str = cls.channel_cfg['group']['teamUpGroup']['id']
            kook = KookRequest.Requests
            await kook.requests(bot, kook.channelApi.channel_update,
                                {"channel_id": group_id,
                                 "name": group_name})

        @classmethod
        async def deleteMessage(cls, bot, msg_id: str):
            kook = KookRequest.Requests
            await kook.requests(bot, kook.messageApi.message_delete,
                                {"msg_id": msg_id})

        @classmethod
        async def updateMessage(cls, bot, msg_id: str, room_number: str,
                                player_number: int, leader: str):
            """
            更新卡片消息
            :param bot:
            :param msg_id:
            :param room_number:
            :param player_number:
            :param leader:
            :return:
            """
            card_msg = cm.OtherCard.shoutOnCard(room_number, player_number, leader)
            kook = KookRequest.Requests
            await kook.requests(bot, kook.messageApi.message_update,
                                {"msg_id": msg_id,
                                 "content": card_msg})

        @classmethod
        async def index(cls, bot, var, channel_id: str, user_id: str):
            player_room = await cls.exitChannelJudgment(channel_id)
            if player_room:
                room_number: str = pf.Processing.halfString(channel_id)
                room = var[room_number]
                if room['people'] - 1 == 0:
                    await cls.deleteRoom(bot, room)
                    group_view = await cls.getGroupView(bot, cls.channel_cfg['group']['teamUpGroup']['id'])
                    old_name = group_view['name']
                    await cls.updateGroup(bot, f"开黑畅聊-当前开黑房间数：{int((old_name.split('：'))[1]) - 1}")
                    msg_id = room['msg_id']
                    await cls.deleteMessage(bot, msg_id)
                    return {"type": "delete_room"}
                else:
                    leader_judgment = await cls.channelLeaderJudgment(user_id, room)
                    msg_id = room['msg_id']
                    if leader_judgment:
                        new_leader = {"leader": room['user_list'][1]['username'],
                                      "leader_id": room['user_list'][1]['user_id']}
                        await cls.updateMessage(bot, msg_id, room_number,
                                                room['number'] - 1, new_leader['leader'])
                        return {"type": "update_room",
                                "new_leader": True,
                                "leader_inf": new_leader}
                    else:
                        await cls.updateMessage(bot, msg_id, room_number,
                                                room['number'] - 1, room['leader_name'])
                        return {"type": "update_room",
                                "new_leader": False}
            else:
                return {"type": "none"}
