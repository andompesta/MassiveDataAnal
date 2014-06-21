import java.io.*;

public class ProgBar {
	private int nchars_;
	private int total_;
	private int old_p_;

	public ProgBar(int nchars, int total) {
		nchars_ = nchars;
		total_ = total;
		old_p_ = 0;
	}

	public void printProg(int p) {
		float percentage = (float)p / total_;
		if (percentage - old_p_ < 0.01)
			return;
		old_p_ = (int)percentage;
		int to_print = (int) (percentage * nchars_);
		System.out.printf("\r[");
		for (int i = 0; i < to_print; i++)
			System.out.printf("*");
		for (int i = 0; i < nchars_ - to_print; i++)
			System.out.printf(" ");
		System.out.printf("] %d%%", (int)(percentage*100));
	}
}
