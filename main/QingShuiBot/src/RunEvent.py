import KookRequest


class JoinGuild:
    class AddUserUntrustedGrant:
        @classmethod
        async def index(cls, bot, user_id: str):
            kar = KookRequest.Requests
            await kar.requests(bot=bot, requests=kar.GuildRoleApi.guild_role_grant,
                               parameter={"guild_id": "8329917220869199",
                                          "user_id": user_id,
                                          "role_id": 20161779})
