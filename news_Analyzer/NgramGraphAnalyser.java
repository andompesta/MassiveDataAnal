//package jinsect;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.utils;
/**
 * Created by andocavallari on 24/05/14.
 */
public class NgramGraphAnalyser {
    private List<DocumentNGramSymWinGraph> graphList;
    private static int Rank;
    private static int neighbourhoodDistance;
	private static String newsFolder;

    public NgramGraphAnalyser(){
        graphList = new ArrayList<DocumentNGramSymWinGraph>();
    }

    public NgramGraphAnalyser(ArrayList<DocumentNGramSymWinGraph> graphs){
        graphList = graphs;
    }

    public void loadGraph(List<String> listNews) throws FileNotFoundException, UnsupportedEncodingException {
        int i = 0;
        for (String newsText : listNews){

            DocumentNGramSymWinGraph tempGraph = new DocumentNGramSymWinGraph(Rank, Rank, neighbourhoodDistance);
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
                    finalGraph = new DocumentNGramSymWinGraph(Rank, Rank, neighbourhoodDistance);
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


	private static int argument_parser(String[] args) {
		// If something wrong print help message and exits
		if (args.length < 3) {
			System.out.println("Expected arguments: rank neighbourhood_dis newsfolder");
			return -1;
		}
		Rank = Integer.parseInt(args[0]);
		neighbourhoodDistance = Integer.parseInt(args[1]);
		newsFolder = args[2];
		System.out.println("Performing analysis on "+newsFolder);
		System.out.printf("Rank: %d\nDistance: %d\n", Rank, neighbourhoodDistance);
		return 0;
	}
	///////////////////////////////////////////////////////////////////////////
	// Main
    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException{
		if (argument_parser(args) == -1) 
			return;
        NgramGraphAnalyser analyser = new NgramGraphAnalyser();
        List<String> newsText = new ArrayList<String>();

		// Adding news
        newsText.add("aaabaab");
        newsText.add("aabac");

        analyser.loadGraph(newsText);
        analyser.intersectGraphs();
        analyser.mergeGraphs();
    }
}
