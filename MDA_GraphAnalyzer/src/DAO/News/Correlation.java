package DAO.News;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;

import java.util.ArrayList;
import java.util.List;

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
