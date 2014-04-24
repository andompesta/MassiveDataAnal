/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package dbManagement;

import DAO.Tweet;
import com.mongodb.BasicDBObject;
import com.mongodb.BasicDBObjectBuilder;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import java.net.UnknownHostException;

/**
 *
 * @author andocavallari
 */
public class MongoManager {
    private String host;
    private String dbName;
    private int port;
    
    private MongoClient mClient;
    private DB db;
    
    public MongoManager(){
        host = "localhost";
        dbName = "BigData";
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
   
    public DBCollection getCollection(String collectionName){
        try{
            DBCollection col = db.getCollection(collectionName);
            return col;
        }catch(Exception e){
            e.printStackTrace();
            return null;
        }
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
    
    public void modifyDoc(DBCollection coll,BasicDBObject searchObj, BasicDBObject newObj ){
        
        try{
            coll.update(searchObj, newObj);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    
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
