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
	private static configurationReader conf;
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

	private static int argument_parser(String[] args)  throws FileNotFoundException, IOException {
		// If something wrong print help message and exits
		if (args.length != 1) {
			System.out.println("Expected argument: topic");
			System.out.println("Also, take a look at config.ini file");
			return -1;
		}
		conf = new configurationReader(args[0]);
		System.out.println("Running NGramGraphAnalyser!");
		System.out.println("Tweets contradiction file: "+conf.getTweetsFile());
		System.out.println("News file: "+conf.getNewsFile());
		System.out.println("NGram rank: "+conf.getRank());
		System.out.println("NGram window distance: "+conf.getDistance());
		System.out.println();
		return 0;
	}
	
	///////////////////////////////////////////////////////////////////////////
	// Main
    public static void main(String[] args) throws IOException, FileNotFoundException, InvalidClassException {
		if (argument_parser(args) == -1) 
			return;
		tweetsParser tp = new tweetsParser(conf.getTweetsFile(), conf.getRank(), conf.getDistance());
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
		LineNumberReader lnr = new LineNumberReader(new FileReader(conf.getNewsFile()));
		lnr.skip(Long.MAX_VALUE);
		ProgBar pb = new ProgBar(40, lnr.getLineNumber());
		lnr.close();

		// Parsing each news and creating their graph
		System.out.println();
		System.out.println("Reading news and creating graphs...");
		String currLine;
		BufferedReader br = new BufferedReader(new FileReader(conf.getNewsFile()));
		int idx = 0;
		while ((currLine = br.readLine()) != null) {
			newsParser np = new newsParser(currLine);
			Timestamp pub_date = np.getTimestamp();
			for (int i = 0; i < intervals; i++) {
				if (pub_date.before(intervalEnd[i]) && pub_date.after(intervalBegin[i])) {
					String content = np.getContent();
					DocumentNGramSymWinGraph g = new DocumentNGramSymWinGraph(conf.getRank(), conf.getRank(), conf.getDistance());
					g.setDataString(content);
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
    }
}
