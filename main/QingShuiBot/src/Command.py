import CardMessage
import KookRequest
from PublicFunction import *

Config.reload()


class ImportantInformation:
    config = Config.config
    log = Log
    request = KookRequest.Requests
    send = KookRequest.Send
    msgInf = KookRequest.MessageInformation
    cards = CardMessage
    arg = Parameter


class Help:
    imp = ImportantInformation

    @classmethod
    async def getCommands(cls, number: int):
        command_cfg: dict = Help.imp.config['Command']
        start: int = number * 5 - 5
        end: int = number * 5
        command_list: list = []
        number_list: list = []
        for command in command_cfg:
            command_list.append({command: command_cfg[command]})
        if end > len(command_cfg):
            end = len(command_cfg)
            for point in range(start, end):
                number_list.append(command_list[point])
            return number_list
        else:
            for point in range(start, end):
                number_list.append(command_list[point])
            return number_list

    @classmethod
    async def getNumberBook(cls, args: tuple):
        arg: dict = Help.imp.arg.init(args)
        command_param_num: dict = Help.imp.config['Command']['help']['param_num']
        length = arg['length']
        if length in command_param_num:
            if length == 0:
                arg['args'].append(1)
                return arg['args'][0]
            else:
                return arg['args'][0]

    @classmethod
    async def extractInformation(cls, args: tuple) -> str:
        number = await Help.getNumberBook(args)
        command_cfg: list = await Help.getCommands(number)
        command_cfg_dict = {}
        for point in command_cfg:
            for key in point:
                command_cfg_dict[key] = point[key]
        cmd_list: list = []
        for key in command_cfg_dict:
            value: dict = command_cfg_dict[key]
            name: str = value['name']
            param: str = value['param']
            content: str = value['content']
            param_number: str = ""
            for point in value['param_num']:
                param_number += str(point) + '/'
            cmd_list.append(f"> **{content}**\n`{name} {param}`\n所需参数数量:{param_number}\n")
        command_str: str = ""
        for command in cmd_list:
            command_str += command
        return command_str

    @classmethod
    async def main(cls, msg, args):
        send = Help.imp.send
        card = Help.imp.cards
        await send.sendMessage(msg=msg, messageObject=send.cardMessage,
                               content=card.CommandCard.helpCard(commandList=await Help.extractInformation(args),
                                                                 bookNumber=await Help.getNumberBook(args)))
