package Main;

import DAO.Contradiction.Contradiction;
import DAO.Contradiction.ContradictionParser;
import DAO.News.MongoDB;
import DAO.News.News;
import DAO.Tweet.TweetParser;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by andocavallari on 24/05/14.
 */
public class NgramGraphAnalyser {
    private List<DocumentNGramSymWinGraph> graphList;
    private static int minRank = 3;
    private static int maxRank = 3;
    private static int neighbourhoodDistance = 6;


    public NgramGraphAnalyser(){
        graphList = new ArrayList<DocumentNGramSymWinGraph>();
    }

    public NgramGraphAnalyser(ArrayList<DocumentNGramSymWinGraph> graphs){
        graphList = graphs;
    }

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

    public List<DocumentNGramSymWinGraph> getGraphList() {
        return graphList;
    }

    public void setGraphList(List<DocumentNGramSymWinGraph> graphList) {
        this.graphList = graphList;
    }

    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException{
        NgramGraphAnalyser analyser = new NgramGraphAnalyser();
        List<String> newsText = new ArrayList<String>();
        newsText.add("aaabaab");
        newsText.add("aabac");

        analyser.loadGraph(newsText);
        analyser.intersectGraphs();
        analyser.mergeGraphs();
    }
}
