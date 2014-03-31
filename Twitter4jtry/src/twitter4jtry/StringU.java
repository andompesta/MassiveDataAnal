/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package twitter4jtry;

import java.io.FileWriter;
import java.io.IOException;

/**
 *
 * @author andocavallari
 */
public class StringU {
    
    public StringU(){}
    
    public String controlTweet(String tweet){
        tweet = tweet.replaceAll("“","");
        tweet = tweet.replaceAll("”","");
        return tweet;
    }
    
    public String controlTweetAll(String tweet){
        tweet = tweet.replaceAll("“","");
        tweet = tweet.replaceAll("”","");
        tweet = tweet.replaceAll("\"","");
        return tweet;
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
    
    public String deleteDuplicate(String tweet){
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
