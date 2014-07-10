package Utils;

import Correlators.AdaptiveNewsCorrelator;
import Correlators.TruncateNewsCorrelator;
import DAO.Contradiction.Contradiction;
import DAO.Contradiction.ContradictionParser;
import Correlators.Correlation;
import DAO.News.MongoDB;
import DAO.News.News;
import DAO.Tweet.Tweet;
import DAO.Tweet.TweetParser;
import com.mongodb.DBCollection;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * Created by ando on 09/07/14.
 */
public class TweetNewsCorrelationDoJob {
    private String topicName;
    private String dataPath;
    private int neighbourhoodDistance;


    public TweetNewsCorrelationDoJob(int n) {
        Properties prop = new Properties();
        try {
            InputStream input = new FileInputStream("config/graph.properties");
            prop.load(input);
            this.topicName = prop.getProperty("topicName");
            this.dataPath = prop.getProperty("dataPath");
            this.neighbourhoodDistance = n;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void printToFile(String textToPrint, String arg,int index, int wSize) {
        try {
            if (arg.equals("truncate")) {
                PrintWriter pf = new PrintWriter(dataPath + "/" + arg + "/" + topicName +"/"+ this.neighbourhoodDistance+
                        "/" + wSize + "/CorrelationScore-DocumentId-" + index + ".json", "UTF-8");
                pf.print(textToPrint);
                pf.close();
            }
            else if(arg.equals("adaptive")){
                PrintWriter pf = new PrintWriter(dataPath + "/" + arg + "/" + topicName + "/"+ this.neighbourhoodDistance +
                        "/CorrelationScore-DocumentId-" + index + ".json", "UTF-8");
                pf.print(textToPrint);
                pf.close();
            }
            System.out.println("Saved file CorrelationScore-DocumentId-" + index + ".json");
        }catch(Exception e){e.printStackTrace();}
    }

    public void doJob(String arg) {
        MongoDB manager = new MongoDB();
        try {
            //Read contradiction-info
            Map<String, Contradiction> contrad = ContradictionParser.parsContradictions();

            manager.dbConnection();
            DBCollection newsCollection = manager.getCollection("News-" + topicName);

            //Lista di tutte le news lette dal Db
            List<News> topicNews = manager.getNews(newsCollection);
            System.out.println("Read all the news for the topic " + topicName);

            //Lista di tutti i tweet dei periodi di sentiment shift letti da file .json
            List<ArrayList<Tweet>> contTweet = TweetParser.parsContrTweet(topicName);
            System.out.println("Read all the contradiction tweet");

            if (arg.equals("truncate")){
                doTruncate(arg, topicNews,contTweet,contrad.get(topicName));
            }
            else if (arg.equals("adaptive")){
                doAdaptive(arg, topicNews,contTweet,contrad.get(topicName));
            }


        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            manager.dbConnectionClose();
        }

    }

    private void doTruncate(String arg, List<News> topicNews, List<ArrayList<Tweet>> contTweet, Contradiction contrad) throws FileNotFoundException, UnsupportedEncodingException {
        List<Integer> wSizes = truncateWindows();
        TruncateNewsCorrelator nc = new TruncateNewsCorrelator(contTweet, contrad, wSizes, this.neighbourhoodDistance );

        int i = 0;
        //Start to compute correlation between news and contradiction tweet
        for (News news : topicNews){
            List<Correlation> experiments = nc.correlate(news);
            i++;
            System.out.println("Compute the correlation between news " + i + " and contradiction tweet");
            int j = 0;
            for (Correlation tc : experiments){
                //Save value on a json
                String json = tc.toJson();
                printToFile( json, arg, i, wSizes.get(j) );
                j++;
            }
        }
    }

    private void doAdaptive( String arg, List<News> topicNews, List<ArrayList<Tweet>> contTweet, Contradiction contrad ){
        List<Integer> wSizes = adaptiveWindows(contTweet);
        AdaptiveNewsCorrelator anc = new AdaptiveNewsCorrelator(contTweet, contrad, wSizes,this.neighbourhoodDistance );

        int i = 0;
        //Start to compute correlation between news and contradiction tweet
        for (News news : topicNews){
            Correlation experiment = anc.correlate(news);
            i++;
            System.out.println("Compute the correlation between news " + i + " and contradiction tweet");

            //Save value on a json
            String json = experiment.toJson();
            printToFile( json, arg, i , 0 );
        }
    }


    //finestra che elimina dallo scoring tutte le news maggiori di 5d,7d,10g,30g
    private List<Integer> truncateWindows() {
        List<Integer> wSizes = null;
        Properties prop = new Properties();
        try {
            InputStream input = new FileInputStream("config/graph.properties");
            prop.load(input);
            wSizes = new ArrayList<Integer>();
            wSizes.add(Integer.parseInt(prop.getProperty("5Size")));
            wSizes.add(Integer.parseInt(prop.getProperty("weekSize")));
            wSizes.add(Integer.parseInt(prop.getProperty("10Size")));
            wSizes.add(Integer.parseInt(prop.getProperty("monthSize")));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return wSizes;
    }

    //finestra che si adatta al numero di tweet di contraddizione
    private List<Integer> adaptiveWindows(List<ArrayList<Tweet>> contTweet) {
        List<Integer> wSizes = null;
        int[] temp = new int[contTweet.size()];
        int baseline = 777600;
        try {
            wSizes = new ArrayList<Integer>();
            int i = 0;
            for (List<Tweet> ct : contTweet){
                temp[i] = ct.size();
                System.out.println("Number of cTweet: "+temp[i] + "\tCP: "+i);
                i++;
            }
            int avg = calculateAverage(temp);
            for (i = 0; i < temp.length; i++ ){
                int ws = baseline + ( (avg - temp[i]) * 100 );

                System.out.println("windowsSize: "+ ws +"\tCP: "+i);
                wSizes.add(ws);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return wSizes;
    }

    private static int calculateAverage(int[] numTweets) {
        int sum = 0;
        for (int num : numTweets) {
            sum += num;
        }
        return (Integer) sum / numTweets.length;
    }
}
