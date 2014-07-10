package Main;

import Correlators.Correlation;
import Correlators.CorrelationComparator.ScoreComparator;
import Correlators.Score;
import DAO.Summary.SentenceByCP;
import DAO.Summary.SentenceScore;
import Utils.NewsSummarizerDoJob;
import com.google.gson.Gson;
import gr.demokritos.iit.jinsect.documentModel.comparators.NGramCachedGraphComparator;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramGraph;
import gr.demokritos.iit.jinsect.documentModel.representations.DocumentNGramSymWinGraph;
import gr.demokritos.iit.jinsect.structs.GraphSimilarity;

import java.io.*;
import java.util.*;

/**
 * Created by ando on 07/07/14.
 */
public class NewsSummarizer {

    public static void main(String[] args){
        String computationType = "truncate";
        int wSize = 2678400;
        try{

            for (int i = 3 ; i < 8 ; i++){
            NewsSummarizerDoJob summarizer = new NewsSummarizerDoJob(wSize, computationType, i);
                summarizer.doJob();
            }
        }catch(Exception e )
        {e.printStackTrace();}
    }
}
