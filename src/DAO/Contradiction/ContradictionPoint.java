package DAO.Contradiction;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by ando on 19/06/14.
 */
public class ContradictionPoint implements Serializable {
    @SerializedName("cValue")
    private float cValue;
    @SerializedName("cType")
    private float cType;
    @SerializedName("timeBegin")
    private long timeBegin;
    @SerializedName("timeEnd")
    private long timeEnd;

    public ContradictionPoint() {
    }

    public ContradictionPoint(float cValue, float cType, long timeBegin, long timeEnd) {
        this.cValue = cValue;
        this.cType = cType;
        this.timeBegin = timeBegin;
        this.timeEnd = timeEnd;
    }

    public float getcType() {
        return cType;
    }

    public void setcType(float cType) {
        this.cType = cType;
    }

    public float getcValue() {
        return cValue;
    }

    public void setcValue(float cValue) {
        this.cValue = cValue;
    }

    public long getTimeBegin() {
        return timeBegin;
    }

    public void setTimeBegin(long timeBegin) {
        this.timeBegin = timeBegin;
    }

    public long getTimeEnd() {
        return timeEnd;
    }

    public void setTimeEnd(long timeEnd) {
        this.timeEnd = timeEnd;
    }
}
