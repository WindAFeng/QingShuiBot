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
    imp = ImportantInformation  # 导入重要信息模块

    @classmethod
    async def getCommands(cls, number: int):
        #  获取命令列表
        command_cfg: dict = Help.imp.config['Command']  # 获取命令配置
        start: int = number * 5 - 5  # 起始命令的索引
        end: int = number * 5  # 结束命令的索引
        command_list: list = []  # 命令列表
        number_list: list = []  # 数字列表
        for command in command_cfg:  # 遍历命令配置
            command_list.append({command: command_cfg[command]})  # 将命令添加到命令列表中
        if end > len(command_cfg):  # 判断是否超出命令数量
            end = len(command_cfg)  # 修正结束命令的索引
            for point in range(start, end):
                number_list.append(command_list[point])  # 将命令列表中的命令添加到数字列表中
            return number_list
        else:
            for point in range(start, end):
                number_list.append(command_list[point])  # 将命令列表中的命令添加到数字列表中
            return number_list

    @classmethod
    async def getNumberBook(cls, args: tuple):
        #  获取数字书籍
        arg: dict = Help.imp.arg.init(args)  # 初始化参数
        command_param_num: dict = Help.imp.config['Command']['help']['param_num']  # 获取help命令的参数数量配置
        length = arg['length']  # 获取参数长度
        if length in command_param_num:  # 判断参数长度是否在配置中
            if length == 0:  # 参数长度为0
                arg['args'].append(1)  # 添加数字1到参数列表
                return arg['args'][0]  # 返回数字1
            else:  # 参数长度不为0
                return arg['args'][0]  # 返回参数列表中的第一个数字

    @classmethod
    async def extractInformation(cls, args: tuple) -> str:
        #  提取命令信息
        number = await Help.getNumberBook(args)  # 获取数字书籍
        command_cfg: list = await Help.getCommands(number)  # 获取命令列表
        command_cfg_dict = {}  # 命令配置字典
        for point in command_cfg:
            for key in point:
                command_cfg_dict[key] = point[key]  # 将命令列表中的命令添加到命令配置字典中
        cmd_list: list = []  # 命令列表
        for key in command_cfg_dict:
            value: dict = command_cfg_dict[key]  # 获取命令配置
            name: str = value['name']  # 获取命令名称
            param: str = value['param']  # 获取命令参数
            content: str = value['content']  # 获取命令内容
            param_number: str = ""  # 参数数量字符串
            for point in value['param_num']:  # 遍历参数数量列表
                param_number += str(point) + ','  # 将参数数量拼接到参数数量字符串中
            cmd_list.append(f">  **{content}**\n`{name}  {param}`\n所需参数数量:{param_number}\n")  # 将命令信息添加到命令列表中
        command_str: str = ""  # 命令字符串
        for command in cmd_list:
            command_str += command  # 将命令列表中的命令字符串拼接到命令字符串中
        return command_str

    @classmethod
    async def main(cls, msg, args):
        #  主函数
        send = Help.imp.send  # 获取消息发送模块
        card = Help.imp.cards  # 获取卡片模块
        await send.sendMessage(msg=msg, messageObject=send.cardMessage,
                               content=card.CommandCard.helpCard(commandList=await Help.extractInformation(args),
                                                                 bookNumber=await Help.getNumberBook(
                                                                     args)))  # 发送消息、卡片消息和命令列表信息


class Main:
    imp = ImportantInformation  # 导入重要信息模块

    @classmethod
    async def main(cls):
        pass


class QueryServer:
    imp = ImportantInformation  # 导入重要信息模块

    @classmethod
