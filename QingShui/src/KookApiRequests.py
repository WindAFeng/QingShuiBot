from khl import MessageTypes


class BasicObject(object):
    class GuildApi:  # 服务器相关接口列表
        guild_list: list[str, str] = ["guild/list", "GET"]
        guild_view: list[str, str] = ["guild/view", "GET"]
        guild_user_list: list[str, str] = ["guild/user-list", "GET"]
        guild_nickname: list[str, str] = ["guild/nickname", "POST"]
        guild_leave: list[str, str] = ["guild/leave", "POST"]
        guild_kickout: list[str, str] = ["guild/kickout", "POST"]
        guild_mute_list: list[str, str] = ["guild-mute/list", "GET"]
        guild_mute_create: list[str, str] = ["guild-mute/create", "POST"]
        guild_mute_delete: list[str, str] = ["guild-mute/delete", "POST"]
        guild_boost_history: list[str, str] = ["guild-boost/history", "GET"]

    class ChannelApi:  # 频道相关接口列表
        channel_list: list[str, str] = ["channel/list", "GET"]
        channel_view: list[str, str] = ["channel/view", "GET"]
        channel_create: list[str, str] = ["channel/create", "POST"]
        channel_update: list[str, str] = ["channel/update", "POST"]
        channel_delete: list[str, str] = ["channel/delete", "POST"]
        channel_user_list: list[str, str] = ["channel/user-list", "GET"]
        channel_move_user: list[str, str] = ["channel/move-user", "POST"]
        channel_role_index: list[str, str] = ["channel-role/index", "GET"]
        channel_role_create: list[str, str] = ["channel-role/create", "POST"]
        channel_role_update: list[str, str] = ["channel-role/update", "POST"]
        channel_role_delete: list[str, str] = ["channel-role/delete", "POST"]

    class MessageApi:  # 频道消息相关接口列表
        message_list: list[str, str] = ["message/list", "GET"]
        message_view: list[str, str] = ["message/view", "GET"]
        message_update: list[str, str] = ["message/update", "POST"]
        message_delete: list[str, str] = ["message/delete", "POST"]
        message_reaction_list: list[str, str] = ["message/reaction-list", "GET"]
        message_add_reaction: list[str, str] = ["message/add-reaction", "POST"]
        message_delete_reaction: list[str, str] = ["message/delete-reaction", "POST"]

    class ChannelUserApi:  # 频道用户相关接口列表
        channel_user_get_joined_channel: list[str, str] = ["channel-user/get-joined-channel", "GET"]

    class UserChatApi:  # 私信聊天会话接口列表
        user_chat_lis: list[str, str] = ["user-chat/list", "GET"]
        user_chat_view: list[str, str] = ["user-chat/view", "GET"]
        user_chat_create: list[str, str] = ["user-chat/create", "POST"]
        user_chat_delete: list[str, str] = ["user_chat/delete", "POST"]

    class DirectMessageApi:  # 用户私聊消息接口列表
        direct_message_list: list[str, str] = ["direct-message/list", "GET"]
        direct_message_update: list[str, str] = ["direct-message/update", "POST"]
        direct_message_delete: list[str, str] = ["direct-message/delete", "POST"]
        direct_message_reaction_list: list[str, str] = ["direct-message/reaction-list", "GET"]
        direct_message_add_reaction: list[str, str] = ["direct-message/add-reaction", "POST"]
        direct_message_delete_reaction: list[str, str] = ["direct-message/delete-reaction", "POST"]

    class UserApi:  # 用户相关接口列表
        user_me: list[str, str] = ["user/me", "GET"]
        user_view: list[str, str] = ["user/view", "GET"]
        user_offline: list[str, str] = ["user/offline", "POST"]

    class AssetApi:  # 媒体模块
        asset_create: list[str, str] = ["asset/create", "POST"]

    class InviteApi:
        invite_list: list[str, str] = ["invite/list", "GET"]
        invite_create: list[str, str] = ["invite/create", "POST"]
        invite_delete: list[str, str] = ["invite/delete", "POST"]

    class BlackListApi:
        blacklist_list: list[str, str] = ["blacklist/list", "GET"]
        blacklist_create: list[str, str] = ["blacklist/create", "POST"]
        blacklist_delete: list[str, str] = ["blacklist/delete", "POST"]

    @staticmethod
    async def requests(bot, requests: list[str, str], parameter: dict):  # 定义请求方法
        if requests[1] == "GET":  # 判断请求类型
            req = await bot.client.gate.request(requests[1], requests[0], params=parameter)  # 发送请求
            return req  # 返回数据
        elif requests[1] == "POST":  # 判断请求类型是否为POST
            req = await bot.client.gate.request(requests[1], requests[0], data=parameter)  # 发送请求
            return req  # 返回数据


# 发送消息类
class Send:  # 定义发送消息类

    def __init__(self, bot, msg=None):  # 创建基类
        self.msg = msg  # 创建传参msg
        self.bot = bot  # 创建传参bot

    async def SendText(self, content, temporary: bool, magic_id: str):  # 创建发送普通消息异步函数
        if temporary:  # 判断临时消息
            await self.msg.ctx.channel.send(content, temp_target_id=magic_id)  # 发送普通临时消息
        else:  # 否则
            message_id = await self.msg.ctx.channel.send(content)  # 发送普通消息
            return message_id  # 返回消息ID

    async def SendCard(self, content, temporary: bool, magic_id: str = ""):  # 创建发送卡片消息异步函数
        if temporary:  # 判断临时消息
            await self.msg.ctx.channel.send(content, type=MessageTypes.CARD, temp_target_id=magic_id)  # 发送卡片临时消息
        else:  # 否则
            message_id = await self.msg.ctx.channel.send(content, type=MessageTypes.CARD)  # 发送卡片消息
            return message_id  # 返回消息ID

    async def ChannelSendText(self, content, magic_id: str):  # 创建发送指定频道普通消息异步函数
        say = await self.bot.fetch_public_channel(magic_id)  # 创建频道链接
        message_id = await say.send(content)  # 给指定频道发送普通消息
        return message_id  # 返回消息ID

    async def ChannelSendCard(self, content, magic_id: str):  # 创建发送指定频道卡片消息异步函数
        say = await self.bot.fetch_public_channel(magic_id)  # 创建频道链接
        message_id = await say.send(content, type=MessageTypes.CARD)  # 给指定频道发送卡片消息
        return message_id  # 返回消息ID


class MessageInformation:  # 定义消息类
    def __init__(self, msg):
        self.msg = msg

    async def messageInformation(self) -> dict:  # 定义异步方法获取指令所有信息并返回为字典类型
        user_name = self.msg.author.username  # 获取用户名
        identity_group = self.msg.author.identify_num  # 获取用户认证数字
        text = self.msg.content  # 获取用户发送的消息文本
        user_id = self.msg.author.id  # 获取用户ID
        user_role = (await self.msg.ctx.guild.fetch_user(user_id)).roles  # 获取用户角色组
        send_server_id = self.msg.ctx.guild.id  # 获取服务器ID
        send_channel_id = self.msg.ctx.channel.id  # 获取频道ID
        user_avatar = self.msg.author.avatar  # 获取用户头像
        return {"user_name": user_name, "user_id": user_id,
                "user_role": user_role, "guild_id": send_server_id,
                "user_avatar": user_avatar, "channel_id": send_channel_id,
                "text": text, "identity_group": identity_group}  # 返回数据
