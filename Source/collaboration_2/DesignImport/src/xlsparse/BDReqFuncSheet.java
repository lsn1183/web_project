package xlsparse;

import jsonobj.ReqFuncInfo;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;

import java.util.ArrayList;

public class BDReqFuncSheet {
    public String[] keywordStr = new String[]{"软件需求一览"};
    public int startRowIndex = -1;
    public int endRowIndex = -1;
    public int funcNameColIndex = -1;   //式样书名称
    public int funcNameTypeIndex = -1;  //式样书类型
    public int funcIDColIndex = -1;  //机能点
    public int funcUCNoIndex = -1;   //usecase编号
//    public int funcVerColIndex = -1;
//    public int funcChapterColIndex = -1;

    public ArrayList<ReqFuncInfo> parseSheet(XSSFSheet sheetInfo) {
        ArrayList<ReqFuncInfo> retReqFuncList = new ArrayList<>();

        if (sheetInfo.getSheetName().indexOf(this.keywordStr[0])<0) {
            return retReqFuncList;
        }
        this.initRowColIndex(sheetInfo);

        if (funcNameColIndex < 0 || funcNameTypeIndex < 0 || funcIDColIndex < 0 || funcUCNoIndex < 0) {
            return retReqFuncList;
        }
        for (int iRowIndex = startRowIndex; iRowIndex <= endRowIndex; iRowIndex++) {
            XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);
            ReqFuncInfo oneReqFunc = new ReqFuncInfo();
            if (rowInfo == null) {
                continue;
            }

            XSSFCell cellInfo = rowInfo.getCell(funcNameColIndex);
            if (cellInfo == null) {
                continue;
            }
            if (cellInfo.getStringCellValue().length() == 0) {
                continue;
            }
            oneReqFunc.funcFileName = cellInfo.getStringCellValue();
            cellInfo = rowInfo.getCell(funcIDColIndex);
            if (cellInfo!= null) {
                oneReqFunc.funcID = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(funcNameTypeIndex);
            if (cellInfo != null) {
                oneReqFunc.funcType = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(funcUCNoIndex);
            if (cellInfo != null) {
                oneReqFunc.usecaseNo = cellInfo.getStringCellValue();
            }
            retReqFuncList.add(oneReqFunc);
        }
        return retReqFuncList;
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
//                if (cellInfo.getCellType()!= Cell.CELL_TYPE_STRING) {
//                    continue;
//                }
                String cellValue = cellInfo.getStringCellValue();
                if (cellValue.indexOf("式样书类型")>=0) {
                    startRowIndex = iRowIndex+1;
                    funcNameTypeIndex = iColIndex;
                }
                else if (cellValue.indexOf("式样书名称")>=0) {
                	funcNameColIndex = iColIndex;
                }
                else if (cellValue.indexOf("机能点")>=0) {
                	funcIDColIndex = iColIndex;
                }
                else if(cellValue.indexOf("UsecaseNo")>=0) {
                	funcUCNoIndex = iColIndex;
                }
            }
        }
    }


}
