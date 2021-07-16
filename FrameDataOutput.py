import csv
import operator
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT

# 每一帧的数据类
class DrawCallData:
    def __init__(self):
        self.ID = 0  # 时间
        self.Name = 0  # 数值
        self.Parameters = ""  # 参数
        self.Clocks = 0
        self.SPRead = 0
        self.VertexRead = 0
        self.TextureRead = 0
        self.ReadTotal = 0
        self.WriteTotal = 0


def getAllDrawCalls(csv_path):
    csv_file = open(csv_path)
    csv_reader_lines = csv.reader(csv_file)
    drawCallDataArray = []
    for one_line in csv_reader_lines:
        if one_line[0].strip() == '':
            continue
        elif one_line[0].strip() == "ID":
            continue
        drawCall = DrawCallData()
        drawCall.ID = int(one_line[0].strip())
        drawCall.Name = one_line[1].strip()
        drawCall.Parameters = one_line[2].strip()
        if one_line[5].strip() == '':
            continue
        drawCall.Clocks = int(one_line[5].strip())
        drawCall.SPRead = int(one_line[7].strip())
        drawCall.VertexRead = int(one_line[9].strip())
        drawCall.TextureRead = int(one_line[8].strip())
        drawCall.WriteTotal = int(one_line[10].strip())
        drawCall.ReadTotal = int(one_line[6].strip())
        drawCallDataArray.append(drawCall)
    return drawCallDataArray


def getTopDrawCall(csv_path, word_path, topNum, Matrix):
    document = Document()
    document.add_heading('Snapdragon FrameData', level=0)

    allDrawCalls = getAllDrawCalls(csv_path)
    camp = ()
    if Matrix == "Read Total (Bytes)":
        camp = operator.attrgetter('ReadTotal')
    elif Matrix == "Texture Memory Read BW (Bytes)":
        camp = operator.attrgetter('WriteTotal')
    elif Matrix == "Clocks":
        camp = operator.attrgetter('Clocks')

    allDrawCalls.sort(key=camp, reverse=True)

    # 生成Top表格
    dataTable = document.add_table(topNum + 2, 7, style="Light Grid")
    dataTable.alignment = WD_TABLE_ALIGNMENT.CENTER  # 居中
    headLine = ["DrawCall", "Clocks", "SP Memory Read", "Vertex Memory Read", "Texture Memory Read BW",
                "Write Total", "Read Total"]

    for i in range(7):
        dataTable.cell(0, i).text = headLine[i]

    drawCallSum = DrawCallData()
    drawCallSum.ID = "Sum"
    for dc in allDrawCalls:
        drawCallSum.Clocks += dc.Clocks
        drawCallSum.SPRead += dc.SPRead
        drawCallSum.VertexRead += dc.VertexRead
        drawCallSum.TextureRead += dc.TextureRead
        drawCallSum.WriteTotal += dc.WriteTotal
        drawCallSum.ReadTotal += dc.ReadTotal

    dataTable.cell(topNum + 1, 0).text = drawCallSum.ID
    dataTable.cell(topNum + 1, 1).text = str(drawCallSum.Clocks)
    dataTable.cell(topNum + 1, 2).text = str(drawCallSum.SPRead)
    dataTable.cell(topNum + 1, 3).text = str(drawCallSum.VertexRead)
    dataTable.cell(topNum + 1, 4).text = str(drawCallSum.TextureRead)
    dataTable.cell(topNum + 1, 5).text = str(drawCallSum.WriteTotal)
    dataTable.cell(topNum + 1, 6).text = str(drawCallSum.ReadTotal)

    for i in range(topNum):
        drawCall = allDrawCalls[i]
        dataLine = [str(drawCall.ID),
                    str(drawCall.Clocks) + " ("+str("%.1f%%" % (drawCall.Clocks*100.0/drawCallSum.Clocks))+")",
                    str(drawCall.SPRead)+" ("+str("%.1f%%" % (drawCall.SPRead*100.0/1))+")",
                    str(drawCall.VertexRead)+" ("+str("%.1f%%" % (drawCall.VertexRead*100.0/drawCallSum.VertexRead))+")",
                    str(drawCall.TextureRead)+" ("+str("%.1f%%" % (drawCall.TextureRead*100.0/drawCallSum.TextureRead))+")",
                    str(drawCall.WriteTotal)+" ("+str("%.1f%%" % (drawCall.WriteTotal*100/drawCallSum.WriteTotal))+")",
                    str(drawCall.ReadTotal)+" ("+str("%.1f%%" % (drawCall.ReadTotal * 100/drawCallSum.ReadTotal))+")"]
        for j in range(7):
            dataTable.cell(i + 1, j).text = dataLine[j]

    document.save(word_path)
    print("Save SDFrameData")
