package Main;

import DAO.Contradiction.Contradiction;
import DAO.Contradiction.ContradictionParser;
import DAO.News.Correlation;
import DAO.News.MongoDB;
import DAO.News.News;
import DAO.Tweet.Tweet;
import DAO.Tweet.TweetParser;
import Utils.NewsCorrelator;
import com.google.gson.Gson;
import com.google.gson.internal.Streams;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.utils;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * Created by andocavallari on 24/05/14.
 */
public class TweetNewsCorrelator {
    private static int minRank;
    private static int maxRank;
    private static int neighbourhoodDistance;
    private static String topicName;
    private static String dataPath;

    private static void printToFile(String textToPrint, int index, int wSize) throws FileNotFoundException, UnsupportedEncodingException {
        PrintWriter pf = new PrintWriter(dataPath +"/" + topicName + "/" + wSize + "/Score-"+index+".json","UTF-8");
        pf.print(textToPrint);
        pf.close();
    }

    private static String createJson(Gson builder, Correlation tc){
        String json = "{";
        json += "\"scores\" : " + builder.toJson(tc.getScore()) +",";
        json += "\"text\" : \"" + tc.getText() + "\",";
        json += "\"news\" : {} }";
        return json;
    }



    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException{

        Properties prop = new Properties();
        InputStream input = null;
        MongoDB manager = new MongoDB();
        try{
            input = new FileInputStream("config/graph.properties");
            prop.load(input);
            minRank = Integer.parseInt(prop.getProperty("minRank"));
            maxRank = Integer.parseInt(prop.getProperty("maxRank"));
            neighbourhoodDistance = Integer.parseInt(prop.getProperty("neighbourhoodDistance"));
            topicName = prop.getProperty("topicName");
            dataPath = prop.getProperty("dataPath");

            //Read contradiction-info
            Map<String, Contradiction> contrad = ContradictionParser.parsContradictions();

            manager.dbConnection();
            DBCollection newsCollection = manager.getCollection("News-"+topicName);

            //Lista di tutte le news lette dal Db
            List<News> topicNews = manager.getNews(newsCollection);
            System.out.println("Read all the news for the topic "+ topicName);

            //Lista di tutti i tweet dei periodi di sentiment shift letti da file .json
            List<ArrayList<Tweet>> contTweet = TweetParser.parsContrTweet(topicName);
            System.out.println("Read all the contradiction tweet");
/*
            int[] numberOfTweet = new int[contTweet.size()];

            for(int i = 0; i < contTweet.size() ; i++){
                numberOfTweet[i] = contTweet.size();
            }

            int avr = calculateAverage(numberOfTweet);
*/

            List<Integer> wSizes = new ArrayList<Integer>();
            wSizes.add( Integer.parseInt(prop.getProperty("5Size")) );
            wSizes.add( Integer.parseInt(prop.getProperty("weekSize")) );
            wSizes.add( Integer.parseInt(prop.getProperty("10Size")) );
            wSizes.add( Integer.parseInt(prop.getProperty("monthSize")) );

            NewsCorrelator nc = new NewsCorrelator(contTweet, contrad.get(topicName) , minRank, maxRank, neighbourhoodDistance, wSizes );

            Gson builder = new Gson();
            int i = 0;

            //Start to compute correlation between news and contradiction tweet
            for (News news : topicNews){
                List<Correlation> experiments = nc.correlate(news);
                i++;
                System.out.println("Compute the correlation between news " + i + " and contradiction tweet");
                int j = 0;
                for (Correlation tc : experiments){
                    //Save value on a json
                    String json = createJson(builder, tc);
                    printToFile( json, i, wSizes.get(j) );
                    j++;
                }
            }

        }catch(Exception e){
            e.printStackTrace();
        }finally {
            manager.dbConnectionClose();
        }
    }


    private static int calculateAverage(int[] numTweets) {
        int sum = 0;
        for (int num : numTweets) {
                sum += num;
            }
        return sum / numTweets.length;
    }

    /*
    public void loadGraph(List<String> listNews) throws FileNotFoundException, UnsupportedEncodingException {
        int i = 0;
        for (String newsText : listNews){

            DocumentNGramSymWinGraph tempGraph = new DocumentNGramSymWinGraph(minRank, maxRank, neighbourhoodDistance);
            tempGraph.setDataString(newsText);
            graphList.add(tempGraph);

            File graphFile = new File("graph/graph-"+i+".gv");
            PrintWriter writer = new PrintWriter(graphFile , "UTF-8");
            writer.print(utils.graphToDot(tempGraph.getGraphLevel(0), false));
            writer.close();
            i++;
        }
    }

    public void mergeGraphs(){
        DocumentNGramSymWinGraph finalGraph= null;
        int iMergeCnt = 0;
        try {
            File graphFile = new File("graph/mergeGraph.gv");
            PrintWriter writer = new PrintWriter(graphFile , "UTF-8");
            for (int i = 0; i < graphList.size(); i++)
            {
                //Compute the merded graph
                if(finalGraph == null){
                    finalGraph = new DocumentNGramSymWinGraph(minRank, maxRank, neighbourhoodDistance);
                    finalGraph = graphList.get(i);
                }else{
                    finalGraph.merge(graphList.get(i), (1.0 / (1.0 + iMergeCnt)));
                }
                iMergeCnt++;
            }
            writer.print(utils.graphToDot(finalGraph.getGraphLevel(0), false));
            writer.close();
        }catch (Exception ex){
            ex.printStackTrace();
        }
    }

    public DocumentNGramGraph intersectGraphs(){
        DocumentNGramGraph itersectGraph = null;
        DocumentNGramSymWinGraph temp = null;
        try {
            File graphFile = new File("graph/intersectGraph.gv");
            PrintWriter writer = new PrintWriter(graphFile , "UTF-8");
            for (DocumentNGramSymWinGraph currGraph : graphList)
            {
                //Compute the merded graph
                if(temp == null){
                    temp = currGraph;
                }else{
                    itersectGraph = temp.intersectGraph(currGraph);
                }
            }
            writer.print(utils.graphToDot(itersectGraph.getGraphLevel(0), false));
            writer.close();
        }catch (Exception ex){
            ex.printStackTrace();
            return null;
        }
        return itersectGraph;
    }
    */

}
