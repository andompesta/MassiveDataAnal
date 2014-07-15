TEXFILES_REPORT:=report.tex $(shell ls chapters/*.tex chapters/results/*.tex)

report.pdf: ${TEXFILES_REPORT}
	@${MAKE} --no-print-directory report.pdf-forced


report.pdf-forced:
	@echo "- PDFLATEX: report.pdf"
	@cat /dev/null | pdflatex -halt-on-error -file-line-error -interaction=nonstopmode  report.tex &> pdflatex.log; \
	if [ $$? != 0 ]; \
	then \
		cat pdflatex.log; \
		exit 1; \
	fi;
	@if grep "rerunfilecheck Warning" pdflatex.log > /dev/null ; \
	then \
		echo "   - 'rerunfilecheck Warning' found: Rerunning pdflatex..."; \
		${MAKE} --no-print-directory report.pdf-forced; \
	fi;


clean:
	@TMP=`ls *.aux *.log *.pdf *.out`; \
	echo "- Cleaning: $${TMP}"; \
	rm $${TMP};


.PHONY: report.pdf-forced clean
