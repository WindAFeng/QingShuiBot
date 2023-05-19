import time


class Log(object):
    """
    需要参数:
    无
    类参数:
    无
    描述：实现日志输出
    """
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
