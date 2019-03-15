package xlsparse;

import jsonobj.IfInfo;
import jsonobj.ImageInfo;
import jsonobj.ResourceInfo;
import jsonobj.SectionInfo;
import jsonobj.UCTableInfo;

import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;


import utils.XlsUtil;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;

import javax.imageio.ImageIO;

public class BDBlockSheet {
    public String[] keywordStr = new String[]{"Block"};
    private XlsUtil xlsUtil = new XlsUtil();
    public String imgType = "block";
    public int startRowIndex = -1;
    public int endRowIndex = -1;
    public int ucNoColIndex = -1;
    public int ucTitleColIndex = -1;
    public int ucIntroduceColIndex = -1;
    public int seqNoColIndex = -1;
    public int seqSheetColIndex = -1;
    public int rsTitleColIndex = -1;
    public int rsValueColIndex = -1;
    

    public ArrayList<SectionInfo> parseSheet(XSSFSheet sheetInfo, String imgPath) throws Exception{
        ArrayList<SectionInfo> sectionInfo = new ArrayList<>();
        if (checkSheetInfo(sheetInfo) == false) {
            return sectionInfo;
        }
        String sheetName = sheetInfo.getSheetName();
        SectionInfo section = new SectionInfo();
        section.sheetName = sheetName;
        ArrayList<XlsImageInfo> xlsImgList = this.xlsUtil.getSheetImgList(sheetInfo);
        if (xlsImgList.size() == 0) {
        	return sectionInfo;
        }
        ImageInfo oneImgInfo = new ImageInfo();
        for (int iIndex = 0; iIndex < xlsImgList.size(); iIndex++) {
            XlsImageInfo xlsImgInfo = xlsImgList.get(iIndex);
            if(iIndex == 0) {
	            int titleStartRow = xlsImgInfo.startRowIndex-1;
	            for (int i = titleStartRow; i >= 0; i--) {
	            	XSSFRow rowInfo = sheetInfo.getRow(i);
            		if(rowInfo!=null) {
            			for (int iColIndex = i; iColIndex < rowInfo.getLastCellNum(); iColIndex++) {
        	                XSSFCell cellInfo = rowInfo.getCell(iColIndex);
        	                if (cellInfo == null) {
        	                	continue;
        	                }
        	                String title = cellInfo.getStringCellValue();
        	                oneImgInfo.imgTitle = title.replace("■", "");
        	                break;
        	            }
            			break;
            		}	            				            	
	            }
            }
            byte[] data = xlsImgInfo.picData.getData();
            String extName = xlsImgInfo.picData.suggestFileExtension();
            String filePath = imgPath + "/"+ sheetName + "_"+imgType + iIndex+"." + extName;
            oneImgInfo.imgFilePath.add(filePath);
            FileOutputStream out = new FileOutputStream(filePath);
            out.write(data);
            out.close();
        }
        int iStartIntroRow = xlsImgList.get(xlsImgList.size()-1).endRowIndex + 1;
        int iEndIntroRow = sheetInfo.getLastRowNum()+1;
        if(sheetName.indexOf("UseCase") >= 0) {
        	this.initUcRowColIndex(sheetInfo);
        	if (ucNoColIndex > 0 && ucTitleColIndex > 0 && ucIntroduceColIndex > 0 
        			&& seqNoColIndex > 0 && seqSheetColIndex > 0) {
        		iEndIntroRow = startRowIndex-2;
        		section.ucInfo = getUcTable(sheetInfo, startRowIndex, endRowIndex);
            }
        }else if(sheetName.indexOf("Sequence") >= 0) {
        	this.initRsRowColIndex(sheetInfo);
        	if (rsTitleColIndex > 0 && rsValueColIndex > 0) {
        		iEndIntroRow = startRowIndex-2;
        		section.resourInfo = getRsInfo(sheetInfo, startRowIndex, endRowIndex);
            }
        }
          
        for (int iRowIndex = iStartIntroRow; iRowIndex < iEndIntroRow; iRowIndex++) {
            if (sheetInfo.getRow(iRowIndex) == null) {
                continue;
            }
            String lineStr = "";
            for (int iColIndex=1; iColIndex < sheetInfo.getRow(iRowIndex).getLastCellNum(); iColIndex++) {
                lineStr = lineStr + this.xlsUtil.getCellStrInfo(sheetInfo, iRowIndex, iColIndex);
            }

            if (lineStr.length()>0) {
                oneImgInfo.imgIntroduce = oneImgInfo.imgIntroduce + lineStr + "\n";
            }
        }
        if (!oneImgInfo.imgIntroduce.equals("")) {
            oneImgInfo.imgIntroduce = oneImgInfo.imgIntroduce.substring(0,
                    oneImgInfo.imgIntroduce.lastIndexOf("\n"));
            oneImgInfo.imgIntroduce = oneImgInfo.imgIntroduce.replace("■说明", "");
            if (oneImgInfo.imgIntroduce.length()>1) {
            	if(oneImgInfo.imgIntroduce.substring(0,1).equals("\n")) {
            	oneImgInfo.imgIntroduce = oneImgInfo.imgIntroduce.substring(1);
            	}
            }
        }
        section.imageInfo = oneImgInfo;
        sectionInfo.add(section);
        return sectionInfo;
    }

    private boolean checkSheetInfo(XSSFSheet sheetInfo) {
        for (String oneKeyword : keywordStr) {
            if (sheetInfo.getSheetName().indexOf(oneKeyword)>=0) {
                return true;
            }
        }

        return false;
    }
    
    public ArrayList<UCTableInfo> getUcTable(XSSFSheet sheetInfo, int startRow, int endRow){
    	ArrayList<UCTableInfo> tableInfo = new ArrayList<>();
    	for (int iRowIndex = startRow; iRowIndex <= endRow; iRowIndex++) {
            XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);
            UCTableInfo oneUcInfo = new UCTableInfo();
            if (rowInfo == null) {
                continue;
            }
            XSSFCell cellInfo = rowInfo.getCell(ucNoColIndex);
            if (cellInfo == null) {
                continue;
            }
            if (cellInfo.getStringCellValue().length() == 0) {
                continue;
            }
            oneUcInfo.ucNo = cellInfo.getStringCellValue();
            cellInfo = rowInfo.getCell(ucTitleColIndex);
            if (cellInfo!= null) {
            	oneUcInfo.ucTile = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(ucIntroduceColIndex);
            if (cellInfo != null) {
            	oneUcInfo.ucIntroduce = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(seqNoColIndex);
            if (cellInfo != null) {
            	oneUcInfo.seqNo = cellInfo.getStringCellValue();
            }
            cellInfo = rowInfo.getCell(seqSheetColIndex);
            if (cellInfo != null) {
            	oneUcInfo.seqSheet = cellInfo.getStringCellValue();
            }

            tableInfo.add(oneUcInfo);
        }

        return tableInfo;
    }
    
    public ArrayList<ResourceInfo> getRsInfo(XSSFSheet sheetInfo, int startRow, int endRow){
    	ArrayList<ResourceInfo> resourInfoList = new ArrayList<>();
    	for (int iRowIndex = startRow; iRowIndex <= endRow; iRowIndex++) {
    		ResourceInfo resourInfo = new ResourceInfo();
    		XSSFRow rowInfo = sheetInfo.getRow(iRowIndex);
    		if (rowInfo == null) {
                continue;
            }
            XSSFCell cellInfo = rowInfo.getCell(rsTitleColIndex);
            if (cellInfo == null) {
                continue;
            }
            if (cellInfo.getStringCellValue().length() == 0) {
                continue;
            }
            resourInfo.title = cellInfo.getStringCellValue();
            cellInfo = rowInfo.getCell(rsValueColIndex);
            if (cellInfo!= null) {
            	resourInfo.value = cellInfo.getStringCellValue();
            }
            resourInfoList.add(resourInfo);
    	}
    	return resourInfoList;
    }
    
    
    public void initUcRowColIndex(XSSFSheet sheetInfo) {
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
                if (cellValue.indexOf("UsecaseNo") >= 0) {
                    startRowIndex = iRowIndex + 1;
                    ucNoColIndex = iColIndex;
                } else if (cellValue.indexOf("Usecase名称") >= 0) {
                    ucTitleColIndex = iColIndex;
                } else if (cellValue.indexOf("Usecase说明") >= 0) {
                    ucIntroduceColIndex = iColIndex;
                } else if (cellValue.indexOf("SequenceNo") >= 0) {
                    seqNoColIndex = iColIndex;
                } else if (cellValue.indexOf("SequenceSheet名称") >= 0) {
                    seqSheetColIndex = iColIndex;
                } 
            }
        }       
    }
    public void initRsRowColIndex(XSSFSheet sheetInfo) {
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
                if (cellValue.indexOf("名称") >= 0) {
                    startRowIndex = iRowIndex + 1;
                    rsTitleColIndex = iColIndex;
                } else if (cellValue.indexOf("内容") >= 0) {
                    rsValueColIndex = iColIndex;
                }
            }
        }
    }
    
//    private String emfReader(String filePath, String extName) throws Exception  {
//        EMFInputStream inputStream = new EMFInputStream(new FileInputStream(filePath), EMFInputStream.DEFAULT_VERSION);
//        System.out.println("height = " + inputStream.readHeader().getBounds().getHeight());
//        System.out.println("widht = " + inputStream.readHeader().getBounds().getWidth());
//        EMFRenderer emfRenderer = new EMFRenderer(inputStream);
//        final int width = (int)inputStream.readHeader().getBounds().getWidth();
//        final int height = (int)inputStream.readHeader().getBounds().getHeight();
//        System.out.println("widht = " + width + " and height = " + height);
//        final BufferedImage result = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
//        Graphics2D g2 = (Graphics2D)result.createGraphics();
//        emfRenderer.paint(g2);
//        String newFilePath = filePath.replace(extName, "png");
//        File outputfile = new File(newFilePath);
//        ImageIO.write(result, "png", outputfile);
//        return newFilePath;
//    }

}
