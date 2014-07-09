package Main;

import DAO.Contradiction.Contradiction;
import DAO.News.Correlation;
import DAO.News.Score;
import DAO.Summary.SentenceByCP;
import DAO.Summary.SentenceScore;
import DAO.Tweet.Tweet;
import com.google.gson.Gson;
import gr.demokritos.iit.jinsect.documentModel.comparators.NGramCachedGraphComparator;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.structs.GraphSimilarity;

import java.io.*;
import java.util.*;

/**
 * Created by ando on 07/07/14.
 */
public class NewsSummarizer {
    private static int minRank;
    private static int maxRank;
    private static int neighbourhoodDistance;
    private static String windowSize;
    private static String topicName;
    private static String dataPath;
    private static String resultPath;
    private static DocumentNGramGraph[] intersectionGraph;
    private static int contradictionPoint;
    private static SentenceByCP sentenceByCP;
    private static int sl;

    private static List<Correlation> readData(){
        List<Correlation> ret = new ArrayList<Correlation>();
        //Type arrTy = temp.getClass();
        BufferedReader dataset;
        try {
            File folder = new File(dataPath +"/" + topicName + "/" + windowSize);
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
                    Correlation temp = parser.fromJson(jsontext,Correlation.class);
                    ret.add(temp);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ret;

    }

    private static void computeNewsGram( List<Correlation> news) throws Exception {
        int i = 0;
        int size = news.size();
        while(i < size){
            for (Score s : news.get(i).getScore()){
                if(s.getScore() > 0.0){
                    DocumentNGramGraph doc = new DocumentNGramSymWinGraph(minRank, maxRank, neighbourhoodDistance);
                    doc.setDataString(news.get(i).getText());
                    news.get(i).setNews(doc);

                    //calcolo le frasi presenti in questa news per poi calcolare il ssummary
                    sentenceSplitter(s.getIdContrPoin(), news.get(i).getText());

                    i++;
                    break;
                }
                else if(s.getIdContrPoin() == 2){
                    news.remove(i);
                    size = news.size();
                }
            }
        }
    }

    private static void sentenceSplitter(int index, String newsText) throws Exception {
        if (index > contradictionPoint)
            throw new Exception("indice impossibile, bug nel codice");

        String[] ret = newsText.split("\\.");
        for (String s : ret) {
            s = s.trim();
            if(sentenceByCP.getSentenceCollection()[index] == null)
                sentenceByCP.getSentenceCollection()[index] = new HashSet<String>();
            sentenceByCP.getSentenceCollection()[index].add(s);
        }
    }

    private static void intersectGraph(List<Correlation> news, DocumentNGramGraph[] g) {
        for (Correlation c : news ){
            for (int i = 0; i < c.getScore().length; i++) {
                if ( c.getScore()[i].getScore() > 0.0 ){
                    if (g[i] == null){
                        g[i] = c.getNews();
                    }
                    else{
                        g[i] = g[i].intersectGraph(c.getNews());
                    }
                }
            }
        }
    }



    private static SentenceScore[][] summarizeDocument() throws Exception {
        //ilizialization phase
        SentenceScore[][] scores = new SentenceScore[contradictionPoint][];
        for (int i = 0; i < contradictionPoint; i++){
            if ( contradictionPoint != sentenceByCP.getSentenceCollection().length)
                throw new Exception("Error in the computation due to wrong index of the SentenceByCP class");
            scores[i] = new SentenceScore[sentenceByCP.getSentenceCollection()[i].size()];
        }

        NGramCachedGraphComparator comparator = new NGramCachedGraphComparator();
        DocumentNGramGraph s = new DocumentNGramSymWinGraph(minRank,maxRank, neighbourhoodDistance);

        for ( int i = 0; i < contradictionPoint; i++ ){
            int j = 0;
            for ( String sentence : sentenceByCP.getSentenceCollection()[i] ) {
                s.setDataString(sentence);
                GraphSimilarity gs = comparator.getSimilarityBetween(intersectionGraph[i], s);
                double score = (gs.SizeSimilarity == 0.0) ? 0.0 : gs.ValueSimilarity / gs.SizeSimilarity;
                SentenceScore temp = new SentenceScore(sentence, score);
                scores[i][j] = temp;
                j++;
            }
            Arrays.sort(scores[i]);
        }
        return scores;
    }

    private static void doJob() throws Exception {
        List<Correlation> news = readData();
        if (news.isEmpty()){
            throw new Exception("Errore in the reading of the news files");
        }
        else{
            //inizialization
            contradictionPoint = news.get(0).getScore().length;
            sentenceByCP = new SentenceByCP(contradictionPoint);

            //computation

            computeNewsGram(news); // esegue anche sentenceSplit -> sentenceByCP
            for (int i = 0; i < sentenceByCP.getSentenceCollection().length; i++){
                printSentence(sentenceByCP.getSentenceCollection()[i],i);
            }
            intersectionGraph = new DocumentNGramGraph[contradictionPoint];
            //Calcola il "riassunto" del testo delle news
            intersectGraph(news, intersectionGraph);

            SentenceScore[][] scores = summarizeDocument();
            printScore(scores);

        }


    }

    private static void printSentence(Set<String> textToPrint, int index) throws FileNotFoundException, UnsupportedEncodingException {
        PrintWriter pf = new PrintWriter(dataPath +"/" + topicName + "/sentence-"+index+".txt","UTF-8");
        String printingT = "";
        for (String text : textToPrint){
            printingT += text+"\n";
        }
        pf.print(printingT);
        pf.close();
    }

    private static void printScore(SentenceScore[][] scores) throws FileNotFoundException, UnsupportedEncodingException {
        for (int i = 0; i < scores.length; i++){
            PrintWriter pf = new PrintWriter(resultPath +"/" + topicName + "/results-" +windowSize+ "-" + i + ".txt","UTF-8");
            String printingT = "";
            int wordCount = 0;
            for (SentenceScore ss : scores[i]){
                printingT += ss.toString()+"\n";
                wordCount += ss.getSentence().split("\\s+").length; //separate string around spaces
                if (wordCount > 100){
                    break;
                }
            }
            pf.print(printingT);
            pf.close();
        }
    }



    public static void main(String[] args){
        Properties prop = new Properties();
        InputStream input = null;
        try {
            input = new FileInputStream("config/graph.properties");
            prop.load(input);
            minRank = Integer.parseInt(prop.getProperty("minRank"));
            maxRank = Integer.parseInt(prop.getProperty("maxRank"));
            neighbourhoodDistance = Integer.parseInt(prop.getProperty("neighbourhoodDistance"));
            topicName = prop.getProperty("topicName");
            dataPath = prop.getProperty("dataPath");
            resultPath = prop.getProperty("resultPat");
            windowSize = prop.getProperty("10Size");
            sl = Integer.parseInt(prop.getProperty("summaryLenght"));
            doJob();
        }catch (Exception e){e.printStackTrace();}
    }


}
