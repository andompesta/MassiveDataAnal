import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.LineNumberReader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.UnsupportedEncodingException;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.utils;
import org.json.JSONObject;
import org.json.JSONException;
import java.io.IOException;


public class NgramGraphAnalyser {
    private static int Rank;
    private static int neighbourhoodDistance;
	private static String newsFile;
	private DocumentNGramGraph GlobalIntersection;
	private DocumentNGramGraph outlier;

    public NgramGraphAnalyser(){
		GlobalIntersection = null;
		outlier = null;
    }

	public void intersectGraph(DocumentNGramGraph g) {
		if (GlobalIntersection == null)
			GlobalIntersection = g;
		else
			GlobalIntersection = GlobalIntersection.intersectGraph(g);
	}

	public void computeOutlier(DocumentNGramGraph g) {
		if (outlier == null)
			outlier = g;
		else {
			DocumentNGramGraph diff1, diff2;
			diff1 = GlobalIntersection.inverseIntersectGraph(outlier);
			diff2 = GlobalIntersection.inverseIntersectGraph(g);
			if (diff2.length() > diff1.length())
				outlier = g;
		}
	}

	public DocumentNGramGraph getIntersection() {
		return GlobalIntersection;
	}

	public DocumentNGramGraph getOutlier() {
		return outlier;
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
		System.out.printf("INPUT: %s\nRANK: %d\nDISTANCE: %d\n", newsFile, Rank, neighbourhoodDistance);
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
		BufferedReader br = new BufferedReader(new FileReader(newsFile));
		int idx = 0;
		while ((currLine = br.readLine()) != null) {
			try {
				JSONObject jobj = new JSONObject(currLine);
				String content = jobj.optString("lead_paragraph", "");
				content += " " + jobj.optString("full_text", "");
				DocumentNGramSymWinGraph g = new DocumentNGramSymWinGraph(Rank, Rank, neighbourhoodDistance);
        		g.setDataString(content);
				
				analyzer.intersectGraph(g);
				analyzer.computeOutlier(g);

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
			System.err.println(error_num+" errors occurred. Read log file for more information");
		log.close();

		DocumentNGramGraph inter, outl, diff;
		inter = analyzer.getIntersection();
		outl = analyzer.getOutlier();
		diff = outl.inverseIntersectGraph(inter);
		System.out.println("Intersection size: " + inter.length());
		System.out.println("Outlier size: " + outl.length());
		System.out.println("Outlier differs of: "+ diff.length());

		System.out.println("Saving your intersection and outlier graph to files");
		PrintWriter writer = new PrintWriter("intersection.gv", "UTF-8");
        writer.print(utils.graphToDot(inter.getGraphLevel(0), false));
        writer.close();
		writer = new PrintWriter("outlier.gv", "UTF-8");
		writer.print(utils.graphToDot(outl.getGraphLevel(0), false));
		writer.close();
    }
}
