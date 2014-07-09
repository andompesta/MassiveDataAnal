package Main;

import DAO.Contradiction.Contradiction;
import DAO.Contradiction.ContradictionParser;
import DAO.News.MongoDB;
import DAO.News.News;
import DAO.Tweet.Tweet;
import DAO.Tweet.TweetParser;
import Utils.TweetUtil;
import com.mongodb.DBCollection;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * Created by ando on 19/06/14.
 */
public class TweetContradiction {

    private static String topicName;

    public static void main(String[] args) throws IOException {

        Properties prop = new Properties();
        InputStream input = null;
        MongoDB manager = new MongoDB();
        try {
            input = new FileInputStream("config/graph.properties");
            prop.load(input);
            topicName = prop.getProperty("topicName");

            //Mappa contenente topic e contraddizioni per qei topic
            Map<String, Contradiction> contrad = ContradictionParser.parsContradictions();

            manager.dbConnection();
            DBCollection newsCollection = manager.getCollection("News-" + topicName);

            //Lista di tutte le news lette dal Db
            List<News> topicNews = manager.getNews(newsCollection);
            //Lista di tutti i tweet letti da file .txt
            ArrayList<Tweet> topicTweet = TweetParser.parsTweet("topic_" + contrad.get(topicName).getId() + "_spamfree.txt");

            TweetUtil.contrTweet(topicName, contrad, topicTweet);

            //Lista di tutti i tweet dei periodi di sentiment shift letti da file .json
            ArrayList<ArrayList<Tweet>> contTweet = TweetParser.parsContrTweet(topicName);
        }catch(Exception e ){e.printStackTrace();}
        finally {
            manager.dbConnectionClose();
        }
    }
}
