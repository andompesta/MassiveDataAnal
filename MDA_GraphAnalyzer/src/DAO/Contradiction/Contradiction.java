package DAO.Contradiction;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by ando on 19/06/14.
 */
public class Contradiction implements Serializable{

    @SerializedName("topicId")
    private int id;
    @SerializedName("contradictions")
    private ContradictionPoint[] contradictions;

    public Contradiction(int id, ContradictionPoint[] contradictions) {
        this.id = id;
        this.contradictions = contradictions;
    }

    public Contradiction() {
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public ContradictionPoint[] getContradictions() {
        return contradictions;
    }

    public void setContradictions(ContradictionPoint[] contradictions) {
        this.contradictions = contradictions;
    }
}
