import WordOutput
import FrameDataOutput


# 数据换区间段过滤设置为None
timePeriods = None
timePeriods = [(120, 680)]
# 分割线区间段
slicedPeriods = None
# slicedPeriods = [25, 46, 52, 83, 109, 136, 156, 180, 243, 258, 282, 303, 330, 348, 361, 380]

# word = WordOutput.createSnapDragonDataDocx("22.csv", "22.docx", timePeriods, slicedPeriods)

frameResourcePath = "..\\Snapdragon2Word\\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
frameDoc = FrameDataOutput.getTopDrawCall("22.csv", "22.docx", 20, "Clocks", frameResourcePath)
