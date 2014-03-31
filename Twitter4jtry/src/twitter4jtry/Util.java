/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package twitter4jtry;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import hirondelle.date4j.DateTime;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.net.UnknownHostException;
import java.util.ArrayList;
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
import dbManagement.CollectionManager;
import dbManagement.MongoManager;
import DAO.Tweet;
import java.util.Map;
import java.util.Set;
import org.bson.BSONObject;

/**
 *
 * @author Sandro
 */
public class Util {
    
    private CollectionManager colMr;
    private MongoManager mongoMr;
    private StringU stringCheker;
    
    public Util() throws UnknownHostException {
        mongoMr = new MongoManager();
        mongoMr.dbConnection();
        colMr = new CollectionManager(mongoMr);
        stringCheker = new StringU();
    }
    
    public void captureTwettStream(){
        final TimeZone myZone = TimeZone.getDefault();
        
        StatusListener listener = new StatusListener() {
            @Override
            public void onStatus(Status status) {
                
                DateTime now = DateTime.now(myZone);
                
                String name = status.getUser().getScreenName();
                String message = status.getText();
                
                message = stringCheker.controlTweet(message);
                
                
                try {
                        System.out.println();
                        System.out.println("|------------------------------------------|");
                        System.out.println("Name = "+name);
                        System.out.println("Tweet = "+message);
                        System.out.println("Date = "+now.format("YYYY-MM-DD hh:mm:ss"));
                        
                        message = URLEncoder.encode(message, "UTF-8");
                        
                        Tweet tweet = new Tweet();
                        tweet.put("Name", name);
                        tweet.put("Tweet", message);
                        tweet.put("Date", now);
                        
                        //System.out.println("{ \"name\" : \"" + name + "\" , \"twett\" : \"" + status.getText()+"\" , \"date\" : \"" + date+"\" }\n");
                        colMr.getTwettsCol().insert(tweet);
                        
                } catch (UnsupportedEncodingException ex) {
                    Logger.getLogger(Twitter4jtry.class.getName()).log(Level.SEVERE, null, ex);
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
        double[][] bb = {{-6.252622, 50.488032}, {2.252622, 57.488032}};

        String[] language = { "en" };
        qfilter.locations(bb);
        qfilter.language(language);
        
        // filter() method internally creates a thread which manipulates TwitterStream and calls these adequate listener methods continuously.
        twitterStream.filter(qfilter);
    }
    
    
    public void fixTweets() throws UnsupportedEncodingException{
        colMr.getTwettsCol().setObjectClass(Tweet.class);
        DBCursor tweetCur = colMr.getTwettsCol().find();
        
        int i = 0;
        int col_size = (int) colMr.getTwettsCol().count();
        
        while(tweetCur.hasNext() && i<col_size){
            i++;
            
            Tweet t = (Tweet) tweetCur.next();
            
            String message = t.getString("Tweet");
            message = message.replaceAll("%3F","");
            message = URLDecoder.decode(message, "UTF-8");
            message = stringCheker.controlTweet(message);
            
            System.out.println(i);
            System.out.println(message);
            
            ArrayList<String> tags = new ArrayList();
            ArrayList<String> links = new ArrayList();
            boolean notEmptyTag = false;
            boolean notEmptyLink = false;
            
            for(String temp: message.split(" ")){
                if(temp.startsWith("#")){
                    tags.add(temp);
                    notEmptyTag = true;
                }
                else if(temp.startsWith("http")){
                    links.add(temp);
                    notEmptyLink = true;
                }
            }
            
            if(notEmptyTag && notEmptyLink){
                t.put("Tags", tags);
                t.put("Links", links);
            }
            else if(notEmptyTag)
                t.put("Tags", tags);
            else if(notEmptyLink)
                t.put("Links", links);
            
            if(notEmptyLink || notEmptyTag)
                colMr.getTwettsCol().save(t);
        }
        
    }
}
