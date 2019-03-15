package xlsparse;

import jsonobj.BasicDesignInfo;
import jsonobj.IfInfo;
import jsonobj.ImageInfo;
import jsonobj.ReqFuncInfo;
import jsonobj.SectionInfo;

import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;

public class BasicDesignXls {
    private XSSFWorkbook workBook = null;

    private BasicDesignInfo BDInfo = new BasicDesignInfo();

    public BasicDesignXls(String xlsFileName) throws Exception {
        File checkFile = new File(xlsFileName);
        if (checkFile.exists() && checkFile.isFile()) {
           this.workBook = new XSSFWorkbook(new FileInputStream(xlsFileName));
        }
    }

    public BasicDesignInfo doParse(String imgPath) throws Exception{
        if (this.workBook == null && this.workBook == null) {
            return this.BDInfo;
        }

        int sheetNum = this.workBook.getNumberOfSheets();

        for (int iSheetIndex = 0; iSheetIndex < sheetNum; iSheetIndex++) {

            XSSFSheet sheetInfo = this.workBook.getSheetAt(iSheetIndex);
            if (BDInfo.basicDesignSummary.equals("")){
            	this.BDInfo.basicDesignSummary = new BDSummarySheet().parseSheet(sheetInfo);
            }
            ArrayList<ReqFuncInfo> retFuncStrList = new BDReqFuncSheet().parseSheet(sheetInfo);
            for (ReqFuncInfo iReqInfo : retFuncStrList) {
                this.BDInfo.reqFuncList.add(iReqInfo);
            }
            ArrayList<IfInfo> retIfStrList = new BDIfSheet().parseSheet(sheetInfo);
            for (IfInfo ifInfo : retIfStrList){
                this.BDInfo.ifList.add(ifInfo);
            }
            ArrayList<SectionInfo>  blockImgList = new BDBlockSheet().parseSheet(sheetInfo, imgPath);
            for (SectionInfo blockImg : blockImgList) {
                this.BDInfo.blockImgList.add(blockImg);
            }
            ArrayList<SectionInfo> classImgList = new BDClassSheet().parseSheet(sheetInfo, imgPath);
            for (SectionInfo classImg : classImgList) {
                this.BDInfo.classImaList.add(classImg);
            }
            ArrayList<SectionInfo> usecaseImaList = new BDUsecaseSheet().parseSheet(sheetInfo, imgPath);
            for (SectionInfo usecaseIma : usecaseImaList){
                this.BDInfo.usecaseImaList.add(usecaseIma);
            }
            ArrayList<SectionInfo> sequenceImaList = new BDSequenceSheet().parseSheet(sheetInfo, imgPath);
            for (SectionInfo sequenceIma : sequenceImaList){
                this.BDInfo.sequenceImaList.add(sequenceIma);
            }
            ArrayList<SectionInfo> activityImaList = new BDActivitySheet().parseSheet(sheetInfo, imgPath);
            for (SectionInfo activityIma : activityImaList){
                this.BDInfo.activityImaList.add(activityIma);
            }
            ArrayList<SectionInfo> stateImaList = new BDStateSheet().parseSheet(sheetInfo, imgPath);
            for (SectionInfo stateIma : stateImaList){
                this.BDInfo.stateImaList.add(stateIma);
            }
        }

        return this.BDInfo;
    }


}
