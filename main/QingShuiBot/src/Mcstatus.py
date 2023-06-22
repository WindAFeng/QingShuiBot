from mcstatus import JavaServer


class Status:
    latency: str
    version: str
    player_max: str
    player_online: str


class McStatus:
    @classmethod
    def server(cls, server_ip: str, server_port: str = "25565") -> Status:
        look_up = JavaServer.lookup(f"{server_ip}:{server_port}")
        status = look_up.status()
        Status.player_online = status.players.online
        Status.player_max = status.players.max
        Status.latency = status.latency
        Status.version = status.version.name
        return Status()
