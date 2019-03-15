package main;
import java.io.IOException;
import java.lang.System;
import com.change_vision.jude.api.inf.AstahAPI;
import com.change_vision.jude.api.inf.model.IModel;
import com.change_vision.jude.api.inf.model.INamedElement;
import com.change_vision.jude.api.inf.model.ISequenceDiagram;
import com.change_vision.jude.api.inf.project.ProjectAccessor;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;



/**
 * Sample for Getting API list.
 * 
 */
public class astah_check_it_needed {

    public static void main(String[] args) {
        try {
            System.out.println("Opening project...");
            ProjectAccessor prjAccessor = AstahAPI.getAstahAPI().getProjectAccessor();
            String projectPath = "";
//            projectPath = "C:\\Users\\yuyin\\Desktop\\TAGL_RequirementAnalysis_HAL.asta"; 
            if (args.length >= 1) {
                projectPath = args[0];
            }
            System.out.println(projectPath);
            File file = new File(projectPath);
            String fileName=file.getName();
//            System.out.println(fileName);
            if (fileName.endsWith(".asta")) {
                // System.out.println(s);
                prjAccessor.open(projectPath, true, false, true);
//                System.out.println("here");
                // Get a project model
                IModel project = prjAccessor.getProject();
                // Get all sequence diagrams.
                INamedElement[] sequences = prjAccessor.findElements(ISequenceDiagram.class);
                System.out.println("sequence num:" + sequences.length);
                String sequencTxtPath = projectPath.replace(fileName, "SequencDiagram.txt");
                System.out.println(sequencTxtPath);
                File txtfile = new File(sequencTxtPath);
                if(!txtfile.exists()) {
                	txtfile.getParentFile().mkdir();
                }
                // Show sequence informations.
                for (int i = 0; i < sequences.length; i++) {
                    ISequenceDiagram seq = (ISequenceDiagram) sequences[i];
//                    System.out.println("SequencDiagram : " + seq.getName());               
                    //write
                    FileWriter fw;
                    if (i == 0){
                    	fw = new FileWriter(txtfile);
                    }
                    else{
                    fw = new FileWriter(txtfile, true);
                    }
                    BufferedWriter bw = new BufferedWriter(fw);
                    bw.write(seq.getName()+"\r\n");
                    bw.flush();
                    bw.close();
                    fw.close();

                }
                prjAccessor.close();
            }
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
}
