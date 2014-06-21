import java.util.List;
import java.util.ArrayList;

public class Stats {
	private	ArrayList<Integer> v;
	private	int min;
	private int min_idx;
	private	int max;
	private int max_idx;
	private	int sum;

	public Stats() {
		min = Integer.MAX_VALUE;
		max = Integer.MIN_VALUE;
		min_idx = max_idx = 0;
		sum = 0;
		v = new ArrayList<Integer>();
	}

	void notify(int i) {
		sum += i;
		v.add(i);
		if (i < min) {
			min = i;
			min_idx = v.size() - 1;
		}
		if (i > max) {
			max = i;
			max_idx = v.size() -1;
		}
	}

	float mean() {
		return (float) sum / v.size();
	}

	int min() {
		return min;
	}
	
	int minIndex() {
		return min_idx;
	}

	int max() {
		return max;
	}

	int maxIndex() {
		return max_idx;
	}

	float variance() {
		float m = mean();
		float s = 0;
		for (int i : v) {
			s += (i - m) * (i - m);
		}
		return s/v.size();
	}

	float stdDeviation() {
		return (float)Math.sqrt(variance());
	}
}
