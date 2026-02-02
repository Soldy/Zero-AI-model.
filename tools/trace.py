import copy

def readLog(log_file_name_ : str)->list[dict[str,str|int]]:
    out : list[dict[str,str|int]] = []
    with open(log_file_name_, 'r', encoding='UTF-8') as file:
        data : str = file.read().rstrip()
        lines : list[str]= data.split("\n")
        for i in lines:
            pack : dict[str,str|int] = {}
            a = i.split('. ')
            pack['serial'] = a[0]
            b = a[1].split(' ! ')
            pack['timestamp'] = b[0]
            c = a[1].split(' | ')
            pack['ncc'] = c[0]
            pack['mem'] = c[1]
            out.append(pack)
    return out

def memsFromLog(
  log_ : list[dict[str,str|int]],
  limit_:int = 999999999999
)->list[str]:
    serial : int= 0
    out : list[int] = []
    for i in log_:
        if serial > limit_ :
            break
        out.append(int((int(i['mem'])/1024)/1024))
        serial = serial + 1
    return out

def timeFromLog(
  log_ : list[dict[str,str|int]],
  limit_:int = 999999999999
)->list[str]:
    serial : int= 0
    out : list[int] = []
    start_time : int = 0
    first : bool = True
    for i in log_:
        if serial > limit_ :
            break
        times = int(int(i['timestamp'])/1000)
        if first :
            first = False
            start_time = copy.deepcopy(times)
            out.append(0)
        else:
            out.append(times-start_time)
            print(times-start_time)
        serial = serial + 1
    return out
