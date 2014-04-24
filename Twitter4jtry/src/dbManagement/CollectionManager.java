/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package dbManagement;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.MongoClient;

/**
 *
 * @author andocavallari
 */
public class CollectionManager {
    
    private DBCollection twettsCol;
    
    public CollectionManager(MongoManager mMr) {
        this.twettsCol = mMr.getCollection("Tweets");
    }

    public DBCollection getTwettsCol() {
        return twettsCol;
    }

    public void setTwettsCol(DBCollection twettsCol) {
        this.twettsCol = twettsCol;
    }
    
    
        
}
