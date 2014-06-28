import org.ini4j.Ini;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;

class configurationReader {
	private String newsFile;
	private String tweetsFile;
	private int rank;
	private int distance;

	public configurationReader(String topic) throws FileNotFoundException, IOException {
		Ini conf = new Ini(new FileReader("config.ini"));
		Ini.Section Graph = conf.get("Graph");
		Ini.Section Paths = conf.get("Paths");
		rank = Integer.parseInt(Graph.get("rank"));
		distance = Integer.parseInt(Graph.get("distance"));
		newsFile = Paths.get("news_path").replace("X", topic);
		tweetsFile = Paths.get("tweets_path").replace("X", topic);
	}

	public String getNewsFile() {
		return newsFile;
	}

	public String getTweetsFile() {
		return tweetsFile;
	}

	public int getRank() {
		return rank;
	}

	public int getDistance() {
		return distance;
	}
}
