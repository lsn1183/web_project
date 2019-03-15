import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.ss.util.CellReference;
import org.apache.poi.xssf.usermodel.*;

import java.io.*;
import java.util.List;
import java.util.ArrayList;

import com.google.gson.*;
import com.google.gson.stream.JsonReader;

/**
 * Created by huangyp on 17-10-26.
 */

public class ExportToExcel {

    public static void main(String[] args) throws Exception{
        if (args.length < 4){
            System.out.println("Usage:HUToExcel <filetype> <jsonfile> <template> <outfile>");
            throw new Exception("Parameter is error");
        }

//        JsonReader jsonReader = new JsonReader(new FileReader("/mnt/sharedoc/hu_all_mid.json"));
//        File excelFile = new File("/mnt/sharedoc/template/HU_RequirementDefinition.Ver0.17_template.xlsx");
        JsonReader jsonReader = new JsonReader(new FileReader(args[1]));
        File excelFile = new File(args[2]);
        XSSFWorkbook wb = new XSSFWorkbook(new FileInputStream(excelFile));

        XSSFSheet ws = null;
        int iStartRow = 9;
        int iRow = 9;
        System.out.println(args[0]);
        if (args[0].equalsIgnoreCase("HU")) {
            ws = wb.getSheet("HU要件定義書");
            iStartRow = 9;
            iRow = 9;
        }
        else if(args[0].equalsIgnoreCase("TAGLDEF")) {
            ws = wb.getSheet("TAGL要件定義");
            iStartRow = 5;
            iRow = 5;
        }
        else if(args[0].equalsIgnoreCase("TAGLANA")) {
            ws = wb.getSheet("TAGL要件分析");
            iStartRow = 5;
            iRow = 5;
        }
        else {
            System.out.println("file type is error, availavle type is [HU, TAGLDEF, TAGLANA]");
            throw new Exception("filetype is error");
        }

        Gson gson =  new Gson();
        List hu_export_list = gson.fromJson(jsonReader,List.class);

        XSSFRow nowRow;
        XSSFCell nowCell;
        int iLastCol = 0;

        for (int r_index = 0; r_index<hu_export_list.size(); r_index++){
            List lineListInfo = (ArrayList<Object>)hu_export_list.get(r_index);
            nowRow = ws.getRow(iRow);
            if (nowRow == null) {
                nowRow = ws.createRow(iRow);
            }

            int iCol = 0;
            iLastCol = lineListInfo.size()-1;
            for (int c_index = 0; c_index < lineListInfo.size(); c_index++){
                nowCell = nowRow.getCell(iCol);
                if (nowCell == null) {
                    nowCell = nowRow.createCell(iCol);
                    nowCell.setCellStyle(ws.getRow(iStartRow).getCell(iCol).getCellStyle());
                }

                if (args[0].equalsIgnoreCase("HU") && (c_index == 12)) {
                    nowCell.setCellFormula(String.format("%s%d&\".\"&%s%d",
                            CellReference.convertNumToColString(1),(r_index+iStartRow+1),
                            CellReference.convertNumToColString(13),(r_index+iStartRow+1)
                            ));
                    iCol+=1;
                    continue;
                }
                else if (args[0].equalsIgnoreCase("TAGLDEF") && (c_index == 2)) {
                        nowCell.setCellFormula(String.format("%s%d&\".\"&%s%d",
                                CellReference.convertNumToColString(1),(r_index+iStartRow+1),
                                CellReference.convertNumToColString(3),(r_index+iStartRow+1)
                        ));
                        iCol+=1;
                        continue;
                    }


                Object colObj = (Object)lineListInfo.get(c_index);

                if (colObj == null){
                    nowCell.setCellValue("");
                }
                else if(colObj.getClass().toString().indexOf("Double")>=0){
                    Double colDoubleVal = (Double)colObj;
                    nowCell.setCellValue(colDoubleVal.intValue());
                }
                else {
                    nowCell.setCellValue((String)colObj);
                }

                iCol+=1;
            }
            iRow+=1;
        }
        //hidden the last row because the last row is md5
        if (iLastCol>0){
            ws.setColumnHidden(iLastCol,true);
        }

        System.out.println(iRow);
        //Refresh conditional formatting
        XSSFSheetConditionalFormatting wsConFormat = ws.getSheetConditionalFormatting();
        for (int iConIndex = 0; iConIndex<wsConFormat.getNumConditionalFormattings(); ++iConIndex){
            XSSFConditionalFormatting conFormat = wsConFormat.getConditionalFormattingAt(iConIndex);
            CellRangeAddress[] nowSheetRanges = conFormat.getFormattingRanges().clone();
            for (int iRangeIndex = 0; iRangeIndex<nowSheetRanges.length; iRangeIndex++){
                nowSheetRanges[iRangeIndex].setLastRow(iRow-1);
            }
            conFormat.setFormattingRanges(nowSheetRanges);
        }

        //Refresh formula header
        for (int iHeaderRow = 0; iHeaderRow <= iRow; ++iHeaderRow) {
            XSSFRow templateRow = ws.getRow(iHeaderRow);
            if (templateRow == null){
                continue;
            }
            for (int iColIndex = 0; iColIndex < templateRow.getLastCellNum(); iColIndex++){
                XSSFCell templateCell = templateRow.getCell(iColIndex);
                if (templateCell == null){
                    continue;
                }

                if (templateCell.getCellTypeEnum() == CellType.FORMULA){
                    templateCell.setCellFormula(templateCell.getCellFormula());
                }

            }
        }

//        OutputStream os = new FileOutputStream(new File("/mnt/sharedoc/test_hu_export.xlsx"));
        OutputStream os = new FileOutputStream(new File(args[3]));
        wb.write(os);
        os.close();
    }
}
