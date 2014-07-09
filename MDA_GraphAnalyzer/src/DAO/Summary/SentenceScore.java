package DAO.Summary;

import java.util.Comparator;

/**
 * Created by ando on 08/07/14.
 */
public class SentenceScore implements Comparator<SentenceScore>, Comparable<SentenceScore>{
    private String sentence;
    private double score;

    public SentenceScore(){}

    public SentenceScore(String sentence, double score) {
        this.sentence = sentence;
        this.score = score;
    }

    public String getSentence() {
        return sentence;
    }

    public void setSentence(String sentence) {
        this.sentence = sentence;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    @Override
    public int compareTo(SentenceScore o) {
        if (this.getScore() < o.getScore()) return 1;
        if (this.getScore() > o.getScore()) return -1;
        return 0;
    }

    @Override
    public int compare(SentenceScore o1, SentenceScore o2) {
        if (o1.getScore() < o2.getScore()) return 1;
        if (o1.getScore() > o2.getScore()) return -1;
        return 0;
    }

    @Override
    public String toString(){
        String ret;
        ret = this.getSentence();
        return ret;
    }
}
