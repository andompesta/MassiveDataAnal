import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.LineNumberReader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.utils;
import org.json.JSONObject;
import org.json.JSONException;
import java.io.IOException;


public class NgramGraphAnalyser {
    private static List<DocumentNGramSymWinGraph> graphList;
    private static int Rank;
    private static int neighbourhoodDistance;
	private static String newsFile;

    public NgramGraphAnalyser(){
        graphList = new ArrayList<DocumentNGramSymWinGraph>();
    }

    public NgramGraphAnalyser(ArrayList<DocumentNGramSymWinGraph> graphs){
        graphList = graphs;
    }

	public void loadGraph(String article, String filename) throws FileNotFoundException, UnsupportedEncodingException {
		DocumentNGramSymWinGraph tempGraph = new DocumentNGramSymWinGraph(Rank, Rank, neighbourhoodDistance);
        tempGraph.setDataString(article);
	   	graphList.add(tempGraph);
		File graphFile = new File(filename);
		PrintWriter writer = new PrintWriter(graphFile , "UTF-8");
		writer.print(utils.graphToDot(tempGraph.getGraphLevel(0), false));
		writer.close();
	}

    public void loadGraphs(List<String> listNews) throws FileNotFoundException, UnsupportedEncodingException {
        int i = 0;
        for (String newsText : listNews){
			loadGraph(newsText, "graph/graph-"+i+".gv");
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
			System.out.println("Expected arguments: rank neighbourhood_dis newsfile");
			return -1;
		}
		Rank = Integer.parseInt(args[0]);
		neighbourhoodDistance = Integer.parseInt(args[1]);
		newsFile = args[2];
		System.out.println("Performing analysis on "+newsFile);
		System.out.printf("Rank: %d\nDistance: %d\n", Rank, neighbourhoodDistance);
		return 0;
	}
	///////////////////////////////////////////////////////////////////////////
	// Main
    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException, IOException, JSONException{
		if (argument_parser(args) == -1) 
			return;
        NgramGraphAnalyser analyzer = new NgramGraphAnalyser();
		PrintWriter log = new PrintWriter("errors.log", "UTF-8");
		int error_num = 0;
		
		// Initializing the Progress Bar
		LineNumberReader lnr = new LineNumberReader(new FileReader(newsFile));
		lnr.skip(Long.MAX_VALUE);
		ProgBar pb = new ProgBar(40, lnr.getLineNumber());
		lnr.close();

		// Parsing each news and creating their graph
		System.out.println("Reading file and creating graphs...");
		log.println("Reading file");
		String currLine;
		int idx = 0;
		BufferedReader br = new BufferedReader(new FileReader(newsFile));
		while ((currLine = br.readLine()) != null) {
			try {
				String outf = "graph/news"+idx+".gv";
				JSONObject jobj = new JSONObject(currLine);
				String content = jobj.optString("lead_paragraph", "");
				content += " " + jobj.optString("full_text", "");
				analyzer.loadGraph(content, outf);
				idx++;
				pb.printProg(idx);
			}
			catch (JSONException exc) {
				log.println("\n"+exc.getMessage());
				log.println(currLine+"\n");
				error_num++;
			}
		}
		System.out.println();
		if (error_num > 0)
			System.err.println(error_num+" errors occurred. Read log file for more information\n");
		log.close();

		System.out.println("Computing the graphs intersection...");
		DocumentNGramGraph intersection = analyzer.intersectGraphs();

		// Now check how much each news differ from the global intersection
		Stats stat = new Stats();
		for (int i = 0; i < graphList.size(); i++) {
			DocumentNGramGraph diff = graphList.get(i).inverseIntersectGraph(intersection);
			stat.notify(diff.length());
			PrintWriter pw = new PrintWriter("graph/diff"+i+".gv", "UTF-8");
			pw.print(utils.graphToDot(diff.getGraphLevel(0), false));
			pw.close();
		}
		System.out.println("Statistics on differences:");
		System.out.println("Max difference: "+stat.max());
		System.out.println("Maximum point: "+stat.maxIndex());
		System.out.println("Min difference: "+stat.min());
		System.out.println("Minimum point: "+stat.minIndex());
		System.out.println("Mean: "+stat.mean());
		System.out.println("Variance: "+stat.variance());
		System.out.println("Standard Devition: "+stat.stdDeviation());
    }
}
