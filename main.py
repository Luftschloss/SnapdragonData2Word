import WordOutput
import FrameDataOutput

# 数据换区间段过滤设置为None
timePeriods = None
timePeriods = [(100, 510)]
# 分割线区间段
slicedPeriods = None
slicedPeriods = [130, 162, 210, 240, 280, 305, 345, 375, 425, 445, 470, 490]

# word = WordOutput.createSnapDragonDataDocx("12.csv", "12.docx", timePeriods, slicedPeriods)

frameResourcePath = "..\\Snapdragon2Word\\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
frameDoc = FrameDataOutput.getTopDrawCall("11.csv", "11.docx", 15, "Read Total (Bytes)", frameResourcePath)