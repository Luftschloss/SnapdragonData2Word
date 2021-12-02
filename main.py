import WordOutput
import FrameDataOutput


# 数据换区间段过滤设置为None
timePeriods = None
timePeriods = [(136, 205)]
# 分割线区间段
slicedPeriods = None
slicedPeriods = [161, 188]

word = WordOutput.createSnapDragonDataDocx("Nova.csv", "12.docx", timePeriods, slicedPeriods)

frameResourcePath = "..\\Snapdragon2Word\\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
# frameDoc = FrameDataOutput.getTopDrawCall("11.csv", "11.docx", 15, "Read Total (Bytes)", frameResourcePath)
