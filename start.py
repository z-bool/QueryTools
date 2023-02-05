from spider.RunTask import main, tryme
from log.outputlog import Log
import time
import click


BANNER = """
                   ,---,         ,---,         ,---,        
                  '  .' \       '  .' \       '  .' \       
                 /  ;    '.    /  ;    '.    /  ;    '.     
                :  :       \  :  :       \  :  :       \    
                :  |   /\   \ :  |   /\   \ :  |   /\   \   
                |  :  ' ;.   :|  :  ' ;.   :|  :  ' ;.   :  
                |  |  ;/  \   \  |  ;/  \   \  |  ;/  \   \ 
                '  :  | \  \ ,'  :  | \  \ ,'  :  | \  \ ,' 
                |  |  '  '--' |  |  '  '--' |  |  '  '--'   
                |  :  :       |  :  :       |  :  :         
                |  | ,'       |  | ,'       |  | ,'         
                `--''         `--''         `--''     
                
            重点声明:
                QueryTools: 安全工具
                    1.接口对请求频率有限制,查询效率较慢,请耐心等待.
                    2.QueryIpTools工具仅用于技术交流学习,请勿用于违法用途,否则与本人无关.
                    3.QueryIpTools工具仅用于技术交流学习,不得用于商业用途,仅做交流学习,仅作技术交流学习.
                    4.QueryIpTools种使用到的接口均为公开接口
                
"""


@tryme.try_
@click.command()
@click.option("--file", default="text.txt", help="-- file xxx.txt")
def start(file):
    time.sleep(3)
    Log.info(BANNER)
    main(file)


if __name__ == '__main__':
    start()
