import requests
from mcstatus import JavaServer


class McStatus:
    latency: str
    version: str
    player_max: str
    player_online: str

    @classmethod
    def server(cls, server_ip: str, server_port: str = "25565"):
        look_up = JavaServer.lookup(f"{server_ip}:{server_port}")
        status = look_up.status()
        McStatus.player_online = status.players.online
        McStatus.player_max = status.players.max
        McStatus.latency = status.latency
        McStatus.version = status.version.name
        return McStatus()


class HypixelStatus:
    __url__: str = "https://api.hypixel.net/player"
    __key__: str = "9a7b0fe3-6f0a-4783-9515-881b779d9374"

    def __init__(self, username: str):
        self.__username__ = username

    @property
    def request(self):
        data = requests.get(
            url=self.__url__,
            params={
                "key": self.__key__,
                "name": self.__username__
            })
        return data.json()
