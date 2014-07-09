package DAO.Summary;

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
}
