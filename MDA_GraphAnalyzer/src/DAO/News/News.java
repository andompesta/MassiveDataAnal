package DAO.News;

/**
 * Created by ando on 19/06/14.
 */
public class News {
    private String text;
    private String hdeadline;
    private long timestamp;
    private String leadParagraph;

    public News(String text, long timestamp, String leadParagraph, String hdeadline) {
        this.text = text;
        this.timestamp = timestamp;
        this.leadParagraph = leadParagraph;
        this.hdeadline = hdeadline;
    }

    public News() {

    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getHdeadline() {
        return hdeadline;
    }

    public void setHdeadline(String hdeadline) {
        this.hdeadline = hdeadline;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public String getLeadParagraph() {
        return leadParagraph;
    }

    public void setLeadParagraph(String leadParagraph) {
        this.leadParagraph = leadParagraph;
    }
}
