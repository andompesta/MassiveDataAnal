package DAO.News;

import com.mongodb.*;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

/**
 * Created by ando on 19/06/14.
 */
public class MongoDB {
    private String host;
    private String dbName;
    private int port;

    private MongoClient mClient;
    private DB db;

    public MongoDB(){
        host = "localhost";
        dbName = "MDA_News";
        port = 27017;
    }


    public void dbConnection(){
        try{
            this.mClient = new MongoClient(host, port);
            this.db = mClient.getDB(dbName);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    public void dbConnectionClose(){
        try{
            this.mClient.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public DBCollection getCollection(String collectionName){
        try{
            DBCollection col = db.getCollection(collectionName);
            return col;
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }
    }

    public ArrayList<News> getNews(DBCollection coll){
        ArrayList<News> ret = null;
        try{
            ret = new ArrayList<News>();
            DBCursor newsIterator = coll.find();
            while(newsIterator.hasNext()){
                DBObject temp = newsIterator.next();
                SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
                String d = (String) temp.get("pub_date");
                d = d.substring(0,10);
                Date pubDate = formatter.parse(d);
                DBObject headline = (DBObject) temp.get("headline");
                News news = new News((String)temp.get("full_text"), pubDate.getTime(),(String) temp.get("lead_paragraph"), (String) headline.get("main"));
                ret.add(news);
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        return ret;
    }

    public DBCollection createCollection(String CollectionName){
        try{
            DBObject options = BasicDBObjectBuilder.start().add("capped", true).get();
            DBCollection col = db.createCollection(CollectionName,options);
            return col;
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }
    }
/*
    public void modifyDoc(DBCollection coll,BasicDBObject searchObj, BasicDBObject newObj ){

        try{
            coll.update(searchObj, newObj);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
*/
    /*
    public void insertTweet(DBCollection coll, String name, String twett, String date){
        try{
            BasicDBObject doc = new BasicDBObject("Name", name).
                              append("Tweet", twett).
                            append("Date", date);
            coll.insert(doc);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    */
    /*
    public DBCursor getDocuments(DBCollection coll){
        DBCursor els = null;
        try{
            els = coll.find();
        }catch(Exception e){
            e.printStackTrace();
        }
        return els;
    }
    */
}
