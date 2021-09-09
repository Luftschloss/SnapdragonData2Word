import WordOutput
import FrameDataOutput

# 数据换区间段过滤设置为None
timePeriods = None
timePeriods = [(180, 920)]
# 分割线数据
slicedPeriods = None
slicedPeriods = [300, 450]

word = WordOutput.createSnapDragonDataDocx("23.csv", "23.docx", timePeriods, slicedPeriods)

frameResourcePath = "..\\SnapDragonData2World\\FrameCapture"
# "Read Total (Bytes)"、“Clocks”
# frameDoc = FrameDataOutput.getTopDrawCall("f3.csv", "f3.docx", 20, "Read Total (Bytes)", frameResourcePath)