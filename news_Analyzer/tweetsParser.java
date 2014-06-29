import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.text.ParseException;
import org.json.JSONObject;
import org.json.JSONArray;
import org.json.JSONException;
import java.io.LineNumberReader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import java.sql.Timestamp;

public class tweetsParser {
	private int contr;
	private long[] min_time;
	private long[] max_time;
	DocumentNGramGraph[] inter;

	public tweetsParser(String infile, int rank, int distance) throws FileNotFoundException, IOException {
		// Counting the number of rows in the file
		try {
			LineNumberReader lnr = new LineNumberReader(new FileReader(infile));
			lnr.skip(Long.MAX_VALUE);
			contr = lnr.getLineNumber();
			lnr.close();
		}
		catch (Exception exc) {
			System.err.println("I wasn't able to read the tweets file "+infile);
			throw exc;
		}
		System.out.printf("Detected %d contradiction points\n", contr);
		// Initialization
		min_time = new long[contr];
		max_time = new long[contr];
		inter = new DocumentNGramGraph[contr];
		for (int i = 0; i < contr; i++) {
			min_time[i] = Long.MAX_VALUE;
			max_time[i] = Long.MIN_VALUE;
			inter[i] = null;
		}
		// Populating
		BufferedReader br = new BufferedReader(new FileReader(infile));
		for (int i = 0; i < contr; i++) {
			System.out.printf("Computing graph for contradiction point %d/%d. ", i+1, contr);
			String line = br.readLine();
			JSONArray arr = new JSONArray(line);
			for (int j = 0; j < arr.length(); j++) {
				JSONObject jobj = arr.getJSONObject(j);
				long time = jobj.getLong("time");
				if (time < min_time[i]) min_time[i] = time;
				if (time > max_time[i]) max_time[i] = time;
				String text = jobj.getString("text");
				DocumentNGramSymWinGraph g = new DocumentNGramSymWinGraph(rank, rank, distance);
				g.setDataString(text);
				if (inter[i] == null)
					inter[i] = g;
				else
					inter[i].intersectGraph(g);
			}
			Timestamp t1, t2;
			t1 = new Timestamp(min_time[i]*1000);
			t2 = new Timestamp(max_time[i]*1000);
			System.out.println("Ranges from " + t1 + " to " + t2);
		}
	}

	public int getContrNumber() {
		return contr;
	}

	public long getMinTime(int i) {
		return min_time[i];
	}

	public long getMaxTime(int i) {
		return max_time[i];
	}

	public DocumentNGramGraph getIntersection(int i) {
		return inter[i];
	}
}


