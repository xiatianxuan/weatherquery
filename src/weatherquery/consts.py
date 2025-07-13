GLOBAL_DEBUG=True # 全局调试标志 

class Logger:
    def __init__(self,is_debug:bool):
        self.__is_debug=is_debug
    
    def log(self,text:str,flag:str="LOG")->None:
        if self.__is_debug:
            print(f"{flag}:\t{text}")
    
    def debug(self,text:str):
        self.log(text,"DEBUG")

LOGGER=Logger(GLOBAL_DEBUG)