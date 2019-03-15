package docs;

import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.xssf.usermodel.*;
import java.util.*;

public class XlsUtil {
    public String getStrVal(XSSFSheet ws, int rowIndex, int colIndex) {
        XSSFRow rowInfo = ws.getRow(rowIndex);
        if (rowInfo == null){
            return "";
        }
        XSSFCell cellInfo = rowInfo.getCell(colIndex);
        if (cellInfo == null){
            return "";
        }

        if (cellInfo.getCellTypeEnum() == CellType.NUMERIC) {
            Double nCellInfo = cellInfo.getNumericCellValue();
            if (nCellInfo.intValue()*1.0 == nCellInfo) {
                return Integer.toString(nCellInfo.intValue());
            }
            else{
                return Double.toString(nCellInfo.doubleValue());
            }
        }
        else if (cellInfo.getCellTypeEnum() == CellType.BLANK) {
            return "";
        }
        else if (cellInfo.getCellTypeEnum() == CellType.ERROR) {
            return "";
        }

        return cellInfo.getStringCellValue();
    }

    public int getIntVal(XSSFSheet ws, int rowIndex, int colIndex) {
        XSSFRow rowInfo = ws.getRow(rowIndex);
        if (rowInfo == null){
            return 0;
        }
        XSSFCell cellInfo = rowInfo.getCell(colIndex);
        if (cellInfo == null){
            return 0;
        }

        if (cellInfo.getCellTypeEnum() == CellType.NUMERIC) {
            Double nCellInfo = cellInfo.getNumericCellValue();
            return nCellInfo.intValue();
        }
        else if (cellInfo.getCellTypeEnum() == CellType.BLANK) {
            return 0;
        }

        return 0;
    }

    public double getDoubleVal(XSSFSheet ws, int rowIndex, int colIndex) {
        XSSFRow rowInfo = ws.getRow(rowIndex);
        if (rowInfo == null){
            return 0.0;
        }
        XSSFCell cellInfo = rowInfo.getCell(colIndex);
        if (cellInfo == null){
            return 0.0;
        }

        if (cellInfo.getCellTypeEnum() == CellType.NUMERIC) {
            Double nCellInfo = cellInfo.getNumericCellValue();
            return nCellInfo.doubleValue();
        }
        else if (cellInfo.getCellTypeEnum() == CellType.BLANK) {
            return 0.0;
        }

        return 0.0;
    }

    public String getCellDataType(XSSFSheet ws, int rowIndex, int colIndex){
        XSSFRow rowInfo = ws.getRow(rowIndex);
        if (rowInfo == null){
            return "BLANK";
        }
        XSSFCell cellInfo = rowInfo.getCell(colIndex);
        if (cellInfo == null){
            return "BLANK";
        }

        if (cellInfo.getCellTypeEnum() ==  CellType.NUMERIC){
            return "NUMBER";
        }

        return "STR";
    }

    public XlsRichValue getRichStrVal(XSSFSheet ws, int rowIndex, int colIndex) {
        XlsRichValue resultInfo = new XlsRichValue();

        XSSFRow rowInfo = ws.getRow(rowIndex);
        if (rowInfo == null){
            return resultInfo;
        }
        XSSFCell cellInfo = rowInfo.getCell(colIndex);
        if (cellInfo == null){
            return resultInfo;
        }

        resultInfo.strVal = this.getStrVal(ws, rowIndex, colIndex);
        XlsStyle cellXlsStyle = this.getXlsStyleByFont(cellInfo.getCellStyle().getFont());
        cellXlsStyle.startIndex = 0;
        cellXlsStyle.strLength = resultInfo.strVal.length();

        if (cellInfo.getCellTypeEnum() == CellType.NUMERIC ||
                cellInfo.getCellTypeEnum() == CellType.BLANK ||
                cellInfo.getCellTypeEnum() == CellType.ERROR){
            resultInfo.styleInfoList.add(cellXlsStyle);
            return resultInfo;
        }

        XSSFRichTextString richText = cellInfo.getRichStringCellValue();
        int richTextNum = richText.numFormattingRuns();
        if (richTextNum == 0) {
            resultInfo.styleInfoList.add(cellXlsStyle);
            return resultInfo;
        }

        for (int i=0; i < richTextNum; i++) {
            if (i>0) {
                cellXlsStyle = this.getXlsStyleByFont(richText.getFontOfFormattingRun(i));
            }

            cellXlsStyle.startIndex = richText.getIndexOfFormattingRun(i);
            cellXlsStyle.strLength = richText.getLengthOfFormattingRun(i);

            resultInfo.styleInfoList.add(cellXlsStyle);
        }

        return resultInfo;
    }

    private XlsStyle getXlsStyleByFont(XSSFFont fontInfo) {
        XlsStyle newStyle = new XlsStyle();
        if (fontInfo != null) {
            newStyle.fontName = fontInfo.getFontName();
            newStyle.fontSize = fontInfo.getFontHeightInPoints();
            if (fontInfo.getXSSFColor()!= null) {
                newStyle.fontColorRGB = fontInfo.getXSSFColor().getRGB();
            }
            newStyle.isBold = fontInfo.getBold();
            newStyle.isItalic = fontInfo.getItalic();
            newStyle.isStrike = fontInfo.getStrikeout();
        }

        return newStyle;
    }

}
