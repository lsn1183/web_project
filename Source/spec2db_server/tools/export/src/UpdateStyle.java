import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.OutputStream;
import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFConditionalFormatting;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFSheetConditionalFormatting;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class UpdateStyle
{
    public static void main(String[] args)
            throws Exception
    {
        if (args.length < 5)
        {
            System.out.println("Usage:UpdateStyle <OriginalXlsFile> <HUTemplateFile> <TAGLDEFTemlateFile> <TAGLANATemlateFile> <Outfile>");
            throw new Exception("Parameter is error");
        }
        File originalFile = new File(args[0]);
        XSSFWorkbook originalWorkBook = new XSSFWorkbook(new FileInputStream(originalFile));

        XSSFWorkbook templateWorkBook = null;
        if (originalWorkBook.getSheet("HU要件定義書") != null)
        {
            templateWorkBook = new XSSFWorkbook(new FileInputStream(args[1]));
            RefreshStyle(originalWorkBook.getSheet("HU要件定義書"), templateWorkBook.getSheet("HU要件定義書"), 9, 79);
        }
        else if (originalWorkBook.getSheet("TAGL要件定義") != null)
        {
            templateWorkBook = new XSSFWorkbook(new FileInputStream(args[2]));
            RefreshStyle(originalWorkBook.getSheet("TAGL要件定義"), templateWorkBook.getSheet("TAGL要件定義"), 5, 61);
        }
        else if (originalWorkBook.getSheet("TAGL要件分析") != null)
        {
            templateWorkBook = new XSSFWorkbook(new FileInputStream(args[3]));
            RefreshStyle(originalWorkBook.getSheet("TAGL要件分析"), templateWorkBook.getSheet("TAGL要件分析"), 5, 130);
        }
        if (templateWorkBook != null)
        {
            OutputStream os = new FileOutputStream(args[4]);
            templateWorkBook.write(os);
            os.close();
        }
    }

    private static void RefreshStyle(XSSFSheet originalSheet, XSSFSheet templateSheet, int iStartRow, int iColLength)
    {
        int iRow = iStartRow;
        for (; iRow <= originalSheet.getLastRowNum(); iRow++)
        {
            XSSFRow originalRow = originalSheet.getRow(iRow);
            XSSFRow templateRow = templateSheet.getRow(iRow);
            if (originalRow.getCell(0) == null) {
                break;
            }
            if (originalRow.getCell(1).getStringCellValue().equalsIgnoreCase("")) {
                break;
            }
            if (templateRow == null) {
                templateRow = templateSheet.createRow(iRow);
            }
            int iCol = 0;
            for (; iCol < originalRow.getLastCellNum(); iCol++)
            {
                XSSFCell templateCell = templateRow.getCell(iCol);
                if (templateCell == null)
                {
                    templateCell = templateRow.createCell(iCol);
                    if (templateSheet.getRow(iStartRow).getCell(iCol) != null) {
                        templateCell.setCellStyle(templateSheet.getRow(iStartRow).getCell(iCol).getCellStyle());
                    }
                }
                if (originalRow.getCell(iCol) != null) {
                    if (originalRow.getCell(iCol).getCellTypeEnum() == CellType.STRING) {
                        templateCell.setCellValue(originalRow.getCell(iCol).getStringCellValue());
                    } else if (originalRow.getCell(iCol).getCellTypeEnum() == CellType.NUMERIC) {
                        templateCell.setCellValue(originalRow.getCell(iCol).getNumericCellValue());
                    } else if (originalRow.getCell(iCol).getCellTypeEnum() == CellType.FORMULA) {
                        templateCell.setCellFormula(originalRow.getCell(iCol).getCellFormula());
                    } else if (originalRow.getCell(iCol).getCellTypeEnum() != CellType.BLANK) {
                        System.out.println("errrrrrrrr!!!---" + originalRow.getCell(iCol).getCellTypeEnum());
                    }
                }
            }
            //refresh the rest column style
            for (; iCol < iColLength; iCol++) {
                XSSFCell templateCell = templateRow.getCell(iCol);
                if (templateCell == null)
                {
                    templateCell = templateRow.createCell(iCol);
                }
                if (templateSheet.getRow(iStartRow).getCell(iCol) != null) {
                    templateCell.setCellStyle(templateSheet.getRow(iStartRow).getCell(iCol).getCellStyle());
                }
            }
        }

        XSSFSheetConditionalFormatting wsConFormat = templateSheet.getSheetConditionalFormatting();
        for (int iConIndex = 0; iConIndex < wsConFormat.getNumConditionalFormattings(); iConIndex++)
        {
            XSSFConditionalFormatting conFormat = wsConFormat.getConditionalFormattingAt(iConIndex);
            CellRangeAddress[] nowSheetRanges = (CellRangeAddress[])conFormat.getFormattingRanges().clone();
            for (int iRangeIndex = 0; iRangeIndex < nowSheetRanges.length; iRangeIndex++) {
                nowSheetRanges[iRangeIndex].setLastRow(iRow);
            }
            conFormat.setFormattingRanges(nowSheetRanges);
        }

        //Refresh formula header
        for (int iHeaderRow = 0; iHeaderRow <= iRow; ++iHeaderRow) {
            XSSFRow templateRow = templateSheet.getRow(iHeaderRow);
            if (templateRow == null){
                continue;
            }
            for (int iColIndex = 0; iColIndex < iColLength; iColIndex++){
                XSSFCell templateCell = templateRow.getCell(iColIndex);
                if (templateCell == null){
                    continue;
                }

                if (templateCell.getCellTypeEnum() == CellType.FORMULA){
                    templateCell.setCellFormula(templateCell.getCellFormula());
                }

            }
        }
    }
}
