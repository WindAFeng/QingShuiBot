import time

import yaml


class Log(object):
    __debug: str = "[DEBUG]"
    __info: str = "[INFO]"
    __warn: str = "[WARN]"
    __error: str = "[ERROR]"
    __fatal: str = "[FATAL]"
    __datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    @classmethod
    def _printf(cls, level: str = None, runningMessage: str = None):
        """
        需要level, runningMessage参数传入
        是否返回数据:不是
        返回类型:None
        函数描述:日志输出基类
        """
        print(f"{level} {Log.__datatime} {runningMessage}")

    @classmethod
    def debugLog(cls, runningMessage: str = None):
        """
        需要runningMessage参数传入
        是否返回数据:不是
        返回类型:None
        函数描述:输出debug日志
        """
        Log._printf(level=cls.__debug, runningMessage=runningMessage)

    @classmethod
    def infoLog(cls, runningMessage: str = None):
        """
        需要runningMessage参数传入
        是否返回数据:不是
        返回类型:None
        函数描述:输出info日志
        """
        Log._printf(level=cls.__info, runningMessage=runningMessage)

    @classmethod
    def warnLog(cls, runningMessage: str = None):
        """
        需要runningMessage参数传入
        是否返回数据:不是
        返回类型:None
        函数描述:输出warn日志
        """
        Log._printf(level=cls.__warn, runningMessage=runningMessage)

    @classmethod
    def errorLog(cls, runningMessage: str = None):
        """
        需要xxx, xxx参数传入
        是否返回数据:是或不是
        返回类型:str|int|list|dict......
        函数描述:
        """
        Log._printf(level=cls.__error, runningMessage=runningMessage)

    @classmethod
    def fatalLog(cls, runningMessage: str = None):
        """
        需要xxx, xxx参数传入
        是否返回数据:不是
        返回类型:None
        函数描述:输出fatal日志
        """
        Log._printf(level=cls.__fatal, runningMessage=runningMessage)


class Config(object):
    # 定义类属性
    config: dict
    __path: str = "../config/config.yml"  # 配置文件位置

    @classmethod
    def reload(cls):  # reload类方法
        try:
            with open(cls.__path, encoding='utf-8') as cfg:
                Config.config = yaml.load(cfg, Loader=yaml.FullLoader)  # 读取yaml文件
                cfg.close()
            Log.infoLog("Reload Success")
        except FileNotFoundError:  # 如果找不到文件
            Log.errorLog("Not Found Config")
            Log.infoLog("Created Config File")
            open(cls.__path, 'w')


class Parameter:

    @classmethod  # 类方法装饰器
    def init(cls, args: tuple = None):  # init初始化方法，参数为元组类型，可为空
        args_list: list = []
        for point in args:  # 遍历参数元组
            args_list.append(point)  # 将参数元组中的每个元素添加到args_list列表中
        return {"length": len(args_list), "args": args_list}  # 返回一个字典，包含args_list的长度和内容
