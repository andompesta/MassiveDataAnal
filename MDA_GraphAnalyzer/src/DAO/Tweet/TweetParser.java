package DAO.Tweet;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by ando on 19/06/14.
 */
public class TweetParser {
    private static BufferedReader dataset;

    public static ArrayList<Tweet> parsTweet(String arg){
        ArrayList<Tweet> ret = new ArrayList<Tweet>();
        BufferedReader dataset;
        try {
            dataset = new BufferedReader(new FileReader("data/twitter-selected/"+arg));
            String line = new String();
            while ((line = dataset.readLine()) != null) {
                String[] str = line.split("\t");
                Tweet temp = new Tweet(str[3], Long.parseLong(str[2]));
                ret.add(temp);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ret;
    }

    public static ArrayList<ArrayList<Tweet>> parsContrTweet(String arg){
        ArrayList<ArrayList<Tweet>> ret = new ArrayList<ArrayList<Tweet>>();
        Tweet[] temp;
        //Type arrTy = temp.getClass();
        BufferedReader dataset;
        try {
            dataset = new BufferedReader(new FileReader("contradiction-tweet/"+arg+"-contr-tweet.json"));
            String line = new String();
            while ((line = dataset.readLine()) != null) {
                Gson builder = new Gson();
                temp = builder.fromJson(line, Tweet[].class);
                ret.add(new ArrayList<Tweet>(Arrays.asList(temp)));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ret;
    }

}