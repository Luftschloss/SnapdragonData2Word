import WordOutput
import FrameDataOutput
# import Snapdragon2WordWindow

# 数据换区间段过滤设置为None
timePeriods = None
timePeriods = [(35, 179)]
# 分割线区间段
slicedPeriods = None
slicedPeriods = [40, 68, 95, 120, 149, 176]

word = WordOutput.createSnapDragonDataDocx("FSR.csv", "FSR.docx", timePeriods, slicedPeriods)

frameResourcePath = "D:\WorkSpace\Snapdragon2Word\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
# frameDoc = FrameDataOutput.getTopDrawCall("c3.csv", "c3.docx", 20, "Read Total (Bytes)", frameResourcePath)
