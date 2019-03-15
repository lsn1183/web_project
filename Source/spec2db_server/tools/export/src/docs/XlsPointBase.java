package docs;
import org.apache.poi.xssf.usermodel.XSSFSheet;

import java.util.*;

public class XlsPointBase {
    protected String version="";
    protected XlsDocInfo smallCat = null;
    protected XlsDocInfo basicReq = null;
    protected XlsDocInfo dataID = null;
    protected XlsDocInfo reviewResult = null;
    protected XlsDocInfo pointNo = null;
    protected XlsDocInfo statusInfo = null;
    protected XlsDocInfo commentInfo = null;
    protected XlsDocInfo leaderCheck = null;
    protected XlsDocInfo leader2Check = null;
    protected XlsDocInfo finalCheck = null;
    protected XlsDocInfo actionUser = null;
    protected XlsDocInfo priorityInfo = null;
    protected XlsDocInfo pointDate = null;
    protected XlsDocInfo suntecStatus = null;
    protected XlsDocInfo fixedInfo = null;
    protected XlsDocInfo suntecMemo = null;
    protected XlsDocInfo arlLinkPoint = null;
    protected XlsDocInfo arlCannotModify = null;

    public ArrayList<XlsDocInfo> getInfoList() {
        ArrayList<XlsDocInfo> resultList = new ArrayList<XlsDocInfo>();
        return resultList;
    }

    protected boolean checkTitleBase(XSSFSheet ws, int titleRowIndex) {
        boolean checkResult = true;

        XlsUtil xlsUtil = new XlsUtil();

        ArrayList<XlsDocInfo> infoList = this.getInfoList();
        for (int i=0; i<infoList.size();i++){
            XlsDocInfo docInfo = infoList.get(i);
            boolean titleCheck = false;
            String xlsVal = xlsUtil.getStrVal(ws, titleRowIndex,docInfo.yIndex);

            for (int iTitle=0; iTitle< docInfo.titleInfo.size();iTitle++){
                String nowTitle = docInfo.titleInfo.get(iTitle);
                if (xlsVal.indexOf(nowTitle)>=0){
                    titleCheck = true;
                    break;
                }
//                else{
//                    System.out.println(xlsVal);
//                    System.out.println(docInfo.titleInfo);
//                }
            }

            checkResult = checkResult&titleCheck;
        }

        return checkResult;
    }

    public int getFirstRowNum(){
        return 0;
    }

    public boolean checkTitle(XSSFSheet ws) {
        return false;
    }


}
