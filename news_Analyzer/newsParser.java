import java.sql.Timestamp;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.text.ParseException;
import org.json.JSONObject;
import org.json.JSONException;

public class newsParser {
	private String content;
	private Timestamp pub_date;

	public newsParser(String s) {
		try {
			JSONObject jobj = new JSONObject(s);
			// Extracting the timestamp
			String date_str = jobj.getString("pub_date");
			date_str = date_str.split("T")[0];
			DateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
			Date date = (Date) formatter.parse(date_str);
			pub_date = new Timestamp(date.getTime());
			// Extracting content
			content = jobj.optString("lead_paragraph", "");
			content += " " + jobj.optString("full_text", "");
		}
		catch (JSONException exc) {
			System.err.println("\nERROR: unexpected error while parsing news file");
			System.err.println(exc.getMessage());
		}
		catch (ParseException exc) {
			System.err.println("\nERROR: wrong date format");
			System.err.println(exc.getMessage());
		}
	}

	public String getContent() {
		return content;
	}

	public Timestamp getTimestamp() {
		return pub_date;
	}
}
