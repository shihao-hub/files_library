import argparse
from configparser import ConfigParser


def write(config: ConfigParser):
    # 添加节
    config.add_section('Settings')
    # 设置键值对
    config.set('Settings', 'font', 'Arial')
    config.set('Settings', 'fontsize', '12')

    # 写入文件
    with open('ini_config_test.ini', 'w') as configfile:
        config.write(configfile)


def read(config: ConfigParser):
    # 读取配置文件
    config.read('ini_config_test.ini')

    # 获取配置值
    font = config.get('Settings', 'font')
    fontsize = config.getint('Settings', 'fontsize')

    print(f'Font: {font}, Font Size: {fontsize}')

    # 检查节是否存在
    if config.has_section('User'):
        name = config.get('User', 'name')
        age = config.get('User', 'age')
        print(f'User Name: {name}, Age: {age}')


def main():
    parser = argparse.ArgumentParser()

    choices = {"write": write, "read": read}

    parser.add_argument("rw", choices=choices)

    # 创建配置解析器
    config = ConfigParser()

    args = parser.parse_args()
    fn = choices[args.rw]
    fn(config)


if __name__ == '__main__':
    main()
