package Utils;

import Correlators.Correlation;
import Correlators.CorrelationComparator.ScoreComparator;
import Correlators.Score;
import DAO.Summary.SentenceByCP;
import DAO.Summary.SentenceScore;
import com.google.gson.Gson;
import gr.demokritos.iit.jinsect.documentModel.comparators.NGramCachedGraphComparator;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.structs.GraphSimilarity;

import java.io.*;
import java.util.*;

/**
 * Created by ando on 10/07/14.
 */
public class NewsSummarizerDoJob {
    private String computationType;
    private int windowSize;
    private int minRank;
    private int maxRank;
    private int neighbourhoodDistance;
    private String topicName;
    private String dataPath;
    private String resultPath;
    private int maxSortScoreLenght;
    private int summaryLenght;
    private DocumentNGramGraph[] intersectionGraph;
    private int numCP;
    private SentenceByCP sentenceByCP;


    public NewsSummarizerDoJob(int wSize,  String arg, int neighbourhoodDistance){
        this.windowSize = wSize;
        this.computationType = arg;

        Properties prop = new Properties();
        try {
            InputStream input = new FileInputStream("config/graph.properties");
            prop.load(input);
            this.minRank = Integer.parseInt(prop.getProperty("minRank"));
            this.maxRank = Integer.parseInt(prop.getProperty("maxRank"));
            this.neighbourhoodDistance = neighbourhoodDistance;
            this.topicName = prop.getProperty("topicName");
            this.dataPath = prop.getProperty("dataPath");
            this.resultPath = prop.getProperty("resultPat");
            this.summaryLenght = Integer.parseInt(prop.getProperty("summaryLenght"));
            this.maxSortScoreLenght = Integer.parseInt(prop.getProperty("maxScoreLenght"));
        }catch (Exception e){e.printStackTrace();}
    }

    public void doJob() throws Exception {
        List<Correlation> news = readData();
        if (news.isEmpty()){
            throw new Exception("Errore in the reading of the news files");
        }
        else{
            //inizialization
            numCP = news.get(0).getScore().length;
            sentenceByCP = new SentenceByCP(numCP);

            //computation
            computeNewsGram(news);
            //compute the top correlated news with the sentiment shift for each contraddiction point
            Correlation[][] bestNews = computeBestNews(news);
            //compute the sentence present in each top score document
            sentenceSplitter(bestNews);

            sentenceByCP.printSentence(dataPath, computationType, topicName, neighbourhoodDistance);

            intersectionGraph = new DocumentNGramGraph[numCP];
            //Compute the intersection of the top score documents
            intersectionGraph = intersectGraph(bestNews);

            //compte the sentence that summary better the documents
            SentenceScore[][] scores = summarizeDocument();
            printScore(scores);

        }

    }

    private void sentenceSplitter(Correlation[][] bestNews) throws Exception {
        for (int i  = 0; i < bestNews.length;i++ ){
            for (int j = 0 ; j < bestNews.length; j++){
                if ( bestNews[i][j] != null ){
                    String[] ret = bestNews[i][j].getText().split("\\|\\.\\|");
                    for (String s : ret) {
                        s = s.trim();
                        if(sentenceByCP.getSentenceCollection()[i] == null)
                            sentenceByCP.getSentenceCollection()[i] = new HashSet<String>();
                        sentenceByCP.getSentenceCollection()[i].add(s);
                    }
                }

            }
        }
    }

    private DocumentNGramGraph[] intersectGraph(Correlation[][] bestNews) {
        DocumentNGramGraph[] g = new DocumentNGramGraph[numCP];
        for (int i = 0; i < bestNews.length; i++){
            for (Correlation c : bestNews[i]) {
                if (c != null){
                    if (g[i] == null)
                        g[i]=c.getNews();
                    else
                        g[i] = g[i].intersectGraph(c.getNews());
                }
            }
        }
        return g;
    }



    private SentenceScore[][] summarizeDocument() throws Exception {
        //ilizialization phase
        SentenceScore[][] scores = new SentenceScore[numCP][];
        for (int i = 0; i < numCP; i++){
            if ( numCP != sentenceByCP.getSentenceCollection().length)
                throw new Exception("Error in the computation due to wrong index of the SentenceByCP class");
            scores[i] = new SentenceScore[sentenceByCP.getSentenceCollection()[i].size()];
        }

        NGramCachedGraphComparator comparator = new NGramCachedGraphComparator();
        DocumentNGramGraph s = new DocumentNGramSymWinGraph(minRank,maxRank, neighbourhoodDistance);

        //For every sentence of the top 4 document: compute the similarity between the sentence and the intersection of the graph
        for ( int i = 0; i < numCP; i++ ){
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

    private Correlation[][] computeBestNews(List<Correlation> news){
        Correlation[][] sortNews = new Correlation[numCP][maxSortScoreLenght];
        for (int i = 0; i < numCP; i++){
            Collections.sort(news, new ScoreComparator(i));
            for (int j = 0; j < news.size(); j++){
                if ( news.get(j).getScore()[i].getScore() > 0.0 && j < maxSortScoreLenght) {
                    sortNews[i][j] = news.get(j);
                }
                else
                    break;
            }
        }
        return sortNews;
    }

    private void computeNewsGram( List<Correlation> news) throws Exception {
        //Recompute the ngram graph of each news readerd from the json file
        int i = 0;
        int size = news.size();
        while(i < size){
            for (Score s : news.get(i).getScore()){
                if(s.getScore() > 0.0){
                    DocumentNGramGraph doc = new DocumentNGramSymWinGraph(minRank, maxRank, neighbourhoodDistance);
                    doc.setDataString(news.get(i).getText());
                    news.get(i).setNews(doc);
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

    private List<Correlation> readData(){
        List<Correlation> ret = new ArrayList<Correlation>();
        //Type arrTy = temp.getClass();
        BufferedReader dataset;
        File folder = null;
        try {
            if (computationType.equals("truncate")) {
                folder = new File(dataPath +"/" +computationType + "/" + topicName + "/" + this.neighbourhoodDistance + "/" + windowSize);
            }
            else if(computationType.equals("adaptive")){
                folder = new File(dataPath +"/" +computationType + "/" + topicName);
            }
            if (folder != null) {
                File[] listOfFiles = folder.listFiles();
                for (File file : listOfFiles) {
                    if (file.getName().endsWith(".json")) {
                        String name = file.getPath();
                        System.out.println("Loaded file :\t"+name);
                        String jsontext = "";
                        dataset = new BufferedReader(new FileReader(file.getAbsolutePath()));
                        String line = "";
                        while ((line = dataset.readLine()) != null) jsontext += line;
                        Gson parser = new Gson();
                        Correlation temp = parser.fromJson(jsontext, Correlation.class);
                        ret.add(temp);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return ret;
    }

    private void printScore(SentenceScore[][] scores) throws FileNotFoundException, UnsupportedEncodingException {
        if (computationType.equals("truncate")) {
            for (int i = 0; i < scores.length; i++) {
                PrintWriter pf = new PrintWriter(resultPath + "/" + computationType + "/" + topicName + "/" + neighbourhoodDistance +
                        "/" + windowSize + "/Result-CP-" + i + ".txt", "UTF-8");
                String printingT = "";
                int wordCount = 0;
                for (SentenceScore ss : scores[i]) {
                    printingT += ss.toString() + "\n";
                    wordCount += ss.getSentence().split("\\s+").length; //separate string around spaces
                    if (wordCount > summaryLenght) {
                        break;
                    }
                }
                pf.write(printingT);
                pf.close();
            }
        } else if (computationType.equals("adaptive")) {
            for (int i = 0; i < scores.length; i++) {
                PrintWriter pf = new PrintWriter(resultPath + "/" + computationType + "/" + topicName + "/" + neighbourhoodDistance +
                        "/" + "/Result-CP-" + i + ".txt", "UTF-8");
                String printingT = "";
                int wordCount = 0;
                for (SentenceScore ss : scores[i]) {
                    printingT += ss.toString() + "\n";
                    wordCount += ss.getSentence().split("\\s+").length; //separate string around spaces
                    if (wordCount > summaryLenght) {
                        break;
                    }
                }
                pf.write(printingT);
                pf.close();
            }
        }
    }
}
