#!/bin/bash
rm -r data
rm -r logs
mkdir logs
mkdir data
chmod -R 777 logs/
chmod -R 777 data/

echo "LOG OF CHIRPANALYTICA-TRAINING: " &> logs/log.txt
currentDate=`date`
echo $currentDate >> logs/log.txt
pip3 install -r requirements.txt 
curl -H "Accept: text/csv" -o data/usernames.csv https://query.wikidata.org/sparql?query=SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%20%3Ftwitter%20%3Fparty%20%3FpartyLabel%0AWHERE%20%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5%3B%20%23%20item%20is%20a%20human%20being%0A%20%20%20%20%20%20%20%20wdt%3AP102%20%3Fparty%3B%0A%20%20%20%20%20%20%20%20wdt%3AP2002%20%3Ftwitter.%0A%20%20%3Fparty%20wdt%3AP31%20wd%3AQ2023214.%20%23%20party%20is%20a%20German%20party%0A%20%20FILTER%20NOT%20EXISTS%20%7B%0A%20%20%20%20%3Fparty%20wdt%3AP576%20%3Fend.%20%23%20party%20has%20not%20been%20dissolved%0A%20%20%7D%0A%20%20FILTER%20NOT%20EXISTS%20%7B%0A%20%20%20%20%3Ftwitter%20pq%3AP582%20%3FtwitterEnd.%20%23%20twitter%20has%20not%20been%20deleted%0A%20%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22de%2C%5BAUTO_LANGUAGE%5D%22.%20%7D%0A%7D &>> logs/log.txt
python3 tweetdownloader.py &> logs/log_tweetdownloader.txt
rm -r export
mkdir export
touch export/export_count.dat
touch export/export_tfidf.dat
touch export/export_clf.dat
touch export/export_fractions.dat
chmod -R 777 export/

python3 train.py &> logs/log_training.txt
echo "Finished train.sh."