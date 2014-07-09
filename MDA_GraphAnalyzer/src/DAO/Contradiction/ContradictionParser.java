package DAO.Contradiction;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by ando on 19/06/14.
 */
public class ContradictionParser {
    private static String path = "/home/ando/MassiveDataAnal/MDA_GraphAnalyzer/contradiction-info";
    public static Map<String, Contradiction> parsContradictions(){
        Map<String, Contradiction> ret = new HashMap<String, Contradiction>();
        BufferedReader dataset;
        try {
            File folder = new File(path);
            File[] listOfFiles = folder.listFiles();
            for (File file : listOfFiles) {
                if (file.getName().endsWith(".json")) {
                    String name = file.getName();
                    System.out.println(name);
                    String jsontext = "";

                    dataset = new BufferedReader(new FileReader(file.getAbsolutePath()));
                    String line = new String();
                    while ((line = dataset.readLine()) != null) jsontext += line;
                    Gson parser = new Gson();
                    Contradiction temp = parser.fromJson(jsontext,Contradiction.class);
                    ret.put(name.replace(".json",""),temp);
                    }
                }
            } catch (Exception e1) {
            e1.printStackTrace();
        }
        return ret;
    }
}
