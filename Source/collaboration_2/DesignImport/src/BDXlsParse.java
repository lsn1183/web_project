import xlsparse.BasicDesignXls;

import java.io.File;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.stream.JsonWriter;

import jsonobj.BasicDesignInfo;

public class BDXlsParse {
    public static void main(String[] args) throws Exception {
//    	String fileUrl = "C:/Users/yuyin/Desktop/HwyView1.xlsx";
    	String fileUrl = "";
        if (args.length >= 1) {
        	fileUrl = args[0];
        }
        String[] list = fileUrl.split("/");
        String fileExcel = list[list.length-1];
        String fileName = fileExcel.substring(0,fileExcel.lastIndexOf("."));
        BasicDesignXls bdXls = new BasicDesignXls(fileUrl);
        String filePath = fileUrl.replace(fileExcel, fileName);
//        SimpleDateFormat df = new SimpleDateFormat("yyyyMMddHHmmss");
//        filePath = filePath + "_"+ df.format(new Date());
        String imagePath = filePath + "/" + "image";
        File file =new File(imagePath);
        if  (!file.exists()  && !file.isDirectory()) {
          file.mkdirs();
        }
        BasicDesignInfo bdInfo = bdXls.doParse(imagePath);
        bdInfo.basicDesignName = fileName;
        String jsonPath = filePath + "/" + "json/";
        File jsonFile =new File(jsonPath);
        if  (!jsonFile.exists()  && !jsonFile.isDirectory()){
        	jsonFile.mkdirs();
        }
        JsonWriter writer = new JsonWriter(new FileWriter(jsonPath+fileName+".json"));
        Gson gson = new Gson();
        gson.toJson(bdInfo, BasicDesignInfo.class, writer);
        writer.close();
//        String fileUrl = "/home/huangyp/17cyDetail/Traffic";
//        List<String> filelist = new ArrayList<>();
//        filelist = getFileList(fileUrl, filelist);
//        for(String oneFile : filelist) {
//            String[] list = oneFile.split("/");
//            String fileName = list[list.length - 1];
//            fileName = fileName.substring(0, fileName.lastIndexOf("."));
//            try {
//                BasicDesignXls bdXls = new BasicDesignXls(oneFile);
//                String imagePath = "/home/huangyp/temp/Detail/Traffic/image/"+fileName;
//                File file =new File(imagePath);
//                if  (!file.exists()  && !file.isDirectory()) {
//                    file.mkdirs();
//                }
//                BasicDesignInfo bdInfo = bdXls.doParse(imagePath);
//                bdInfo.basicDesignName = fileName;
//                String jsonPath = "/home/huangyp/temp/Detail/Traffic/json/";
//                File jsonFile =new File(jsonPath);
//                if  (!jsonFile.exists()  && !jsonFile.isDirectory()) {
//                    jsonFile.mkdirs();
//                }
//                JsonWriter writer = new JsonWriter(new FileWriter(jsonPath + fileName + ".json"));
//                Gson gson = new Gson();
//                gson.toJson(bdInfo, BasicDesignInfo.class, writer);
//                writer.close();
//            }catch(Exception e){
//                System.out.println(e.getMessage());
//                System.out.println("文件解析失败："+oneFile);
//                continue;
//            }
//        }
    }

    public static List<String> getFileList(String strPath, List<String> filelist) {
        File dir = new File(strPath);

        File[] files = dir.listFiles(); // 该目录下的文件全部放入数组
        if (files != null) {
            for (int i = 0; i < files.length; i++) {
                if (files[i].isDirectory()) { // 判断是文件还是文夹
                    getFileList(files[i].getAbsolutePath(), filelist); // 获取文件绝对路徑
                }
                else {
                    String strFileName = files[i].getAbsolutePath();
                    filelist.add(strFileName);
                }
            }

        }
        return filelist;
    }
}
