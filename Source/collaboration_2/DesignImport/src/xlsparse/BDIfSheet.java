package xlsparse;

import jsonobj.IfInfo;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;

import java.util.ArrayList;

public class BDIfSheet {
    public String[] keywordStr = new String[]{"IF仕様書"};
    public int startRowIndex = -1;
    public int endRowIndex = -1;
    public int ifNameColIndex = -1;
    public int ifParamColIndex = -1;
    public int ifReturnColIndex = -1;
    public int ifRemakeColIndex = -1;

    public ArrayList<IfInfo> parseSheet(XSSFSheet sheetInfo){
        ArrayList<IfInfo> retIfList = new ArrayList<>();
        if (sheetInfo.getSheetName().indexOf(this.keywordStr[0])<0) {
            return retIfList;
        }
        this.initRowColIndex(sheetInfo);
        if (ifNameColIndex < 0 || ifParamColIndex < 0 || ifReturnColIndex < 0 || ifRemakeColIndex < 0) {
            return retIfList;
        }
        for (int iRowIndex = startRowIndex; iRowIndex <= endRowIndex; iRowIndex++) {
            XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);
            IfInfo oneIfInfo = new IfInfo();
            if (rowInfo == null) {
                continue;
            }
            XSSFCell cellInfo = rowInfo.getCell(ifNameColIndex);
            if (cellInfo == null) {
                continue;
            }
            if (cellInfo.getStringCellValue().length() == 0) {
                continue;
            }
            oneIfInfo.ifName = cellInfo.getStringCellValue();
            cellInfo = rowInfo.getCell(ifParamColIndex);
            if (cellInfo!= null) {
                oneIfInfo.ifParam = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(ifReturnColIndex);
            if (cellInfo != null) {
                oneIfInfo.ifReturn = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(ifRemakeColIndex);
            if (cellInfo != null) {
                oneIfInfo.ifRemake = cellInfo.getStringCellValue();
            }

            retIfList.add(oneIfInfo);
        }

        return retIfList;
    }
    private void initRowColIndex(XSSFSheet sheetInfo) {
        for (int iRowIndex = 0; iRowIndex < sheetInfo.getLastRowNum(); iRowIndex++) {
            XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);
            if (rowInfo == null && startRowIndex < 0) {
                continue;
            }
            if (rowInfo == null && startRowIndex > 0){
            	endRowIndex = iRowIndex + 1;
                return;
            }
            endRowIndex = iRowIndex + 1;
            for (int iColIndex = 0; iColIndex < rowInfo.getLastCellNum(); iColIndex++) {
            	
                XSSFCell cellInfo = rowInfo.getCell(iColIndex);
                if (cellInfo == null) {
                	continue;
                }
//                if (cellInfo.getCellType() != Cell.CELL_TYPE_STRING) {
//                    continue;
//                }
                String cellValue = cellInfo.getStringCellValue();
                if (cellValue.equals("接口")) {
                    startRowIndex = iRowIndex + 1;
                    ifNameColIndex = iColIndex;
                } else if (cellValue.equals("参数")) {
                    ifParamColIndex = iColIndex;
                } else if (cellValue.equals("返回值")) {
                    ifReturnColIndex = iColIndex;
                } else if (cellValue.equals("接口说明")) {
                    ifRemakeColIndex = iColIndex;
                } 
            }
        }
    }
}
