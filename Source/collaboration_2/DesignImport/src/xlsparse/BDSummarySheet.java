package xlsparse;


import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;

import utils.XlsUtil;



public class BDSummarySheet {
	public String[] keywordStr = new String[]{"表紙"};
    public int startRowIndex = -1;
    private XlsUtil xlsUtil = new XlsUtil();
    
    public String parseSheet(XSSFSheet sheetInfo){
    	String summary = "";
    	if (sheetInfo.getSheetName().indexOf(this.keywordStr[0])<0) {
            return summary;
        }
    	this.initRowColIndex(sheetInfo);
    	if (startRowIndex < 0) {
    		return summary;
    	}
    	XSSFRow rowInfo = sheetInfo.getRow(startRowIndex);
    	for (int iRowIndex = startRowIndex; iRowIndex <= sheetInfo.getLastRowNum(); iRowIndex++) {
            if (sheetInfo.getRow(iRowIndex) == null) {
                continue;
            }
            String lineStr = "";
            for (int iColIndex=1; iColIndex < sheetInfo.getRow(iRowIndex).getLastCellNum(); iColIndex++) {
                lineStr = lineStr + this.xlsUtil.getCellStrInfo(sheetInfo, iRowIndex, iColIndex);
            }
            if (lineStr.length()>0) {
            	if(summary.equals("")) {
            		summary = lineStr;
            	}
            	else {
            		summary = summary +"\n" + lineStr ;
            	}
            }
        }
    	return summary;
    }
    
    private void initRowColIndex(XSSFSheet sheetInfo) {
    	for (int iRowIndex = 0; iRowIndex < sheetInfo.getLastRowNum(); iRowIndex++) {
    		XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);
    		if (rowInfo == null) {
                continue;
            }
    		for (int iColIndex = 0; iColIndex < rowInfo.getLastCellNum(); iColIndex++) {
                XSSFCell cellInfo = rowInfo.getCell(iColIndex);
                if (cellInfo == null) {
                	continue;
                }
//                if (cellInfo.getCellType() != Cell.CELL_TYPE_STRING) {
//                    continue;
//                }
                String cellValue = cellInfo.getStringCellValue();
                if (cellValue.indexOf("概要") >= 0) {
                	startRowIndex = iRowIndex + 1;
                	return;
                } 
            }
    	}
    	
    }
}
