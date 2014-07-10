package DAO.Summary;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by ando on 08/07/14.
 */
public class SentenceByCP {
    private Set<String>[] sentenceCollection;

    public SentenceByCP(int lenght) {
        this.sentenceCollection = new HashSet[lenght];
    }

    public Set<String>[] getSentenceCollection() {
        return sentenceCollection;
    }

    public void setSentenceCollection(Set<String>[] sentenceCollection) {
        this.sentenceCollection = sentenceCollection;
    }

    public void insertSentence(String sentence, int index){
        this.sentenceCollection[index].add(sentence);
    }

    public void printSentence(String dataPath, String arg, String topicName, int neighbourhoodDistance) throws FileNotFoundException, UnsupportedEncodingException {
        for (int i = 0; i < this.sentenceCollection.length; i++){
            PrintWriter pf = new PrintWriter(dataPath +"/" +arg + "/" + topicName +"/"+ neighbourhoodDistance +"/Sentence-CP-"+i+".txt","UTF-8");
            String printSentence = "";
            for (String text : this.getSentenceCollection()[i]){
                printSentence += text + "\n";
            }
            pf.write(printSentence);
            pf.close();
        }
    }
}
