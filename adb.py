import os
import json
import time
import r
from loguru import logger
import config



def get_hyperv_port(conf_path=r"C:\\ProgramData\\BlueStacks_nxt\\bluestacks.conf", instance_name="Pie64", read_imageinfo_from_config=False) -> int:
        """ 获取Hyper-v版蓝叠的adb port
        :param conf_path: bluestacks.conf 的路径+文件名
        :param instance_name: 多开的名称，在bluestacks.conf中以类似bst.instance.<instance_name>.status.adb_port的形式出现，如Nougat64，Pie64，Pie64_1等
        :return: adb端口
        此方法来自:MAA https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/dev/src/Python/asst/emulator.py
        """
        with open(conf_path, encoding="UTF-8") as f:
            configs = {
                line.split('=')[0].strip(): line.split('=')[1].strip().strip('"\n')
                for line in f
            }
            if read_imageinfo_from_config:
                instances = [i.strip('"') for i in configs['bst.installed_images'].split(',')]
                instance_name = instances[0]
        return int(configs[f'bst.instance.{instance_name}.status.adb_port'].replace('"', ""))
    
def connect_bluestack():
    adb_path = config.user_config['adb_path']
    device = '127.0.0.1:' + str(get_hyperv_port())
    os.system(f'{adb_path} connect {device}')
    output = os.popen(f'{adb_path} devices').read().strip().split('\n')
    if len(output) <= 1 or output[0] != 'List of devices attached':
        logger.error('Error: 无法连接蓝叠(列表为空))')
        return None
    else:
        config.user_config['adb_address'] = device
        logger.debug(f'已连接设备：{device}')
        config.user_config['device_id'] = device
        logger.debug('已设置devide为蓝叠端口')
        return device
    
def is_qq_on(re_try=True):
    '''检测QQ是否在前台'''
    command = (f'{config.ADB_HEAD} shell dumpsys window windows')
    try:
        process = os.popen(command)
        output = process.read()
        process.close()
        if config.APPID not in output:
            if not re_try:
                logger.info('游戏不在前台')
                return False
            # 应用不在前台，运行应用
            logger.info("游戏不在前台，正在启动")
            logger.debug(f'{config.ADB_HEAD} shell am start {config.APPID}/{config.ACTIVITY}')
            # os.popen(f'{config.ADB_HEAD} shell monkey -p {config.APPID} -c android.intent.category.LAUNCHER 1')
            os.popen(f"{config.ADB_HEAD} shell am start {config.APPID}/{config.ACTIVITY}")
            time.sleep(8)
            return is_qq_on(False)
        else:
            # 处理输出
            logger.debug('应用已在前台')
            return True
    except Exception as e:
        logger.error(f'Error: {e}')
        return False
    
def forward_ports():
    """使用 adb forward 命令将模拟器内的 3600 和 3601 端口分别映射到 36000 和 36001"""
    adb_path = config.user_config['adb_path']
    device = config.user_config['adb_address']
    os.system(f'{adb_path} -s {device} forward tcp:36000 tcp:3600')
    os.system(f'{adb_path} -s {device} forward tcp:36001 tcp:3601')
    logger.debug('已映射端口')

def main():
    # 连接蓝叠模拟器
    device = connect_bluestack()
    if device is None:
        logger.error('无法连接蓝叠模拟器')
        return

    # 检查 QQ 是否在前台，如果不是则启动 QQ
    if not is_qq_on():
        logger.error('无法启动 QQ')
        return

    # 使用 adb forward 命令将模拟器内的 3600 和 3601 端口分别映射到 36000 和 36001
    forward_ports()

if __name__ == '__main__':
    main()