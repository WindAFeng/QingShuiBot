from khl import MessageTypes


class Requests(object):
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

    class GuildRoleApi:
        guild_role_list: list[str, str] = ["guild-role/list", "GET"]
        guild_role_create: list[str, str] = ["guild-role/create", "POST"]
        guild_role_update: list[str, str] = ["guild-role/update", "POST"]
        guild_role_delete: list[str, str] = ["guild-role/delete", "POST"]
        guild_role_grant: list[str, str] = ["guild-role/grant", "POST"]
        guild_role_revoke: list[str, str] = ["guild-role/revoke", "POST"]

    class InviteApi:
        invite_list: list[str, str] = ["invite/list", "GET"]
        invite_create: list[str, str] = ["invite/create", "POST"]
        invite_delete: list[str, str] = ["invite/delete", "POST"]

    class BlackListApi:
        blacklist_list: list[str, str] = ["blacklist/list", "GET"]
        blacklist_create: list[str, str] = ["blacklist/create", "POST"]
        blacklist_delete: list[str, str] = ["blacklist/delete", "POST"]

    guildApi = GuildApi
    channelApi = ChannelApi
    messageApi = MessageApi
    channelUserApi = ChannelUserApi
    userChatApi = UserChatApi
    directMessageApi = DirectMessageApi
    userApi = UserApi
    assetApi = AssetApi
    guildRoleApi = GuildRoleApi
    inviteApi = InviteApi
    blackListApi = BlackListApi

    @classmethod
    async def requests(cls, bot, requests: list[str, str], parameter: dict):  # 定义请求方法
        if requests[1] == "GET":  # 判断请求类型
            req = await bot.client.gate.request(requests[1], requests[0], params=parameter)  # 发送请求
            return req  # 返回数据
        elif requests[1] == "POST":  # 判断请求类型是否为POST
            req = await bot.client.gate.request(requests[1], requests[0], data=parameter)  # 发送请求
            return req  # 返回数据


# 发送消息类
class Send:  # 定义发送消息类
    textMessage: list = [MessageTypes.TEXT, "text"]
    cardMessage: list = [MessageTypes.CARD, "card"]
    textTo: list = [MessageTypes.TEXT, "text-to"]
    cardTo: list = [MessageTypes.CARD, "card-to"]

    @classmethod
    async def sendMessage(cls,
                          msg: any = None,
                          bot: any = None,
                          messageObject: list = None,
                          content: any = None,
                          temporary: bool = None,
                          magic_id: str = None):
        async def sendText():
            if temporary:  # 判断临时消息
                await msg.ctx.channel.send(content, type=messageObject[0], temp_target_id=magic_id)  # 发送普通临时消息
            else:  # 否则
                message_id = await msg.ctx.channel.send(content)  # 发送普通消息
                return message_id  # 返回消息ID

        async def sendCard():
            if temporary:  # 判断临时消息
                await msg.ctx.channel.send(content, type=messageObject[0], temp_target_id=magic_id)  # 发送卡片临时消息
            else:  # 否则
                message_id = await msg.ctx.channel.send(content, type=messageObject[0])  # 发送卡片消息
                return message_id  # 返回消息ID

        async def channelSendText():
            say = await bot.client.fetch_public_channel(magic_id)  # 创建频道链接
            message_id = await say.send(content, type=messageObject[0])  # 给指定频道发送普通消息
            return message_id  # 返回消息ID

        async def channelSendCard():  # 创建发送指定频道卡片消息异步函数
            say = await bot.client.fetch_public_channel(magic_id)  # 创建频道链接
            message_id = await say.send(content, type=messageObject[0])  # 给指定频道发送卡片消息
            return message_id  # 返回消息ID

        function_dict = {"text": lambda: sendText(),
                         "card": lambda: sendCard(),
                         "text-to": lambda: channelSendText(),
                         "card-to": lambda: channelSendCard()}
        running = await function_dict[messageObject[1]]()
        return running


class MessageInformation:  # 定义消息类
    user_name: str
    user_id: str
    user_role: list
    guild_id: str
    user_avatar: str
    channel_id: str
    text: str
    identity_group: str

    @classmethod
    async def messageInformation(cls, msg):  # 定义异步方法获取指令所有信息并返回为字典类型
        msg_inf = MessageInformation
        msg_inf.user_name = msg.author.username  # 获取用户名
        msg_inf.identity_group = msg.author.identify_num  # 获取用户认证数字
        msg_inf.text = msg.content  # 获取用户发送的消息文本
        msg_inf.user_id = msg.author.id  # 获取用户ID
        msg_inf.user_role = (await msg.ctx.guild.fetch_user(msg_inf.user_id)).roles  # 获取用户角色组
        msg_inf.guild_id = msg.ctx.guild.id  # 获取服务器ID
        msg_inf.channel_id = msg.ctx.channel.id  # 获取频道ID
        msg_inf.user_avatar = msg.author.avatar  # 获取用户头像
        return MessageInformation
