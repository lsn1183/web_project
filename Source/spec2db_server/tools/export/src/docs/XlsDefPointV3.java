package docs;

import org.apache.poi.xssf.usermodel.XSSFSheet;

import java.util.ArrayList;

public class XlsDefPointV3 extends XlsPointBase{
    public int titleRowIndex = 4;
    public int startRow = 5;

    public XlsDefPointV3(){
        this.version="v3";

        this.smallCat = new XlsDocInfo();
        this.smallCat.xIndex = 4;
        this.smallCat.yIndex = 6;
        this.smallCat.titleInfo.add("小分類");
        this.smallCat.dataType = "STR";


        this.basicReq = new XlsDocInfo();
        this.basicReq.xIndex = 4;
        this.basicReq.yIndex = 8;
        this.basicReq.titleInfo.add("基本要件");
        this.basicReq.dataType = "STR";

        this.dataID = new XlsDocInfo();
        this.dataID.xIndex = 4;
        this.dataID.yIndex = 2;
        this.dataID.titleInfo.add("TAGL要件定義ID");
        this.dataID.dataType = "FORMULAR_TAGLID";

        this.reviewResult = new XlsDocInfo();
        this.reviewResult.xIndex = 4;
        this.reviewResult.yIndex = 60;
        this.reviewResult.titleInfo.add("レビュー結果");
        this.reviewResult.dataType = "STR";

        this.pointNo = new XlsDocInfo();
        this.pointNo.xIndex = 4;
        this.pointNo.yIndex = 61;
        this.pointNo.titleInfo.add("指摘No.");
        this.pointNo.titleInfo.add("指摘No");
        this.pointNo.dataType = "STR";

        this.statusInfo = new XlsDocInfo();
        this.statusInfo.xIndex = 4;
        this.statusInfo.yIndex = 62;
        this.statusInfo.titleInfo.add("ステータス");
        this.statusInfo.dataType = "STR";

        this.commentInfo = new XlsDocInfo();
        this.commentInfo.xIndex = 4;
        this.commentInfo.yIndex = 63;
        this.commentInfo.titleInfo.add("コメント");
        this.commentInfo.dataType = "RICHSTR";

        this.leaderCheck = new XlsDocInfo();
        this.leaderCheck.xIndex = 4;
        this.leaderCheck.yIndex = 64;
        this.leaderCheck.titleInfo.add("リーダチェック");
        this.leaderCheck.dataType = "RICHSTR";

        this.leader2Check = new XlsDocInfo();
        this.leader2Check.xIndex = 4;
        this.leader2Check.yIndex = 65;
        this.leader2Check.titleInfo.add("リーダ２チェック");
        this.leader2Check.titleInfo.add("リーダ2チェック");
        this.leader2Check.dataType = "RICHSTR";

        this.finalCheck = new XlsDocInfo();
        this.finalCheck.xIndex = 4;
        this.finalCheck.yIndex = 66;
        this.finalCheck.titleInfo.add("最終チェック");
        this.finalCheck.dataType = "RICHSTR";

        this.actionUser = new XlsDocInfo();
        this.actionUser.xIndex = 4;
        this.actionUser.yIndex = 67;
        this.actionUser.titleInfo.add("担当");
        this.actionUser.dataType = "STR";

        this.priorityInfo = new XlsDocInfo();
        this.priorityInfo.xIndex = 4;
        this.priorityInfo.yIndex = 68;
        this.priorityInfo.titleInfo.add("優先度");
        this.priorityInfo.dataType = "STR";
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

        return resultList;
    }

    public boolean checkTitle(XSSFSheet ws) {
        return this.checkTitleBase(ws, this.titleRowIndex);
    }

    public int getFirstRowNum(){
        return this.startRow;
    }
}
