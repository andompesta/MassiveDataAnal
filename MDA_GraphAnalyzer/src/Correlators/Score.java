package Correlators;

/**
 * Created by ando on 07/07/14.
 */
public class Score {
    private int idContrPoin;
    private double score;

    public Score() {
        this.idContrPoin = 0;
        this.score = 0.0;
    }

    public Score(int idContrPoin, double score) {
        this.idContrPoin = idContrPoin;
        this.score = score;
    }

    @Override
    public String toString(){
        String ret = "{\"idContrPoin\":" + this.getIdContrPoin() + "," + "\"score\":"+this.getScore()+"}";
        return  ret;
    }

    public int getIdContrPoin() {
        return idContrPoin;
    }

    public void setIdContrPoin(int idContrPoin) {
        this.idContrPoin = idContrPoin;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }
}
