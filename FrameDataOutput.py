import csv
import operator
import os
from typing import List

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
from enum import Enum
from PIL import Image
from docx.shared import Cm

# 每一帧的数据类
class DrawCallData:
    def __init__(self):
        self.ID = 0  # 时间
        self.IDStr = "ID"
        self.Name = 0  # 数值
        self.NameStr = "Name"
        self.Parameters = ""  # 参数
        self.ParametersStr = "Parameters"
        self.Clocks = 0
        self.ClocksStr = "Clocks"
        self.SPRead = 0
        self.SPReadStr = "SP Memory Read (Bytes)"
        self.VertexRead = 0
        self.VertexReadStr = "Vertex Memory Read (Bytes)"
        self.TextureRead = 0
        self.TextureReadStr = "Texture Memory Read BW (Bytes)"
        self.ReadTotal = 0
        self.ReadTotalStr = "Read Total (Bytes)"
        self.WriteTotal = 0
        self.WriteTotalStr = "Write Total (Bytes)"


class ImageType(Enum):
    TEXTURE2D = 1
    MIPMAP = 2
    CUBEMAP = 4
    TEXTURE2DARRAY = 8
    TEXTURE3D = 16


class ImageInfo:
    def __init__(self):
        self.imagePath = ""
        self.imageName = ""
        self.imageType = ImageType.TEXTURE2D
        self.size = (-1, -1)
        self.isFrameCapture = False

def getAllDrawCalls(csv_path):
    csv_file = open(csv_path)
    csv_reader_lines = csv.reader(csv_file)
    drawCallDataArray = []
    idx = -1
    headline = []
    headIdxDic = {}
    for one_line in csv_reader_lines:
        idx = idx + 1
        if (one_line[0].strip() == '') or (one_line[5].strip() == ''):
            continue
        if idx == 0:
            headline = one_line.copy()
            for i, val in enumerate(headline):
                if val.strip() != "":
                    headIdxDic[val.strip()] = i
            continue
        drawCall = DrawCallData()
        drawCall.ID = int(one_line[headIdxDic[drawCall.IDStr]].strip())
        drawCall.Name = one_line[headIdxDic[drawCall.NameStr]].strip()
        drawCall.Parameters = one_line[headIdxDic[drawCall.ParametersStr]].strip()
        drawCall.Clocks = int(one_line[headIdxDic[drawCall.ClocksStr]].strip())
        drawCall.SPRead = int(one_line[headIdxDic[drawCall.SPReadStr]].strip())
        drawCall.VertexRead = int(one_line[headIdxDic[drawCall.VertexReadStr]].strip())
        drawCall.TextureRead = int(one_line[headIdxDic[drawCall.TextureReadStr]].strip())
        drawCall.WriteTotal = int(one_line[headIdxDic[drawCall.WriteTotalStr]].strip())
        drawCall.ReadTotal = int(one_line[headIdxDic[drawCall.ReadTotalStr]].strip())
        drawCallDataArray.append(drawCall)
    return drawCallDataArray


def getImageInfo(imageFoldPath, fileName: str):
    fullPath = imageFoldPath + "\\" + fileName
    imageInfo = ImageInfo()
    if os.path.isdir(fullPath):
        files = os.listdir(fullPath)
        imageInfo.imagePath = fullPath + "\\" + files[0]
        if fileName.__contains__("(Mipmap)"):
            imageInfo.imageType = ImageType.MIPMAP
            imageInfo.imageName = fileName.strip("(Mipmap)")
        elif fileName.__contains__("(Cubemap)"):
            imageInfo.imageType = ImageType.CUBEMAP
            imageInfo.imageName = fileName.strip("(Cubemap)")
        elif fileName.__contains__("(Texture3D)"):
            imageInfo.imageType = ImageType.TEXTURE3D
            imageInfo.imageName = fileName.strip("(Texture3D)")
        elif fileName.__contains__("(Texture2DArray)"):
            imageInfo.imageType = ImageType.TEXTURE2DARRAY
            imageInfo.imageName = fileName.strip("(Texture2DArray)")
    else:
        imageInfo.imagePath = fullPath
        imageInfo.imageName = fileName.strip(".png")
        imageInfo.imageType = ImageType.TEXTURE2D
        if fileName.startswith("DrawCall_"):
            imageInfo.isFrameCapture = True
    if imageInfo.imagePath != "":
        img = Image.open(imageInfo.imagePath)
        imageInfo.size = img.size
        return imageInfo
    else:
        return None


def getDrawCallImages(drawCall, imagePath):
    imageInfoList: List[ImageInfo] = []
    dcImageFoldPath = os.path.abspath(imagePath + "\\" + str(drawCall))
    if os.path.isdir(dcImageFoldPath):
        files = os.listdir(dcImageFoldPath)
        for file in files:
            imageInfo = getImageInfo(dcImageFoldPath, file)
            if imageInfo is not None:
                imageInfoList.append(imageInfo)
    else:
        print("No Image DrawCall " + str(drawCall))
    return imageInfoList

def getTaleValueStr(value, valueSum):
    return str(value) + " (" + str("%.1f%%" % (value * 100.0 / valueSum)) + ")"

def getTopDrawCall(csv_path, word_path, topNum, Matrix, frameResPath):
    document = Document()
    document.add_heading('Snapdragon FrameData', level=0)
    highLightIdx = -1
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
    document.add_heading('Summary', level=1)
    summaryParagraph = "单帧按" + Matrix + "排序，Top" + str(topNum) + "的DrawCall数据如下表"
    document.add_paragraph(summaryParagraph, style='Body Text')
    dataTable = document.add_table(topNum + 2, 6, style="Light Grid")
    dataTable.alignment = WD_TABLE_ALIGNMENT.CENTER  # 居中
    headLine = ["DrawCall", "Clocks", "Vertex Memory Read", "Texture Memory Read BW", "Write Total", "Read Total"]
    if Matrix == "Clocks":
        highLightIdx = 1
    elif Matrix == "Read Total (Bytes)":
        highLightIdx = 5

    for i in range(6):
        dataTable.cell(0, i).text = headLine[i]

    drawCallSum = DrawCallData()
    drawCallSum.ID = "Sum"
    for dc in allDrawCalls:
        drawCallSum.Clocks += dc.Clocks
        drawCallSum.VertexRead += dc.VertexRead
        drawCallSum.TextureRead += dc.TextureRead
        drawCallSum.WriteTotal += dc.WriteTotal
        drawCallSum.ReadTotal += dc.ReadTotal

    dataTable.cell(topNum + 1, 0).text = drawCallSum.ID
    dataTable.cell(topNum + 1, 1).text = str(drawCallSum.Clocks)
    dataTable.cell(topNum + 1, 2).text = str(drawCallSum.VertexRead)
    dataTable.cell(topNum + 1, 3).text = str(drawCallSum.TextureRead)
    dataTable.cell(topNum + 1, 4).text = str(drawCallSum.WriteTotal)
    dataTable.cell(topNum + 1, 5).text = str(drawCallSum.ReadTotal)
    shading_elm1 = parse_xml(r'<w:shd {} w:fill="FFDE3B"/>'.format(nsdecls('w')))
    dataTable.cell(topNum + 1, highLightIdx)._tc.get_or_add_tcPr().append(shading_elm1)

    for i in range(topNum):
        drawCall = allDrawCalls[i]
        dataLine = [str(drawCall.ID),
                    getTaleValueStr(drawCall.Clocks, drawCallSum.Clocks),
                    getTaleValueStr(drawCall.VertexRead, drawCallSum.VertexRead),
                    getTaleValueStr(drawCall.TextureRead, drawCallSum.TextureRead),
                    getTaleValueStr(drawCall.WriteTotal, drawCallSum.WriteTotal),
                    getTaleValueStr(drawCall.ReadTotal, drawCallSum.ReadTotal)]
        for j in range(6):
            dataTable.cell(i + 1, j).text = dataLine[j]
        shading_elm2 = parse_xml(r'<w:shd {} w:fill="FFDE3B"/>'.format(nsdecls('w')))
        dataTable.cell(i + 1, highLightIdx)._tc.get_or_add_tcPr().append(shading_elm2)

    # 单个DrawCall数据处理
    for i in range(topNum):
        dc = allDrawCalls[i]
        document.add_heading("DrawCall-" + str(dc.ID), level=1)
        imageInfoList = getDrawCallImages(dc.ID, frameResPath)
        dcTable = document.add_table(2, 3, style="Light Grid")
        dcTable.alignment = WD_TABLE_ALIGNMENT.CENTER  # 居中
        dcTable.cell(0,0).text = "帧截图"
        dcTable.cell(0,1).text = "相关纹理"
        dcTable.cell(0,2).text = "GPU数据"
        isFirstImage = True
        for imageInfo in imageInfoList:
            if imageInfo.isFrameCapture:
                pr1 = dcTable.cell(1,0).paragraphs[0].add_run()
                pic = pr1.add_picture(imageInfo.imagePath)
                scale1 = imageInfo.size[0] / 5
                pic.height = Cm(imageInfo.size[1]/scale1)
                pic.width = Cm(5)
                dcTable.cell(1, 0).add_paragraph("Size [{0}x{1}]".format(imageInfo.size[0], imageInfo.size[1]))
            else:
                p1 = None
                if isFirstImage:
                    isFirstImage = False
                    p1 = dcTable.cell(1,1).paragraphs[0]
                else:
                    p1 = dcTable.cell(1,1).add_paragraph()
                pic = p1.add_run().add_picture(imageInfo.imagePath)
                pic.height = Cm(2)
                pic.width = Cm(2)
                p1.add_run("{0} [({1}),{2}x{3}]".format(imageInfo.imageName, imageInfo.imageType.name, imageInfo.size[0], imageInfo.size[1]))

        drawCall = allDrawCalls[i]
        dcTable.cell(1, 2).paragraphs[0].add_run("Read Total:"+getTaleValueStr(drawCall.ReadTotal, drawCallSum.ReadTotal))
        dcTable.cell(1, 2).paragraphs[0].add_run("\nWrite Total:" + getTaleValueStr(drawCall.WriteTotal, drawCallSum.WriteTotal))
        dcTable.cell(1, 2).paragraphs[0].add_run("\nClocks:" + getTaleValueStr(drawCall.Clocks, drawCallSum.Clocks))
        dcTable.cell(1, 2).paragraphs[0].add_run("\nTexture Read:" + getTaleValueStr(drawCall.TextureRead, drawCallSum.TextureRead))
        dcTable.cell(1, 2).paragraphs[0].add_run("\nVertex Read:" + getTaleValueStr(drawCall.VertexRead, drawCallSum.VertexRead))

    document.save(word_path)
    print("Save SDFrameData")
