/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package twitter4jtry;

import com.mongodb.DBCollection;
import hirondelle.date4j.DateTime;
import java.io.FileWriter;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.TimeZone;
import java.util.logging.Level;
import java.util.logging.Logger;
import twitter4j.FilterQuery;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;

/**
 *
 * @author Sandro
 */
public class Util {
    
    private String host;
    private String dbName;
    private int port;
    private DBCollection twettsCol;
    private MongoCollection MC;
    
    public Util() {
        host = "localhost";
        dbName = "BigData";
        port = 27017;
        connectToMongoDB();
    }
    
    
    
    private void connectToMongoDB(){
        try{
            MC = new MongoCollection(host, port);
            MC.dbConnection(dbName);
            twettsCol = MC.getCollection("Twetts");
            
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public void captureTwettStream(){
        final TimeZone myZone = TimeZone.getDefault();
        StatusListener listener = new StatusListener() {
        @Override
        public void onStatus(Status status) {
            
            DateTime now = DateTime.now(myZone);
            String date = now.format("YYYY-MM-DD hh:mm:ss");
            String name = status.getUser().getScreenName();
            String tweet = status.getText();

            //Remove reTwett from data set
            if(!tweet.contains("RT") && !tweet.isEmpty()){
                
                try {
                    tweet = deleteDuplicate(tweet);
                    tweet = URLEncoder.encode(tweet, "UTF-8");
                    System.out.println();
                    System.out.println("|------------------------------------------|");
                    System.out.println("name = "+name);
                    System.out.println("tweet = "+status.getText());
                    System.out.println("date = "+date);
                    //System.out.println("{ \"name\" : \"" + name + "\" , \"twett\" : \"" + status.getText()+"\" , \"date\" : \"" + date+"\" }\n");
                    MC.insertDocument(twettsCol, name, tweet, date);
                } catch (UnsupportedEncodingException ex) {
                    Logger.getLogger(Twitter4jtry.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }

        @Override
        public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {
            System.out.println("Got a status deletion notice id:" + statusDeletionNotice.getStatusId());
        }

        @Override
        public void onTrackLimitationNotice(int numberOfLimitedStatuses) {
            System.out.println("Got track limitation notice:" + numberOfLimitedStatuses);
        }

        @Override
        public void onScrubGeo(long userId, long upToStatusId) {
            System.out.println("Got scrub_geo event userId:" + userId + " upToStatusId:" + upToStatusId);
        }

        @Override
        public void onStallWarning(StallWarning warning) {
            System.out.println("Got stall warning:" + warning);
        }

        @Override
        public void onException(Exception ex) {
            ex.printStackTrace();
        }
    };

    TwitterStream twitterStream = new TwitterStreamFactory().getInstance();
    twitterStream.addListener(listener);

    FilterQuery qfilter = new FilterQuery();
    double[][] location = { { 6.3061523, 36.2265501 },{ 18.3251953, 46.9502622 } };
    String[] language = { "it" };
    qfilter.language(language);
    qfilter.locations(location);

    // filter() method internally creates a thread which manipulates TwitterStream and calls these adequate listener methods continuously.
    twitterStream.filter(qfilter);
    }
    
    public void writeStringToFile(String filePathAndName, String stringToBeWritten) throws IOException{
        try
        {
            String filename= filePathAndName;
            boolean append = true;
            FileWriter fw = new FileWriter(filename,append);
            fw.write(stringToBeWritten);//appends the string to the file
            fw.write("\n");
            fw.close();
        }
        catch(IOException ioe)
        {
            System.err.println("IOException: " + ioe.getMessage());
        }
    }
    
    
    private String deleteDuplicate(String tweet){
        String newStr = new String();
        
        for(String temp: tweet.split(" ")){
            int lng = temp.length() - 1;
            int i = 0;
            int lngStr = 0;
            String conStr = new String();
            while( i < temp.length()-1 ){
                if(i == temp.length() - 2){
                    conStr += temp.substring(lngStr, i+2);
                }
                //else if(i == temp.length() - 1){conStr += temp.substring(i,i+1);}
                else{
                    if(temp.substring(i,i+1).equals(temp.substring(i+1,i+2)) && 
                            temp.substring(i,i+1).equals(temp.substring(i+2,i+3))){
                        int j = 2;
                        if(i+1+j < lng){
                            while(temp.charAt(i) == temp.charAt(i+1+j) ){
                                j++;
                            }
                        }
                        conStr = conStr+temp.substring(lngStr, i+2);
                        lngStr = i+j+1;
                        i = i+j;
                    }
                    
                }
                i++;
            }
            newStr = newStr+" "+conStr;
        }
        
        newStr = newStr.substring(1);
        return newStr;
    }
    
}
