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
 * Created by ando on 05/07/14.
 */
public class TruncateNewsCorrelator {
    private int minRank;
    private int maxRank;
    private int neighbourhoodDistance;
    private List<Integer> windowSize;
    private ContrGraph[] contradGraph;

    public TruncateNewsCorrelator(List<ArrayList<Tweet>> contTweet, Contradiction contradiction, List<Integer> wSize, int neighbourhoodDistance) {
        Properties prop = new Properties();
        try{
            InputStream input = new FileInputStream("config/graph.properties");
            prop.load(input);
            this.minRank = Integer.parseInt(prop.getProperty("minRank"));
            this.maxRank = Integer.parseInt(prop.getProperty("maxRank"));
            this.neighbourhoodDistance = neighbourhoodDistance;
            this.windowSize = wSize;
            int size = (contTweet.size());//se vuoi eliminare elementi
            this.contradGraph = new ContrGraph[size];

            //Calcolo il grafo del merge dei tweet di contraddizione
            mergingGraph(size, contTweet, contradiction);
            System.out.println("Graph of the contradiction tweet compute correctly");
        }catch(Exception e){
            e.printStackTrace();
        }
            /*
            metodo corretto, ora provo a farlo + veloce
            DocumentNGramSymWinGraph temp;
            for (int i = 0; i < contTweet.size();i++){
                List<Tweet> tweets = contTweet.get(i);
                //merge tweet of the same contraddiction point
                temp = mergeTweet(tweets);
                contradGraph.add(temp);
            }
            */

            /*
            intersection
            for(int i = 0; i < size ; i++){
                DocumentNGramGraph g = new DocumentNGramSymWinGraph(minRank, maxRank , neighbourhoodDistance);
                for(Tweet tweet : contTweet.get(i)){
                    g.setDataString(removeUrl(tweet.getText()));
                    intersectGraph(i, g);
                }
            }
            */
    }

    private void mergingGraph(int size, List<ArrayList<Tweet>> contTweet, Contradiction ct) throws Exception {
        //Calcolo il grafo del merge dei tweet di contraddizione
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

    public List<Correlation> correlate(News news){
        DocumentNGramGraph newsGraph = new DocumentNGramSymWinGraph(minRank,maxRank,neighbourhoodDistance);

        newsGraph.setDataString(news.getText());
        List<Correlation> ret = new ArrayList<Correlation>();

        for(int wSize: windowSize) {
            Correlation correlation = new Correlation(contradGraph.length, newsGraph);
            for (ContrGraph graph : contradGraph) {
                correlation.getScore()[graph.idContradPoint] = new Score(graph.idContradPoint, 0.0);
                //controllo la correlazione delle news per una finestra temporale di 1 mese
                if ((graph.beginCon - wSize) < news.getTimestamp() && (graph.endCon + wSize) > news.getTimestamp()) {
                    NGramCachedGraphComparator comparator = new NGramCachedGraphComparator();

                    GraphSimilarity gs = comparator.getSimilarityBetween(newsGraph, graph.contGraph);
                    double NVS = (gs.SizeSimilarity == 0.0) ? 0.0 : gs.ValueSimilarity / gs.SizeSimilarity;
                    correlation.getScore()[graph.idContradPoint].setScore(NVS);
                }
            }
            correlation.setText(news.getText());
            ret.add(correlation);
        }
        return ret;
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

    private DocumentNGramSymWinGraph mergeTweet(List<Tweet> tweets){
        DocumentNGramSymWinGraph finalGraph = null;
        int iMergeCnt = 0;
        try {
            for(Tweet ctw : tweets) {
                DocumentNGramSymWinGraph tempGraph = new DocumentNGramSymWinGraph(minRank,maxRank,neighbourhoodDistance);
                tempGraph.setDataString(ctw.getText());
                if(finalGraph == null) {
                    finalGraph = new DocumentNGramSymWinGraph(minRank, maxRank, neighbourhoodDistance);
                    finalGraph = tempGraph;
                }
                else{
                    finalGraph.merge(tempGraph, (1.0 / (1.0 + iMergeCnt)));
                }
                iMergeCnt++;
                System.out.println(iMergeCnt);
            }
        }catch (Exception ex){
            ex.printStackTrace();
        }
        return finalGraph;
    }

    public void intersectGraph(int i , DocumentNGramGraph g) {
        if (contradGraph[i] == null)
            contradGraph[i] = new ContrGraph(g);
        else
            contradGraph[i].contGraph = contradGraph[i].contGraph.intersectGraph(g);
    }

    private class ContrGraph{
        private int idContradPoint;
        private long beginCon;
        private long endCon;
        private DocumentNGramGraph contGraph;

        private ContrGraph(DocumentNGramGraph contGraph) {
            this.beginCon = 0;
            this.endCon = 0;
            this.contGraph = contGraph;
        }

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
