import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.LineNumberReader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.UnsupportedEncodingException;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.comparators.NGramGraphComparator;
import gr.demokritos.iit.jinsect.structs.GraphSimilarity;
import gr.demokritos.iit.jinsect.utils;
import java.io.IOException;
import java.io.InvalidClassException;
import java.sql.Timestamp;


public class NgramGraphAnalyser {
    private static int Rank;
    private static int neighbourhoodDistance;
	private static String newsFile;
	private static Timestamp init_time;
	private static Timestamp end_time;
	private static String tweets;
	private DocumentNGramGraph GlobalIntersection;
	private DocumentNGramGraph outlier;
	private String outlierContent;
	private double outlierSimilarity;
	private NGramGraphComparator comp;
	private DocumentNGramGraph tweetsGraph;
	private int processed;

    public NgramGraphAnalyser(){
		GlobalIntersection = null;
		outlier = null;
		comp = new NGramGraphComparator();
		outlierSimilarity = -1;
		processed = 0;
    }

	public void setTweetsGraph(DocumentNGramGraph g) {
		tweetsGraph = g;
	}

	public void intersectGraph(DocumentNGramGraph g) {
		if (GlobalIntersection == null)
			GlobalIntersection = g;
		else
			GlobalIntersection = GlobalIntersection.intersectGraph(g);
	}

	public void computeOutlier(DocumentNGramGraph g, String c) throws InvalidClassException {
		processed++;
		GraphSimilarity s = comp.getSimilarityBetween(tweetsGraph, g);
		double gSimilarity = s.getOverallSimilarity();
		if (gSimilarity > outlierSimilarity) {
			outlier = g;
			outlierContent = c;
			outlierSimilarity = gSimilarity;
		}
//		else {
//			GraphSimilarity sim1 = comp.getSimilarityBetween(GlobalIntersection, outlier);
//			GraphSimilarity sim2 = comp.getSimilarityBetween(GlobalIntersection, g);
//			double osim1 = sim1.getOverallSimilarity();
//			double osim2 = sim2.getOverallSimilarity();
//			if (osim2 < osim1) {
//				outlier = g;
//				outlierContent = c;
//			}
//		}
	}

	public DocumentNGramGraph getIntersection() {
		return GlobalIntersection;
	}

	public DocumentNGramGraph getOutlier() {
		return outlier;
	}

	public void printOutlierContent() {
		if (processed == 0) {
			System.out.println("No news has been processed.");
			return;
		}
		System.out.printf("%d news have been processed.\n", processed);
		System.out.printf("More similar text:\n%s\n", outlierContent);
	}

	// TODO: si sta popolando con un po' troppi argomenti
	// probabilmente e' meglio inserire un file di configurazione
	private static int argument_parser(String[] args) {
		// If something wrong print help message and exits
		if (args.length < 6) {
			System.out.println("Expected arguments: rank neighbourhood_dis newsfile init_time end_time tweets_file");
			return -1;
		}
		Rank = Integer.parseInt(args[0]);
		neighbourhoodDistance = Integer.parseInt(args[1]);
		newsFile = args[2];
		init_time = new Timestamp(Long.parseLong(args[3])*1000);
		end_time = new Timestamp(Long.parseLong(args[4])*1000);
		tweets = args[5];
		System.out.printf("INPUT: %s\nRANK: %d\nDISTANCE: %d\n", newsFile, Rank, neighbourhoodDistance);
		System.out.println("INIT_TIME: " + init_time);
		System.out.println("END_TIME: " + end_time);
		return 0;
	}
	
	///////////////////////////////////////////////////////////////////////////
	// Main
    public static void main(String[] args) throws IOException, FileNotFoundException, InvalidClassException {
		if (argument_parser(args) == -1) 
			return;
		tweetsParser tp = new tweetsParser(tweets, Rank, neighbourhoodDistance);
		int intervals = tp.getContrNumber();
		Timestamp[] intervalBegin = new Timestamp[intervals];
		Timestamp[] intervalEnd = new Timestamp[intervals];
        NgramGraphAnalyser[] analyzers = new NgramGraphAnalyser[intervals];
		for (int i = 0; i < intervals; i++) {
			analyzers[i] = new NgramGraphAnalyser();
			analyzers[i].setTweetsGraph(tp.getIntersection(i));
			intervalBegin[i] = new Timestamp(tp.getMinTime(i)*1000);
			intervalEnd[i] = new Timestamp(tp.getMaxTime(i)*1000);
		}
		
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
		while ((currLine = br.readLine()) != null) {
			newsParser np = new newsParser(currLine);
			Timestamp pub_date = np.getTimestamp();
			for (int i = 0; i < intervals; i++) {
				if (pub_date.before(intervalEnd[i]) && pub_date.after(intervalBegin[i])) {
					String content = np.getContent();
					DocumentNGramSymWinGraph g = new DocumentNGramSymWinGraph(Rank, Rank, neighbourhoodDistance);
					g.setDataString(content);
				//	analyzers[i].intersectGraph(g);
					analyzers[i].computeOutlier(g, content);
				}
			}
			idx++;
			pb.printProg(idx);
		}

		System.out.println();
		for (int i = 0; i < intervals; i++) {
			analyzers[i].printOutlierContent();
		}
//		if (processed == 0) {
//			System.out.println("We are sorry to inform you no news are available in the selected time period");
//			return;
//		}
//		else
//			System.out.println(processed + " news in the selected time period");
//		DocumentNGramGraph inter = analyzer.getIntersection();
//		System.out.println("Intersection size: " + inter.length());
//		System.out.println("Outlier content:\n" + analyzer.getOutlierContent());
//
//		System.out.println("Saving your intersection and outlier graph to files");
//		PrintWriter writer = new PrintWriter("intersection.gv", "UTF-8");
//        writer.print(utils.graphToDot(inter.getGraphLevel(0), false));
//        writer.close();
//		writer = new PrintWriter("outlier.gv", "UTF-8");
//		writer.print(utils.graphToDot(outl.getGraphLevel(0), false));
//		writer.close();
    }
}
