package docs;
import docs.XlsPointBase;
import docs.XlsDocInfo;
import docs.XlsUtil;
import org.apache.poi.xssf.usermodel.XSSFSheet;

import java.util.ArrayList;

public class XlsHuPointV2 extends XlsPointBase{
    public int titleRowIndex = 8;
    public int startRow = 9;

    public XlsHuPointV2(){
        this.version="v2";

        this.smallCat = new XlsDocInfo();
        this.smallCat.xIndex = 8;
        this.smallCat.yIndex = 4;
        this.smallCat.titleInfo.add("小分類");
        this.smallCat.dataType = "STR";


        this.basicReq = new XlsDocInfo();
        this.basicReq.xIndex = 8;
        this.basicReq.yIndex = 6;
        this.basicReq.titleInfo.add("基本要件");
        this.basicReq.dataType = "STR";

        this.dataID = new XlsDocInfo();
        this.dataID.xIndex = 8;
        this.dataID.yIndex = 12;
        this.dataID.titleInfo.add("H/U要件定義ID");
        this.dataID.dataType = "FORMULAR_HUID";

        this.reviewResult = new XlsDocInfo();
        this.reviewResult.xIndex = 8;
        this.reviewResult.yIndex = 79;
        this.reviewResult.titleInfo.add("レビュー結果");
        this.reviewResult.dataType = "STR";

        this.pointNo = new XlsDocInfo();
        this.pointNo.xIndex = 8;
        this.pointNo.yIndex = 80;
        this.pointNo.titleInfo.add("指摘No.");
        this.pointNo.dataType = "STR";

        this.statusInfo = new XlsDocInfo();
        this.statusInfo.xIndex = 8;
        this.statusInfo.yIndex = 81;
        this.statusInfo.titleInfo.add("ステータス");
        this.statusInfo.dataType = "STR";

        this.commentInfo = new XlsDocInfo();
        this.commentInfo.xIndex = 8;
        this.commentInfo.yIndex = 82;
        this.commentInfo.titleInfo.add("コメント");
        this.commentInfo.dataType = "RICHSTR";

        this.leaderCheck = new XlsDocInfo();
        this.leaderCheck.xIndex = 8;
        this.leaderCheck.yIndex = 83;
        this.leaderCheck.titleInfo.add("リーダチェック");
        this.leaderCheck.dataType = "RICHSTR";

        this.leader2Check = new XlsDocInfo();
        this.leader2Check.xIndex = 8;
        this.leader2Check.yIndex = 84;
        this.leader2Check.titleInfo.add("リーダ２チェック");
        this.leader2Check.titleInfo.add("リーダ2チェック");
        this.leader2Check.dataType = "RICHSTR";

        this.finalCheck = new XlsDocInfo();
        this.finalCheck.xIndex = 8;
        this.finalCheck.yIndex = 85;
        this.finalCheck.titleInfo.add("最終チェック");
        this.finalCheck.dataType = "RICHSTR";

        this.actionUser = new XlsDocInfo();
        this.actionUser.xIndex = 8;
        this.actionUser.yIndex = 86;
        this.actionUser.titleInfo.add("担当");
        this.actionUser.dataType = "STR";

        this.priorityInfo = new XlsDocInfo();
        this.priorityInfo.xIndex = 8;
        this.priorityInfo.yIndex = 87;
        this.priorityInfo.titleInfo.add("優先度");
        this.priorityInfo.dataType = "STR";

        this.pointDate = new XlsDocInfo();
        this.pointDate.xIndex = 8;
        this.pointDate.yIndex = 88;
        this.pointDate.titleInfo.add("指摘提出日");
        this.pointDate.dataType = "STR";

        this.fixedInfo = new XlsDocInfo();
        this.fixedInfo.xIndex = 8;
        this.fixedInfo.yIndex = 89;
        this.fixedInfo.titleInfo.add("修正済み");
        this.fixedInfo.dataType = "STR";

        this.suntecMemo = new XlsDocInfo();
        this.suntecMemo.xIndex = 8;
        this.suntecMemo.yIndex = 90;
        this.suntecMemo.titleInfo.add("Suntec備考");
        this.suntecMemo.dataType = "STR";
    }

    public ArrayList<XlsDocInfo> getInfoList() {
        ArrayList<XlsDocInfo> resultList = new ArrayList<XlsDocInfo>();

        resultList.add(this.smallCat);
        resultList.add(this.basicReq);
        resultList.add(this.dataID);
        resultList.add(this.reviewResult);
        resultList.add(this.pointNo);
        resultList.add(this.statusInfo);
        resultList.add(this.commentInfo);
        resultList.add(this.leaderCheck);
        resultList.add(this.leader2Check);
        resultList.add(this.finalCheck);
        resultList.add(this.actionUser);
        resultList.add(this.priorityInfo);
        resultList.add(this.pointDate);
        resultList.add(this.fixedInfo);
        resultList.add(this.suntecMemo);

        return resultList;
    }

    public boolean checkTitle(XSSFSheet ws) {
        return this.checkTitleBase(ws, this.titleRowIndex);
    }

    public int getFirstRowNum(){
        return this.startRow;
    }
}
