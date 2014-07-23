topK=${1}
topS=${2}

echo "TF-IDF [Cern] top-k: ${topK} top-s: ${topS}"
python tfidf2.py data/tweets/Cern.json data/news/ok_Cern.json  data/contradictions/info/Cern.json data/contradictions/tweets/Cern-contr-tweet.json ${topK} ${topS} config.ini data/results/tfidf/tfidf_Cern.json

echo "TF-IDF [FortHood] top-k: ${topK} top-s: ${topS}"
python tfidf2.py data/tweets/FortHood.json data/news/ok_FortHood.json  data/contradictions/info/FortHood.json data/contradictions/tweets/FortHood-contr-tweet.json ${topK} ${topS} config.ini data/results/tfidf/tfidf_FortHood.json

echo "TF-IDF [Hangover] top-k: ${topK} top-s: ${topS}"
python tfidf2.py data/tweets/Hangover.json data/news/ok_Hangover.json  data/contradictions/info/Hangover.json data/contradictions/tweets/Hangover-contr-tweet.json ${topK} ${topS} config.ini data/results/tfidf/tfidf_Hangover.json

echo "TF-IDF [Lcross] top-k: ${topK} top-s: ${topS}"
python tfidf2.py data/tweets/Lcross.json data/news/ok_Lcross.json  data/contradictions/info/Lcross.json data/contradictions/tweets/Lcross-contr-tweet.json ${topK} ${topS} config.ini data/results/tfidf/tfidf_Lcross.json

echo "TF-IDF [MichaelJackson] top-k: ${topK} top-s: ${topS}"
python tfidf2.py data/tweets/MichaelJackson.json data/news/ok_MichaelJackson.json  data/contradictions/info/MichaelJackson.json data/contradictions/tweets/MichaelJackson-contr-tweet.json ${topK} ${topS} config.ini data/results/tfidf/tfidf_MichaelJackson.json

echo "TF-IDF [SwineFlu] top-k: ${topK} top-s: ${topS}"
python tfidf2.py data/tweets/SwineFlu.json data/news/ok_SwineFlu.json  data/contradictions/info/SwineFlu.json data/contradictions/tweets/SwineFlu-contr-tweet.json ${topK} ${topS} config.ini data/results/tfidf/tfidf_SwineFlu.json
