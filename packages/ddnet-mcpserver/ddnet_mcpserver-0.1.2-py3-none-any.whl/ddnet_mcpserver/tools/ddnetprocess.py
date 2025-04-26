import psutil

def is_process_running(process_name):
    """检查指定名称的进程是否正在运行"""
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def get_process_status():   
    """获取ddnet进程状态"""
    if is_process_running("ddnet.exe"):
        return "DDNet正在运行"
    else:
        return "DDNet未运行"

def stop_process():
    """关闭ddnet进程"""
    for proc in psutil.process_iter(['name']):
        try:
            if "ddnet.exe" in proc.info['name']:
                proc.terminate()
                return "DDNet进程已关闭"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "DDNet进程未运行"
