package Correlators;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;


/**
 * Created by ando on 05/07/14.
 */
public class Correlation {
    private Score[] scores;
    private DocumentNGramGraph news;
    private String text;

    public Correlation() {}

    public Correlation(int size, DocumentNGramGraph news) {
        this.scores = new Score[size];
        this.news = news;
    }

    public String toJson(){
        String json = "{";
        json += "\"scores\":[";
        for(Score i : this.getScore()){
            json += i.toString();
            if (i.getIdContrPoin() < (scores.length-1) )
                json += ",";
        }
        json += "],";
        json += "\"text\" : \"" + textFormatter(this.getText()) + "\",";
        json += "\"news\" : {} }";
        return json;
    }

    private String textFormatter(String text) {
        String ret = "";
        for (String s : text.split("\\.\\n")) {
            s = s.trim();
            s = s.replaceAll("\\.","");
            ret += s + "|.|";
        }
        return ret;
    }

    public Score[] getScore() {
        return scores;
    }

    public void setScore(Score[] scores) {
        this.scores = scores;
    }

    public DocumentNGramGraph getNews() {
        return news;
    }

    public void setNews(DocumentNGramGraph news) {
        this.news = news;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

}
