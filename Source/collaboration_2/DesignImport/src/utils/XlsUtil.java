package utils;

import org.apache.poi.POIXMLDocumentPart;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.xssf.usermodel.*;
import xlsparse.XlsImageInfo;

import java.util.ArrayList;
import java.util.List;

public class XlsUtil {
    public ArrayList<XlsImageInfo> getSheetImgList(XSSFSheet sheetInfo) {
        ArrayList<XlsImageInfo> retImgList = new ArrayList<XlsImageInfo>();

        for (POIXMLDocumentPart dr : sheetInfo.getRelations()) {
            if (dr instanceof XSSFDrawing) {
                XSSFDrawing drawing = (XSSFDrawing) dr;
                List<XSSFShape> shapes = drawing.getShapes();
                for (XSSFShape shape : shapes) {
                    XSSFPicture pic = (XSSFPicture) shape;
                    XSSFClientAnchor anchor = pic.getPreferredSize();

                    XlsImageInfo oneImageInfo = new XlsImageInfo();
                    oneImageInfo.picData = pic.getPictureData();
                    oneImageInfo.startColIndex = anchor.getCol1();
                    oneImageInfo.endColIndex = anchor.getCol2();
                    oneImageInfo.startRowIndex = anchor.getRow1();
                    oneImageInfo.endRowIndex = anchor.getRow2();

                    retImgList.add(oneImageInfo);
                }
            }
        }

        return retImgList;

    }

    public String getCellStrInfo(XSSFSheet sheetInfo, int iRowIndex, int iColIndex) {
        XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);

        if (rowInfo == null) {
            return "";
        }

        XSSFCell cellInfo = rowInfo.getCell(iColIndex);
        if (cellInfo == null) {
            return "";
        }

        if (cellInfo.getCellType()==Cell.CELL_TYPE_STRING) {
            return cellInfo.getStringCellValue();
        }
        else if (cellInfo.getCellType() == Cell.CELL_TYPE_NUMERIC) {
            return String.format("%f", cellInfo.getNumericCellValue());
        }


        return "";
    }
}
