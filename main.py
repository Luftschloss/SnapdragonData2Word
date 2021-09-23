import WordOutput
import FrameDataOutput

# 数据换区间段过滤设置为None
timePeriods = None
timePeriods = [(310, 925)]
# 分割线区间段
slicedPeriods = None
# slicedPeriods = [315]

word = WordOutput.createSnapDragonDataDocx("basketball.csv", "basketball.docx", timePeriods, slicedPeriods)

frameResourcePath = "..\\SnapDragonData2World\\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
# frameDoc = FrameDataOutput.getTopDrawCall("f3.csv", "f3.docx", 20, "Read Total (Bytes)", frameResourcePath)