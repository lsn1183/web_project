import java.io.FileWriter;
import java.util.ArrayList;
import point.PointInfo;
import point.PointContent;
import com.google.gson.*;

public class DumpPoint {
    public static void main(String[] args) throws Exception {
        if (args.length < 3) {
            System.out.println("Usage:DumpPoint <fullfilename> <type> <jsonfile>");
            throw new Exception("Parameter is error");
        }

        PointContent pointContent = new PointContent(args[0], args[1]);
//        PointContent pointContent = new PointContent("/mnt/sharedoc/point/20171220/元ファイル/TAGL要件定義書/TAGL_RequirementDefinitionVer1.02_30_Media_20171218_TMCReview.xlsx", "DEF");

        if (pointContent.checkDocIsOk() == false) {
            throw new Exception("file format is error");
        }

        ArrayList<ArrayList<PointInfo>> contentList = new ArrayList<ArrayList<PointInfo>>();

        for (int i=pointContent.getFirstRowNum(); i<=pointContent.getLastRowNum(); i++){
            ArrayList<PointInfo> rowPointList = pointContent.getOneRow(i);
            String statusInfo = pointContent.getValByTitle(rowPointList,"ステータス");
            if (statusInfo.indexOf("SUNTEC清書中")<0) {
                continue;
            }

            String lastCheck = pointContent.getValByTitle(rowPointList,"最終チェック");
            if (lastCheck.toLowerCase().trim().indexOf("OK".toLowerCase())!=0) {
                continue;
            }

            contentList.add(rowPointList);

        }

//        FileWriter writer = new FileWriter("/mnt/sharedoc/t.json");
        FileWriter writer = new FileWriter(args[2]);
        Gson gson = new GsonBuilder().create();
        gson.toJson(contentList, writer);
        writer.close();
    }


}
