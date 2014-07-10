package Correlators;

import DAO.Contradiction.Contradiction;
import DAO.News.News;
import DAO.Tweet.Tweet;
import gr.demokritos.iit.jinsect.documentModel.comparators.NGramCachedGraphComparator;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.structs.GraphSimilarity;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by ando on 09/07/14.
 */
public class AdaptiveNewsCorrelator {
    private int minRank;
    private int maxRank;
    private int neighbourhoodDistance;
    private List<Integer> windowSize;
    private ContrGraph contradGraph[];

    public AdaptiveNewsCorrelator(List<ArrayList<Tweet>> contTweet, Contradiction contradiction, List<Integer> wSize, int neighbourhoodDistance) {
        Properties prop = new Properties();
        try{
            InputStream input = new FileInputStream("config/graph.properties");
            prop.load(input);
            minRank = Integer.parseInt(prop.getProperty("minRank"));
            maxRank = Integer.parseInt(prop.getProperty("maxRank"));
            this.neighbourhoodDistance = neighbourhoodDistance;
            this.windowSize = wSize;
            int size = contTweet.size();
            this.contradGraph = new ContrGraph[size];

            //Calcolo il grafo del merge dei tweet di contraddizione
            merginGraph(size, contTweet, contradiction);
            System.out.println("Graph of the contradiction tweet compute correctly");
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    private void merginGraph(int size, List<ArrayList<Tweet>> contTweet, Contradiction ct) throws Exception {
        //Calcolo il grafo del merge dei tweet di contraddizione
        //For each contraddiction point compute the graph of the tweets
        for(int i = 0; i < size ; i++){
            String graphText = "";
            int count = 0;
            for(Tweet tweet : contTweet.get(i)){
                graphText += removeUrl(tweet.getText()) + " ";
                count ++;
                System.out.println(count);
            }
            //Set data to the contradicion graph
            if (i < ct.getContradictions().length){
                contradGraph[i] = new ContrGraph(i, ct.getContradictions()[i].getTimeBegin(), ct.getContradictions()[i].getTimeEnd());
                contradGraph[i].setContGraph(graphText);
            }
            else {
                throw new Exception("Error on the index of the merginGraph function");
            }

        }
    }

    private String removeUrl(String commentstr)
    {
        try {
            String urlPattern = "((https?|http):((//)|(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)";
            Pattern p = Pattern.compile(urlPattern, Pattern.CASE_INSENSITIVE);
            Matcher m = p.matcher(commentstr);
            int i = 0;
            while (m.find()) {
                commentstr = commentstr.replaceAll(m.group(i), "").trim();
                i++;
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        return commentstr;
    }

    public Correlation correlate(News news){
        DocumentNGramGraph newsGraph = new DocumentNGramSymWinGraph(minRank,maxRank,neighbourhoodDistance);
        int size = contradGraph.length;
        newsGraph.setDataString(news.getText());
        List<Correlation> ret = new ArrayList<Correlation>();

        Correlation element = new Correlation(size, newsGraph);

        try {
            for (int i = 0; i < size; i++) {
                if (contradGraph.length != windowSize.size()) {
                    throw new Exception("Error in the data structure of the correlation");
                }
                else{
                    element.getScore()[i] = new Score(contradGraph[i].idContradPoint, 0.0);
                    if ( (contradGraph[i].beginCon - windowSize.get(i)) < news.getTimestamp() &&
                            (contradGraph[i].endCon + windowSize.get(i)) > news.getTimestamp()){
                        NGramCachedGraphComparator comparator = new NGramCachedGraphComparator();

                        GraphSimilarity gs = comparator.getSimilarityBetween(newsGraph, contradGraph[i].contGraph);
                        double NVS = (gs.SizeSimilarity == 0.0) ? 0.0 : gs.ValueSimilarity / gs.SizeSimilarity;
                        element.getScore()[contradGraph[i].idContradPoint].setScore(NVS);
                    }
                }
            }
            element.setText(news.getText());
        }catch(Exception e){e.printStackTrace();}
        return element;
    }

    private class ContrGraph{
        private int idContradPoint;
        private long beginCon;
        private long endCon;
        private DocumentNGramGraph contGraph;

        private ContrGraph(int idContradPoint, long beginCon, long endCon) {
            this.idContradPoint = idContradPoint;
            this.beginCon = beginCon;
            this.endCon = endCon;
            this.contGraph = new DocumentNGramSymWinGraph(minRank, maxRank, neighbourhoodDistance);
        }

        private void setContGraph(String contText) {
            this.contGraph.setDataString(contText);
        }
    }

}
