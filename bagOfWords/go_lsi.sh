lsiDim=${1}
topS=${2}

echo "LSI [Cern] lsi-dimensions: ${lsiDim} top-s: ${topS}"
python lsi2.py data/tweets/Cern.json data/news/ok_Cern.json  data/contradictions/info/Cern.json data/contradictions/tweets/Cern-contr-tweet.json ${lsiDim} ${topS} config.ini data/results/lsi/lsi_Cern.json

echo "LSI [FortHood] lsi-dimensions: ${lsiDim} top-s: ${topS}"
python lsi2.py data/tweets/FortHood.json data/news/ok_FortHood.json  data/contradictions/info/FortHood.json data/contradictions/tweets/FortHood-contr-tweet.json ${lsiDim} ${topS} config.ini data/results/lsi/lsi_FortHood.json

echo "LSI [Hangover] lsi-dimensions: ${lsiDim} top-s: ${topS}"
python lsi2.py data/tweets/Hangover.json data/news/ok_Hangover.json  data/contradictions/info/Hangover.json data/contradictions/tweets/Hangover-contr-tweet.json ${lsiDim} ${topS} config.ini data/results/lsi/lsi_Hangover.json

echo "LSI [Lcross] lsi-dimensions: ${lsiDim} top-s: ${topS}"
python lsi2.py data/tweets/Lcross.json data/news/ok_Lcross.json  data/contradictions/info/Lcross.json data/contradictions/tweets/Lcross-contr-tweet.json ${lsiDim} ${topS} config.ini data/results/lsi/lsi_Lcross.json

echo "LSI [MichaelJackson] lsi-dimensions: ${lsiDim} top-s: ${topS}"
python lsi2.py data/tweets/MichaelJackson.json data/news/ok_MichaelJackson.json  data/contradictions/info/MichaelJackson.json data/contradictions/tweets/MichaelJackson-contr-tweet.json ${lsiDim} ${topS} config.ini data/results/lsi/lsi_MichaelJackson.json

echo "LSI [SwineFlu] lsi-dimensions: ${lsiDim} top-s: ${topS}"
python lsi2.py data/tweets/SwineFlu.json data/news/ok_SwineFlu.json  data/contradictions/info/SwineFlu.json data/contradictions/tweets/SwineFlu-contr-tweet.json ${lsiDim} ${topS} config.ini data/results/lsi/lsi_SwineFlu.json
