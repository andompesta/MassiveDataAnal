package Utils;

import DAO.Contradiction.Contradiction;
import DAO.Contradiction.ContradictionPoint;
import DAO.Tweet.Tweet;
import com.google.gson.Gson;

import java.io.*;
import java.util.ArrayList;
import java.util.Map;

/**
 * Created by ando on 19/06/14.
 */
public class TweetUtil {

    public static void contrTweet(String topicName, Map<String, Contradiction> contrad, ArrayList<Tweet> topicTweet)  {
        ArrayList<ArrayList<Tweet>> shiftTweet = new ArrayList<ArrayList<Tweet>>();
        String path = "/home/ando/MassiveDataAnal/MDA_GraphAnalyzer/contradiction-tweet/"+ topicName +"-contr-tweet.json";

        for( ContradictionPoint contPoin : contrad.get(topicName).getContradictions()) {
            ArrayList<Tweet> temp = new ArrayList<Tweet>();
            for ( Tweet tweet : topicTweet) {
                if (tweet.getTime() >= contPoin.getTimeBegin() && tweet.getTime() <= contPoin.getTimeEnd()) {
                    //Tweet che fanno parte del sentiment shift
                    temp.add(tweet);
                }
            }
            shiftTweet.add(temp);
        }
        try{
            Gson builder = new Gson();
            String json = "";
            for(ArrayList<Tweet> temp : shiftTweet){
                json += builder.toJson(temp);
                json += "\n";
            }

            PrintWriter writer = new PrintWriter(path,"UTF-8");
            writer.print(json);
            writer.close();
        }catch (Exception e){e.printStackTrace();}
    }
}
