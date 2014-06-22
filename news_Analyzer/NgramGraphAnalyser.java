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
import java.io.IOException;
import java.sql.Timestamp;


public class NgramGraphAnalyser {
    private static int Rank;
    private static int neighbourhoodDistance;
	private static String newsFile;
	private static Timestamp init_time;
	private static Timestamp end_time;
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

	// TODO: si sta popolando con un po' troppi argomenti
	// probabilmente e' meglio inserire un file di configurazione
	private static int argument_parser(String[] args) {
		// If something wrong print help message and exits
		if (args.length < 5) {
			System.out.println("Expected arguments: rank neighbourhood_dis newsfile init_time end_time");
			return -1;
		}
		Rank = Integer.parseInt(args[0]);
		neighbourhoodDistance = Integer.parseInt(args[1]);
		newsFile = args[2];
		init_time = new Timestamp(Long.parseLong(args[3])*1000);
		end_time = new Timestamp(Long.parseLong(args[4])*1000);
		System.out.printf("INPUT: %s\nRANK: %d\nDISTANCE: %d\n", newsFile, Rank, neighbourhoodDistance);
		System.out.println("INIT_TIME: " + init_time);
		System.out.println("END_TIME: " + end_time);
		return 0;
	}
	
	///////////////////////////////////////////////////////////////////////////
	// Main
    public static void main(String[] args) throws IOException, FileNotFoundException {
		if (argument_parser(args) == -1) 
			return;
        NgramGraphAnalyser analyzer = new NgramGraphAnalyser();
		
		// Initializing the Progress Bar
		LineNumberReader lnr = new LineNumberReader(new FileReader(newsFile));
		lnr.skip(Long.MAX_VALUE);
		ProgBar pb = new ProgBar(40, lnr.getLineNumber());
		lnr.close();

		// Parsing each news and creating their graph
		System.out.println("Reading file and creating graphs...");
		String currLine;
		BufferedReader br = new BufferedReader(new FileReader(newsFile));
		int idx = 0;
		int processed = 0;
		while ((currLine = br.readLine()) != null) {
			newsParser np = new newsParser(currLine);
			Timestamp pub_date = np.getTimestamp();
			if (pub_date.before(end_time) && pub_date.after(init_time)) {
				DocumentNGramSymWinGraph g = new DocumentNGramSymWinGraph(Rank, Rank, neighbourhoodDistance);
				g.setDataString(np.getContent());
				analyzer.intersectGraph(g);
				analyzer.computeOutlier(g);
				processed++;
			}
			idx++;
			pb.printProg(idx);
		}

		System.out.println();
		DocumentNGramGraph inter, outl, diff;
		inter = analyzer.getIntersection();
		outl = analyzer.getOutlier();
		if (processed == 0) {
			System.out.println("We are sorry to inform you no news are available in the selected time period");
			return;
		}
		else
			System.out.println(processed + " news in the selected time period");
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
