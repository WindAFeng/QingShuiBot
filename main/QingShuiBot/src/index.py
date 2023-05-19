class QingShuiBot:
    class Variable:
        pass

    class Constant:
        pass

    class IndexFunction:
        def __init__(self):
            self.__var = QingShuiBot.Variable
            self.__con = QingShuiBot.Constant

    class BotRunning:
        def __init__(self):
            self.__var = QingShuiBot.Variable
            self.__con = QingShuiBot.Constant

        def indexRunning(self):
            pass


if __name__ == '__main__':
    runningBot = QingShuiBot().BotRunning()
    runningBot.indexRunning()
