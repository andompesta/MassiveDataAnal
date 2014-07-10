package Main;

import Utils.TweetNewsCorrelationDoJob;

import java.io.*;
import java.util.ArrayList;
import java.util.Properties;

import org.apache.commons.lang3.time.StopWatch;

/**
 * Created by andocavallari on 24/05/14.
 */
public class TweetNewsCorrelator {



    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException{
        String executionType = "truncate";
        for (int i = 3; i < 8; i++){
            TweetNewsCorrelationDoJob doCorrela = new TweetNewsCorrelationDoJob(i);
            StopWatch timer = new StopWatch();
            timer.start();
            doCorrela.doJob(executionType);
            timer.stop();

            try {
                PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("data/performance/executiontime.txt", true)));
                out.println(executionType +" execution time :	"+timer.toString()+ "\tneighbourhoodDistance : "+i+"\n");
                out.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
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
