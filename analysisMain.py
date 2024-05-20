# -*- coding: utf-8 -*- 
  
# ==============================
# @author: Joycat
# @time: 2024/04/28
# ==============================

###########################################################################
##
## PLEASE DO *NOT* EDIT THIS FILE!
##
###########################################################################
## CLASS AnalysisResult
###########################################################################
from re import search
from os import path, makedirs
from math import log
from plotly.express import line
from  plotly.graph_objects import Scatter
from pandas import DataFrame
from datetime import datetime

class AnalysisResult():
    '''
    对目标路径文本文件与队伍名称进行匹配
    分析目标队伍的胜率等情况
    '''
    def __init__(self, filePath, teamName):
        """  
        初始化方法,用于创建类的实例时设置初始状态  
  
        Args:  
            filePath (str): 文件路径,指定了数据存储或读取的位置  
            teamName (str): 团队名称,可能用于标识或分类数据  
  
        Returns:  
            None: 初始化方法不返回任何值,而是设置对象的属性  
        """
        self.filePath = filePath
        self.teamName = teamName
        self.saved = False # 用于判断当前对象的分析结果保存状态,初始为false 未保存
        self.finalData = list()
        self.errorsMessages = list()
        self.finalScoreGapDict = dict()
        self.winPro0Dict = dict()
        self.winPro1Dict = dict()
        self.winPro2Dict = dict()
        self.avgGainDict = dict()
        self.avgLoseDict = dict()
        self.nowTime = None
        self.figObject = list()

    def getOriginalResult(self):
        """  
        读取指定文件路径下的文件内容,并返回所有行组成的列表

        Args:  
            无
        Returns:  
            如果文件存在且不为空,返回包含文件所有行的列表(每行作为列表的一个元素)  
            如果文件不存在或为空,向self.errorsMessages列表中添加错误信息,并返回False  
        """
        if not path.exists(self.filePath):
            self.errorsMessages.append(f"{self.filePath} does not exist")
            return False
        file = open(self.filePath)
        lines = file.readlines()
        file.close()
        if not lines:
            self.errorsMessages.append(f"{self.filePath} is empty")
            return False
        return lines
    
    def isMatchLine(self, line):
        """  
        判断传入的字符串是否符合特定的匹配规则
  
        Args:  
            line (str): 待匹配的字符串
  
        Returns:  
            如果line符合第一个匹配规则,返回包含多个分组信息的元组,最后一个元素为True
            如果line符合第二个匹配规则,返回包含多个分组信息的元组,最后一个元素为False
            如果line不符合任何匹配规则,返回False
        """
        pattern1 = rf'{self.teamName}:(\S+)(\s+)(\d+):(\d+)(\s+)(\d+)-(\S+)_(\d+)-vs-(\S+)_(\d+)'
        isMatch = search(pattern1, line)
        if isMatch:
            return (self.teamName, isMatch.group(1), isMatch.group(3), isMatch.group(4), isMatch.group(6), True)#True用于判断当前数据输出时是否需要更改位置
        if not isMatch:
            pattern2 = rf'(\S+):{self.teamName}(\s+)(\d+):(\d+)(\s+)(\d+)-(\S+)_(\d+)-vs-(\S+)_(\d+)'
            isMatch = search(pattern2, line)
        if isMatch:
            return (self.teamName, isMatch.group(1), isMatch.group(4), isMatch.group(3), isMatch.group(6), False)
        if not isMatch:
            return False
    
    
    def getAllOppTeamNames(self, lines):
        """  
        从给定的行列表中提取所有对手队伍名称,并返回这些名称的列表

        :param lines: 包含比赛信息的行列表
        :type lines: list[str]  
        :return: 对手队伍名称的列表
        :rtype: list[str]  
        """
        if not lines:
            return False
        oppTeamNames = list()
        for line in lines:
            matchData = self.isMatchLine(line)
            if matchData and matchData[1] not in oppTeamNames:
                oppTeamNames.append(matchData[1])
        return oppTeamNames
    
    def getAllMatchedLines(self, lines):
        """  
        从给定的行列表中提取所有匹配的行数据,并返回这些数据的列表

        :param lines: 包含比赛信息的行列表
        :type lines: list[str]  
        :return: 匹配行数据的列表,每个元素是一个包含多个分组信息的元组
        :rtype: list[tuple]  
        """
        if not lines:
            return False
        matchedLines = list()
        for line in lines:
            matchData = self.isMatchLine(line)
            if matchData:
                matchedLines.append(matchData)
        return matchedLines
    
    def sortedByTeamName(self, oppTeamNames, matchedLines):
        """  
        根据对手队伍名称对匹配的行数据进行排序,并返回排序后的字典
  
        :param oppTeamNames: 对手队伍名称的列表
        :type oppTeamNames: list[str]  
        :param matchedLines: 匹配行数据的列表
        :type matchedLines: list[tuple]  
        :return: 以对手队伍名称为键,对应匹配行数据列表为值的字典
        :rtype: dict[str, list[tuple]]  
        """ 
        if not oppTeamNames or not matchedLines:
            return False
        sortedLines = dict()
        for oopTeamName in oppTeamNames:
            sortedLines[oopTeamName] = list()
        for matchedLine in matchedLines:
            for oopTeamName in oppTeamNames:
                if matchedLine[1] == oopTeamName:
                    sortedLines[oopTeamName].append(matchedLine)
        return sortedLines
    
    def getNowTime(self):
        """  
        获取当前时间并返回格式化后的字符串
  
        :return: 当前时间的格式化字符串,格式为"%Y%m%d%H%M%S"  
        :rtype: str  
        """  
        nowTime = datetime.now()
        nowTime = nowTime.strftime("%Y%m%d%H%M%S")
        return nowTime


    def calculateScoreCommenly(self, sortedLine):
        """  
        根据传入的排序后的比赛行数据计算得分情况,并返回相应的得分和状态
  
        :param sortedLine: 排序后的比赛行数据,包含至少四个元素,其中索引2和3分别代表两个队伍的得分 
        :type sortedLine: list or tuple  
        :return: 一个包含得分和状态的元组,格式为(队伍1得分, 队伍2得分, 状态)
        :rtype: tuple[int, int, str]  
        """
        if int(sortedLine[2]) == int(sortedLine[3]):
            return (1,1,"Peace")
        if int(sortedLine[2]) > int(sortedLine[3]):
            return (3,0,"Win")
        if int(sortedLine[2]) < int(sortedLine[3]):
            return (0,3,"Lose")
    
    def calculateScoreGap(self, ourScore, oppScore): 
        # +1进行偏移是为了避免分数为0产生计算错误
        # 计算结果越大/小, 平均分差越大,趋于0则分差较小 
        # 计算公式仍可以优化,当前公式计算结果对于 4:0 比 13:2 更加敏感
        ratio = (ourScore+1) / (oppScore+1)
        score_gap = log(ratio)  
        return score_gap
    
    def mean(self, scoreRatio):
        '''
        计算均值

        Args:  
            self: 类实例的引用
            scoreRatio: 列表,得分比率
  
        返回值:  
            float  
        '''
        if len(scoreRatio) == 0:
            return float(0)
        meanScore = sum(scoreRatio)/len(scoreRatio)
        return float(meanScore)


    def analysisMain(self, sortedLines):
        """  
        主分析函数,用于分析比赛数据
  
        Args:  
            self: 类实例的引用
            sortedLines: 字典,包含按规则排序的比赛行数据
  
        返回值:  
            None  
        """  
        nowTime = self.getNowTime()
        self.nowTime = nowTime # 后期增加,用于创建保存图标的文件夹
        # 若存在匹配数据
        if sortedLines:
            # 打印/保存当前系统时间
            self.finalData.append(f"\n\n\n#=======Saved_Time: {nowTime}=======================\n")
        else:
            self.errorsMessages.append("\nNo matched data: \nreason 1: Your teamname is wrong. \nreason 2: Your file is empty. \nreason 3: Your file does not exist.")
            return None
        for key in sortedLines.keys():
            winLines = list()  # 胜利的比赛行列表  
            loseLines = list()  # 失败的比赛行列表  
            peaceLines = list()  # 平局的比赛行列表  
            gainNum = 0  # 总进球数  
            loseNum = 0  # 总失球数  
            ourPoints = 0  # 我方总积分  
            oppPoints = 0  # 对方总积分  
            winCount = 0  # 胜利场数  
            peaceCount = 0  # 平局场数  
            loseCount = 0  # 失败场数  
            scoreRatio = list()  # 得分比率列表 

            self.finalData.append("\n***************************\n")
            # 打印/保存对战双方队伍名称
            self.finalData.append(f"{sortedLines[key][0][0]} -VS- {sortedLines[key][0][1]}\n")

            for sortedLine in sortedLines[key]:
                gainNum += int(sortedLine[2])
                loseNum += int(sortedLine[3])
                scoreRatio.append(self.calculateScoreGap(int(sortedLine[2]), int(sortedLine[3])))
                oneScore = self.calculateScoreCommenly(sortedLine)
                ourPoints += oneScore[0]
                oppPoints += oneScore[1]
                if int(sortedLine[2]) > int(sortedLine[3]):
                    winCount += 1
                    winLines.append(sortedLine)
                if int(sortedLine[2]) == int(sortedLine[3]):
                    peaceCount += 1
                    peaceLines.append(sortedLine)
                if int(sortedLine[2]) < int(sortedLine[3]):
                    loseCount += 1
                    loseLines.append(sortedLine)
            # 打印/保存WIN|PEACE|LOSE
            self.finalData.append("WIN\tPEACE\tLOSE\n")
            self.finalData.append(f"{winCount}\t{peaceCount}\t{loseCount}\n")
            # 打印/保存总场数 总进球数 总失球数
            self.finalData.append(f"-Total-:\t{len(sortedLines[key])}\n")
            self.finalData.append(f"-GainNum-:\t{gainNum}\n")
            self.finalData.append(f"-LoseNum-:\t{loseNum}\n")
            # 打印/保存净得球数
            self.finalData.append(f"-NetNum-:\t{gainNum-loseNum}\n")
            # =================================================================
            # 计算并打印/保存比分因子
            # 比分中存在越大分差时,其数值越大,用于分辨与对应队伍对战是否存在大比分情况,场数越多越精确
            scoreRatioFinal = round(self.mean(scoreRatio), 3)
            self.finalData.append(f"-Score_Gap-:\t{scoreRatioFinal}\n")
            # ===============用于绘制图表=======================
            self.finalScoreGapDict[sortedLines[key][0][1]] = scoreRatioFinal
            # =================================================================
            # 打印/保存双方积分
            self.finalData.append(f"Our_Points:\t{ourPoints}\n")
            self.finalData.append(f"Opp_Points:\t{oppPoints}\n")
            # 打印/保存胜率
            winProb0 = round(100*(ourPoints/(3*len(sortedLines[key]))), 3)# 严格模式胜率
            winProb1 = round(100*(winCount/len(sortedLines[key])), 3)
            winProb2 = round(100*(ourPoints/(ourPoints+oppPoints)), 3)
            
            self.finalData.append(f"Win_Prob:\t{winProb0}%\t[ourPoints/TotalCounts*3]\n")
            self.finalData.append(f"Win_Prob:\t{winProb1}%\t[winCounts/TotalCounts]\n")
            self.finalData.append(f"Win_Prob:\t{winProb2}%\t[ourPoints/TotalPoints]\n")
            # 打印/保存平均进球数 平均失球数
            avgGain = round(gainNum/len(sortedLines[key]), 3)
            avgLose = round(loseNum/len(sortedLines[key]), 3)
            self.finalData.append(f"Avg-Gain:\t{avgGain}\n")
            self.finalData.append(f"Avg-Lose:\t{avgLose}\n")
            # ===============用于绘制图表=======================
            self.winPro0Dict[sortedLines[key][0][1]] = (winProb0)
            self.winPro1Dict[sortedLines[key][0][1]] = (winProb1)
            self.winPro2Dict[sortedLines[key][0][1]] = (winProb2)
            self.avgGainDict[sortedLines[key][0][1]] = (avgGain)
            self.avgLoseDict[sortedLines[key][0][1]] = (avgLose)
            # =================================================
            self.finalData.append("--------------------------------------\n")
            self.finalData.append("\n+++ WIN +++\n")
            if winCount == 0:
                self.finalData.append("\n\tUnfortunately,you didn't win a game. Please continue to refuel.\n")
            else:
                for line in winLines:
                    if line[5]:
                        self.finalData.append(f"{line[4]}-{line[0]}_{line[2]}-vs-{line[1]}_{line[3]}\n")
                    else:
                        self.finalData.append(f"{line[4]}-{line[1]}_{line[3]}-vs-{line[0]}_{line[2]}\n")
            if peaceCount != 0:
                self.finalData.append("\n+++ PEACE +++\n")
                for line in peaceLines:
                    if line[5]:
                        self.finalData.append(f"\t{line[4]}-{line[0]}_{line[2]}-vs-{line[1]}_{line[3]}\n")
                    else:
                        self.finalData.append(f"\t{line[4]}-{line[1]}_{line[3]}-vs-{line[0]}_{line[2]}\n")
            self.finalData.append("\n+++ LOSE +++\n")
            if loseCount == 0:
                self.finalData.append("\n\tCongratulations, you are very good!\n")
            else:
                for line in loseLines:
                    if line[5]:
                        self.finalData.append(f"\t\t{line[4]}-{line[0]}_{line[2]}-vs-{line[1]}_{line[3]}\n")
                    else:
                        self.finalData.append(f"\t\t{line[4]}-{line[1]}_{line[3]}-vs-{line[0]}_{line[2]}\n")
            self.finalData.append("--------------------------------------\n")

    def saveScoreGapCharts(self):
        """  
        保存比分差距分析图到文件中
  
        Args:  
            self: 类实例对象
  
        Returns:  
            无返回值
        """
        df = DataFrame(list(self.finalScoreGapDict.items()), columns=['Team Name', 'Avg_Score_Gap']) 
        fig = line(df, x='Team Name', y='Avg_Score_Gap', title=f'OurTeam: {self.teamName} | Regardless of positive or negative,the larger the Score_Gap,the greater the difference in game scores')
        fig.update_layout(margin=dict(l=50, r=50, t=50, b=50))
        if not path.exists(f'./charts/{self.nowTime}'):
            makedirs(f'./charts/{self.nowTime}')
        fig.write_html(f'./charts/{self.nowTime}/Avg_Score_Gap.html')
        self.figObject.append(fig)
        # fig.show()


    def saveWinProbAndAvg(self):
        """  
        保存胜率和平均得分差分析图到文件中
  
        Args:  
            self: 类实例对象
  
        Returns:  
            无返回值
        """
        df0 = DataFrame.from_dict(self.winPro0Dict, orient='index', columns=['winPro0'])
        df1 = DataFrame.from_dict(self.winPro1Dict, orient='index', columns=['winPro1'])  
        df2 = DataFrame.from_dict(self.winPro2Dict, orient='index', columns=['winPro2'])
        df3 = DataFrame.from_dict(self.avgGainDict, orient='index', columns=['avgGain'])
        df4 = DataFrame.from_dict(self.avgLoseDict, orient='index', columns=['avgLose']) 
        fig = line()
        fig.add_trace(Scatter(x=df0.index, y=df0['winPro0'], mode='lines', name='winPro0[ourPoints/TotalCounts*3]')) 
        fig.add_trace(Scatter(x=df1.index, y=df1['winPro1'], mode='lines', name='winPro1[winCounts/TotalCounts]')) 
        fig.add_trace(Scatter(x=df2.index, y=df2['winPro2'], mode='lines', name='winPro2[ourPoints/TotalPoints]')) 
        fig.add_trace(Scatter(x=df3.index, y=df3['avgGain'], mode='lines', name='avgGain')) 
        fig.add_trace(Scatter(x=df4.index, y=df4['avgLose'], mode='lines', name='avgLose'))  
        fig.update_layout(title=f'OurTeam: {self.teamName}|The Win Rate and Average Score Difference Analysis Chart')  
        fig.update_xaxes(title="Team Name")
        fig.update_yaxes(title="WinPro/AvgGain/AvgLose")
        if not path.exists(f'./charts/{self.nowTime}'):
            makedirs(f'./charts/{self.nowTime}')
        fig.write_html(f'./charts/{self.nowTime}/Win_ProbAndAvg_Gain_Lose.html')
        self.figObject.append(fig)
        # fig.show()

    def showHTMLCharts(self):
        '''
        显示分析图
        '''
        for fig in self.figObject:
            fig.show()

    def saveFinalData(self):  
        """  
        保存最终分析数据到文件中
  
        Args:  
            self: 类实例的引用
  
        返回值:  
            一个元组,包含两个元素：  
                - 第一个元素是布尔值,表示保存是否成功
                - 第二个元素是异常对象(如果有的话),否则为None
        """  
        try:  
            if not path.exists("./finalResult/"):  
                makedirs("./finalResult/")  
  
            with open("./finalResult/analysisResults.txt", "a+") as finalResult:  
                for dataLine in self.finalData:  
                    finalResult.write(dataLine)  
            # None数据是为了使其为元组数据格式与发生错误时返回数据一致,方便后续函数处理
            self.saveScoreGapCharts()# 后期增加
            self.saveWinProbAndAvg()# 后期增加
            return (True, None)
        except Exception as e:  
            self.errorsMessages.append(f"An error occurred while saving data: {e}")
            return (False, e)

    def showFinalData(self):
        """  
        展示最终的分析数据
  
        Args:  
            self: 类实例的引用
  
        返回值:  
            如果finalData为空,则返回None;否则,在控制台上打印finalData中的每一行数据,没有返回值
        """
        if len(self.finalData) == 0:
            return None
        for dataLine in self.finalData:
            print(dataLine)
    
    def showErrorsMessages(self):
        """  
        展示错误消息
  
        Args:  
            self: 类实例的引用
  
        返回值:  
            如果errorsMessages列表为空,则返回None,否则,在控制台上打印errorsMessages中的每一条错误消息,没有返回值
        """  
        if len(self.errorsMessages) == 0:
            return None
        for errorMessage in self.errorsMessages:
            print(errorMessage)

    def getFinalData(self):
        """  
        获取最终的分析数据
  
        Args:  
            self: 类实例的引用
  
        返回值:  
            返回finalData列表,包含最终的分析数据
        """  
        return self.finalData
    
    def getErrorsMessages(self):
        """  
        获取错误消息列表
  
        Args:  
            self: 类实例的引用
  
        返回值:  
            返回errorsMessages列表,包含所有的错误消息
        """  
        return self.errorsMessages

    def runMain(self):
        """  
        运行主函数,执行整个分析流程
  
        Args:  
            self: 类实例的引用
  
        返回值:  
            无返回值,但会在过程中更新类的状态,包括finalData和errorsMessages列表
        """
        lines = self.getOriginalResult()
        oppTeamNames = self.getAllOppTeamNames(lines)
        matchedLines = self.getAllMatchedLines(lines)
        sortedLines = self.sortedByTeamName(oppTeamNames, matchedLines)
        self.analysisMain(sortedLines)



# if __name__ == '__main__':
#     Ana = AnalysisResult('./测试文件/result2.txt', 'YuShan2024')
#     Ana.runMain()
    # Ana.showFinalData()
    # print(Ana.finalScoreGapDict)
    # print(Ana.winPro1Dict)
    # Ana.saveScoreGapCharts()
    # Ana.saveWinProbAndAvg()
    # Ana.showHTMLCharts()
    # print(Ana.winPro1Dict.items())
    # Ana.showErrorsMessages()
