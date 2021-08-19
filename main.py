import WordOutput
import FrameDataOutput

# 数据换区间段过滤设置为None
# timePeriods = None
# timePeriods = [(30, 480)]
# word = WordOutput.createSnapDragonDataDocx("11.csv", "11.docx", timePeriods)

frameResourcePath = "..\\SnapDragonData2World\\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
frameDoc = FrameDataOutput.getTopDrawCall("11.csv", "11.docx", 10, "Read Total (Bytes)", frameResourcePath)