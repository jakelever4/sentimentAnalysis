# Written by Jake Lever 03/2021
import os
import csv
import textblob_sa
import google_analyse_sentiment

SERVICE_ACCOUNT_JSON = 'twitter-scraper-project-1c243893775e.json'


def check_for_gcloud_credentials():
    if SERVICE_ACCOUNT_JSON[-5:] == '.json':
        print('NOTE: Google Service account found. Using credentials: {}'.format(SERVICE_ACCOUNT_JSON))
        return True
    else:
        print('NOTE: No Google service credentials found. Using textblob for sentiment analysis instead.')
        return False


gcloud = check_for_gcloud_credentials()
files = os.listdir('input')
with open('output/summary.csv', 'w', newline='') as csv_summary:
    s_writer = csv.writer(csv_summary, delimiter=',', quoting= csv.QUOTE_MINIMAL)
    if gcloud:
        s_writer.writerow(['filename', 'avg_sentiment', 'sum_sentiment', 'avg_magnitude', 'sum_magnitude', 'num_tweets'])
    else:
        s_writer.writerow(['filename', 'avg_polarity', 'sum_polarity', 'avg_subjectivity', 'sum_subjectivity', 'num_tweets'])

    for filename in files:
        with open('input/' + filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)
            with open('output/' + filename.replace('.csv', '') + '_analysed.csv', 'w', newline='') as csv_out:
                writer = csv.writer(csv_out, delimiter=',', quoting= csv.QUOTE_MINIMAL)
                if gcloud:
                    google_analyse_sentiment.analyse(writer, s_writer, reader, filename, SERVICE_ACCOUNT_JSON)
                else:
                    textblob_sa.analyse(writer, s_writer, reader, filename)

                print('Sentiment Analysis performed successfully. See output folder for results.')


