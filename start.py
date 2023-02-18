#coding=gbk
import requests

from spider.RunTask import main, tryme
from log.outputlog import Log
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
                
"""


@tryme.try_
@click.command()
@click.option("--file", default="text.txt", help="-- file xxx.txt")
def start(file):
    Log.info(BANNER)
    main(file)


if __name__ == '__main__':
    start()

