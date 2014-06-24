package DAO.Tweet;


import com.google.gson.annotations.SerializedName;

/**
 * Created by ando on 19/06/14.
 */
public class Tweet {
    @SerializedName("text")
    private String text;
    @SerializedName("time")
    private Long time;

    public Tweet() {
        this.text = new String();
        this.time = null;
    }

    public Tweet(String text, Long time) {
        this.text = text;
        this.time = time;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public Long getTime() {
        return time;
    }

    public void setTime(Long time) {
        this.time = time;
    }
}
