# -*- coding= utf-8 -*-
import commands, sys
from setproctitle import setproctitle

reload(sys)
sys.setdefaultencoding('utf-8')

def setSingleProcess(ProcName):
    """
    Set process name only if not exists.
    """
    procString = commands.getoutput('ps -A | grep -E '+ProcName+'$')
    if procString!="":
        return False
    else:
        setproctitle(ProcName)
        return True
