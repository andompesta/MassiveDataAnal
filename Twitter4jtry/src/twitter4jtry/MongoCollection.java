/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package twitter4jtry;

import com.mongodb.BasicDBObject;
import com.mongodb.BasicDBObjectBuilder;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import java.net.UnknownHostException;

/**
 *
 * @author andocavallari
 */
public class MongoCollection {
    private MongoClient mClient;
    private DB db;
    
    public MongoCollection(String hostIP, int port) throws UnknownHostException{
        this.mClient = new MongoClient(hostIP, port);   
        db = null;
    }
   
    public void dbConnection(String DbName){
        try{
            this.db = mClient.getDB(DbName);
        }catch(Exception e){
            e.printStackTrace();
        }
    }
   
    public DBCollection getCollection(String CollectionName){
        try{
            DBCollection col = db.getCollection(CollectionName);
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
    
    public void insertDocument(DBCollection coll, String name, String twett, String date){

        try{
            BasicDBObject doc = new BasicDBObject("Name", name).
                              append("Twett", twett).
                            append("Date", date);
            coll.insert(doc);
        }catch(Exception e){
            e.printStackTrace();
        }
    }    
}
