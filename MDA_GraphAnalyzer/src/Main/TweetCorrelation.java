package Main;

import DAO.Contradiction.Contradiction;
import DAO.Contradiction.ContradictionParser;
import DAO.Contradiction.ContradictionPoint;
import DAO.News.MongoDB;
import DAO.News.News;
import DAO.Tweet.Tweet;
import DAO.Tweet.TweetParser;
import Utils.TweetManager;
import com.mongodb.DBCollection;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Map;

/**
 * Created by ando on 19/06/14.
 */
public class TweetCorrelation {

    private static String topicName = "Cern";

    public static void main(String[] args) throws IOException {
        //Mappa contenente topic e contraddizioni per qei topic
        Map<String, Contradiction> contrad = ContradictionParser.parsContradictions();

        MongoDB manager = new MongoDB();
        manager.dbConnection();
        DBCollection newsCollection = manager.getCollection("News-"+topicName);

        //Lista di tutte le news lette dal Db
        ArrayList<News> topicNews = manager.getNews(newsCollection);
        //Lista di tutti i tweet letti da file .txt
        ArrayList<Tweet> topicTweet = TweetParser.parsTweet("topic_"+ contrad.get(topicName).getId() +"_spamfree.txt");
        //Lista di tutti i tweet dei periodi di sentiment shift letti da file .json
        ArrayList<ArrayList<Tweet>> contTweet = TweetParser.parsContrTweet(topicName);


    }
}
