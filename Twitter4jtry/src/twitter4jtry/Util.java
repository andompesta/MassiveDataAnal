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
            String twett = status.getText();

            //Remove reTwett from data set
            if(!twett.contains("RT") && !twett.isEmpty()){
                
                try {
                    twett = URLEncoder.encode(twett, "UTF-8");
                    System.out.println();
                    System.out.println("|------------------------------------------|");
                    System.out.println("name = "+name);
                    System.out.println("twett = "+status.getText());
                    System.out.println("date = "+date);
                    //System.out.println("{ \"name\" : \"" + name + "\" , \"twett\" : \"" + status.getText()+"\" , \"date\" : \"" + date+"\" }\n");
                    MC.insertDocument(twettsCol, name, twett, date);
                    
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
    
}
