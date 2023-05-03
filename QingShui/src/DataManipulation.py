import json
import time  # 导入时间库

import yaml  # 导入yaml库

import KookApiRequests


# 配置文件读取
class Config:  # 创建配置文件类
    config: dict  # 读取所有配置文件
    bot_cfg: dict  # 读取机器人配置文件
    exp_cfg: dict  # 读取经验值配置文件
    command_cfg: dict  # 读取指令配置文件
    kook_server_cfg: dict  # 读取KOOK社区配置文件
    game_server_cfg: dict  # 读取我的世界服务器API请求配置文件
    path: str = '../config/config.yml'  # 设置路径

    @classmethod  # 绑定类模块
    def reloadConfig(cls):  # 创建读取方法
        # noinspection PyBroadException
        try:
            with open(cls.path, encoding='utf-8') as cfg:  # 创建链接
                Config.config = yaml.load(cfg, Loader=yaml.FullLoader)  # 读取yaml文件
                Config.bot_cfg = Config.config['BotInformation']  # 设置机器人配置文件
                Config.exp_cfg = Config.config['Experience']  # 设置经验值配置文件
                Config.command_cfg = Config.config['BotCommand']  # 设置机器人指令配置文件
                Config.kook_server_cfg = Config.config['KookServerSetting']  # 设置KOOK服务器配置文件
                Config.game_server_cfg = Config.config['ServerApi']  # 设置我的世界服务器API请求配置文件
            Logging.infoLog("The configuration file was successfully read")
        except:
            Logging.errorLog("Read failure")


# 经验值转换
class Experience:  # 创建经验值类
    def __init__(self, experience: int):  # 设置基类
        self.experience_dict: dict = Config.exp_cfg  # 获取
        self.experience: int = experience  # 传入经验值参数

    async def conversionLevel(self) -> dict:  # 创建判定方法
        exp_str: str = 'level-'  # 设置读取方式
        ret_dict: dict = {}  # 创建空字典方便读取
        for i in range(1, len(self.experience_dict)):  # 循环遍历配置文件中经验值数值
            l_exp = self.experience_dict[exp_str + f'{i - 1}']  # 获取上一个经验值数据
            r_exp = self.experience_dict[exp_str + f'{i}']  # 获取当前经验值数据
            l_level = i - 1  # 赋值给上一个等级
            r_level = i  # 赋值给当前等级
            if l_exp < self.experience <= r_exp:  # 判断经验值是否大于上一个经验值且小于等于下一个经验值
                ret_dict['exp'] = self.experience  # 给返回字典添加数据
                ret_dict['level'] = r_level  # 给返回字典添加数据
            elif self.experience == l_exp:  # 判断经验值是否等于上一个经验值
                ret_dict['exp'] = self.experience  # 给返回字典添加数据
                ret_dict['level'] = l_level  # 给返回字典添加数据
        if ret_dict == {}:  # 判断是否出现问题
            return {"exp": "Error", "level": "Error"}  # 发生错误返回错误
        else:  # 否则
            return ret_dict  # 返回等级以及经验值





# 日志映射
class Logging:  # 定义日志类
    debug = "[Debug]"  # 创建debug参数
    info = "[Info]"  # 创建info参数
    warn = "[Warn]"  # 创建warn参数
    error = "[Error]"  # 创建error参数
    fatal = "[Fatal]"  # 创建fatal参数

    @classmethod  # 定义类方法
    def debugLog(cls, running_message):  # 创建debug方法
        datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取日期
        print(f"{cls.debug} {datatime} {running_message}")  # 发送日志信息

    @classmethod  # 定义类方法
    def infoLog(cls, running_message):  # 创建info方法
        datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取日期
        print(f"{cls.info} {datatime} {running_message}")  # 发送日志信息

    @classmethod  # 定义类方法
    def warnLog(cls, running_message):  # 创建warn方法
        datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取日期
        print(f"{cls.warn} {datatime} {running_message}")  # 发送日志信息

    @classmethod  # 定义类方法
    def errorLog(cls, running_message):  # 创建error方法
        datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取日期
        print(f"{cls.error} {datatime} {running_message}")  # 发送日志信息

    @classmethod  # 定义类方法
    def fatalLog(cls, running_message):  # 创建fatal方法
        datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 获取日期
        print(f"{cls.fatal} {datatime} {running_message}")  # 发送日志信息


# 获取参数
class Parameter:  # 创建参数类
    def __init__(self, args: tuple):  # 创建基类
        self.args: tuple = args  # 获取传参

    def indexParameter(self) -> dict:  # 定义初始化参数模块
        arg_list: list = []  # 创建返回列表
        for one_type in self.args:  # 循环遍历元组数据
            arg_list.append(one_type)  # 添加数据
        length: int = len(arg_list)  # 获取长度
        return {'length': length, 'args': arg_list}  # 返回数据


# 参数异常反馈
class ErrorParameter:  # 定义参数异常类
    def __init__(self, msg):  # 创建传参方法
        self.msg = msg  # 创建参数msg
        self.message_information = KookApiRequests.MessageInformation(self.msg)  # 创建参数user_information
        self.send = KookApiRequests.Send(None, self.msg)  # 创建参数send

    async def parameterErrorPrompt(self):  # 创建反馈方法
        inf = await self.message_information.messageInformation()  # 获取消息信息
        context = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "color": "#DC143C",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": "参数错误"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "plain-text",
                            "content": "您可能输入了不存在的参数或是缺少参数"
                        }
                    }
                ]
            }
        ]  # 设置卡片消息
        await self.send.SendCard(context, True, inf['user_id'])  # 发送消息
Config.reloadConfig()
print(Config.config)