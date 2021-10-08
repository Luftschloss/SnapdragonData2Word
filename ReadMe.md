SDConfig.json：是SnapDragon测试项的描述及单位等信息的配置文件
MultiGroupConfig.json：是SnapDragon数据生成Word，测试项合并配置文件
FrameDataOutput.py：帧数据输出脚本
WordOutput.py：RealTime数据生成图表脚本
SnapdragonEXE下是对应的修改完的Snapdragon版本，运行环境需要下载GTK#，下载链接：https://www.mono-project.com/download/stable/ ，解压后有一个配置文件CaptureSettings.txt，用来配置帧数据及相关截图的保存路径的，和处理帧数据的frameResourcePath（main.py中）保持一致，需要管理员权限运行。
