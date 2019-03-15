package point;

import docs.*;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;

public class PointContent{
    private String docType = "";
    private XSSFWorkbook wb = null;
    private XSSFSheet ws = null;
    private XlsUtil xlsUtil = new XlsUtil();
    private XlsPointBase pointDoc = null;

    public PointContent(String xlsFileName, String fileType) throws Exception {
        this.docType = fileType;
        File excelFile = new File(xlsFileName);
        this.wb = new XSSFWorkbook(new FileInputStream(excelFile));
        if (this.docType.equals("HU")) {
            this.ws = this.wb.getSheet("HU要件定義書");
            this.pointDoc = new XlsHuPointV3();
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsHuPointV2();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsHuPointV1();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = null;
                return;
            }
        }
        else if (this.docType.equals("DEF")) {
            this.ws = this.wb.getSheet("TAGL要件定義");
            this.pointDoc = new XlsDefPointV7();
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsDefPointV6();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsDefPointV5();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsDefPointV4();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsDefPointV3();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsDefPointV2();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsDefPointV1();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = null;
                return;
            }
        }
        else if (this.docType.equals("ANA")) {
            this.ws = this.wb.getSheet("TAGL要件分析");
            this.pointDoc = new XlsAnaPointV3();
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsAnaPointV2();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = new XlsAnaPointV1();
            }
            if (this.pointDoc.checkTitle(this.ws) == false){
                this.pointDoc = null;
                return;
            }
        }
    }

    public boolean checkDocIsOk() {
        return this.pointDoc != null;
    }

    public int getLastRowNum(){
        return this.ws.getLastRowNum();
    }

    public int getFirstRowNum(){
        return pointDoc.getFirstRowNum();
    }

    public ArrayList<PointInfo> getOneRow(int rowIndex){
        ArrayList<PointInfo> rowPointInfo = new ArrayList<PointInfo>();

        ArrayList<XlsDocInfo> infoList = pointDoc.getInfoList();
        for (int i=0; i<infoList.size();i++){
            XlsDocInfo docInfo = infoList.get(i);
            PointInfo oneInfo = new PointInfo();
            oneInfo.titleInfo = docInfo.titleInfo.get(0);
            oneInfo.xlsDataType = this.xlsUtil.getCellDataType(this.ws, rowIndex, docInfo.yIndex);
            if (docInfo.dataType.equals("FORMULAR_HUID")){
                oneInfo.richVal =  new XlsRichValue();
                oneInfo.richVal.strVal = String.format("%s.%s",
                        this.xlsUtil.getStrVal(this.ws, rowIndex, 1),
                        this.xlsUtil.getStrVal(this.ws, rowIndex, 13));
            }
            else if (docInfo.dataType.equals("FORMULAR_TAGLID")){
                oneInfo.richVal =  new XlsRichValue();
                oneInfo.richVal.strVal = String.format("%s.%s",
                        this.xlsUtil.getStrVal(this.ws, rowIndex, 1),
                        this.xlsUtil.getStrVal(this.ws, rowIndex, 3));
            }
            else {
                oneInfo.richVal = this.xlsUtil.getRichStrVal(this.ws, rowIndex, docInfo.yIndex);
            }
            rowPointInfo.add(oneInfo);
        }

        return rowPointInfo;
    }

    public String getValByTitle(ArrayList<PointInfo> rowPointList, String titleName){
        for (int i=0; i< rowPointList.size();i++){
            PointInfo pointInfo = rowPointList.get(i);
            if (titleName == pointInfo.titleInfo){
                return pointInfo.richVal.strVal;
            }
        }

        return "";
    }

}
