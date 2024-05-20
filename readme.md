# 仿真2d_胜率分析软件
# 仅用于AutoPlay的result.txt文件分析
# 对于其余数据格式，请自行对源代码进行修改使用

# 保存路径:

文本分析结果保存路径：./finalResult/analysisResult.txt 文本文件内

折线图分析结果保存路径：./charts/datetime(保存的日期时间)/内的 .html 文件

Avg_Score_Gap.html：每场平均分差分析，值为正向或负向较大值，意味着比分正向或负向差距越大，显示出两支队伍间的实力差距

Win_ProbAndAvg_Gain_Lose.html：胜率以及平均进/失球分析统计

可以根据analysisResult.txt中的时间戳来寻找对应的分析图文件夹

# 环境依赖：

Python>=3.8

pyinstaller==5.13.0

PyQt6==6.4.2

pyqt6-plugins==6.4.2.2.3

PyQt6-Qt6==6.4.3

PyQt6-sip==13.6.0

pyqt6-tools==6.4.2.3.3

qt6-applications==6.4.3.2.3

qt6-tools==6.4.3.1.3

plotly==5.15.0

pandas==2.0.3

# 方式一：

将源码打包下载到本地 

Linux下在终端中输入 

python3 runMain.py 即可

Windows下在命令窗口中输入 

python runMain.py 即可

# 方式二：

下载对应系统发行版

Windows：仿真2d_胜率分析软件V1.0_Windows.exe

双击运行即可(请确保logo文件夹与可执行处于同级目录下)

Ubuntu：仿真2d_胜率分析软件V1.0_Ubuntu

右键运行即可(请确保logo文件夹与可执行处于同级目录下)

如出现文件无权限，输入：chmod 777 ./仿真2d_胜率分析软件V1.0_Ubuntu 即可

# 对于源码打包命令：

下载打包工具：pip/pip3 install pyinstaller  -i  https://pypi.tuna.tsinghua.edu.cn/simple

在源码所在文件夹打开终端输入：pyinstaller --onefile --icon=./favicon.ico --windowed --strip --name="仿真2d_胜率分析软件" runMain.py

# 在Windows下补全环境：

1. 安装Python>=3.8
2. 打开cmd命令窗口，输入：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
即可

# 在Ubuntu下补全环境(有些可能需要进入root用户下进行)：

1. 打开终端输入：
sudo apt-get install python3 python3-dev python3-pip
2. 输入：
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
即可

# result.txt为测试文件

# PS:

analysisWindows.ui 为 PyQt6 所创建主体框架文件，可在终端或命令窗口中输入:

#用于打开designer设计工具

pyqt6-tools designer

#将test.ui 转换为.py文件

pyuic6 -o test.py test.ui

#直接使用designer打开ui文件进行修改

pyqt6-tools designer analysisWindows.ui


