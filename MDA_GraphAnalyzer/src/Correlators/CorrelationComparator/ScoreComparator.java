package Correlators.CorrelationComparator;

import Correlators.Correlation;

import java.util.Comparator;

/**
 * Created by ando on 10/07/14.
 */
public class ScoreComparator implements Comparator<Correlation> {
    private int index;

    public ScoreComparator(int i){
        this.index = i;
    }

    @Override
    public int compare(Correlation o1, Correlation o2) {
        if (o1.getScore()[index].getScore() < o2.getScore()[index].getScore()) return 1;
        if (o1.getScore()[index].getScore() > o2.getScore()[index].getScore()) return -1;
        return 0;
    }
}
