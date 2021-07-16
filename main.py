import WordOutput
import FrameDataOutput

# 数据换区间段过滤设置为None
# timePeriods = None
timePeriods = [(185, 615)]
word = WordOutput.createSnapDragonDataDocx("datas/mzc.csv", "mzc.docx", timePeriods)

# "Read Total (Bytes)"、“Clocks”
# frameDoc = FrameDataOutput.getTopDrawCall("P2F1.csv", "P2F1.docx", 10, "Read Total (Bytes)")