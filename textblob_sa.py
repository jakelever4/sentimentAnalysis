from textblob import TextBlob
import mutil


def analyse_textblob(text):
    textblob = TextBlob(text)
    return textblob.sentiment.polarity, textblob.sentiment.subjectivity


def analyse(writer, summary_writer, reader, filename):
    writer.writerow(['Tweet_ID', 'Date', 'Text', 'Author_ID', 'sentiment', 'subjectivity'])
    polarity = []
    subjectivity = []

    for row in reader:
        try:
            tweet_id, date, full_text, author_id = row[0], row[1], mutil.remove_url(row[2]), row[3]
        except KeyError:
            print('File structure unknown. Cannot Analyse')
            return

        p, s = analyse_textblob(full_text)
        # print(full_text)
        # print('Polarity: {}. Subjectivity: {}'.format(p, s))

        polarity.append(p)
        subjectivity.append(s)
        writer.writerow([row[0], row[1], row[2], row[3], p, s])

    print('Sentiment analysis results for index: {}'.format(filename))
    sum_p, sum_s, num_tweets = sum(polarity), sum(subjectivity), len(polarity)
    avg_p = sum_p / len(polarity)
    avg_s = sum_s / len(subjectivity)
    summary_writer.writerow([filename.replace('.csv', ''), avg_p, sum_p, avg_s, sum_s, num_tweets])

    print('AVG Sentiment: {}'.format(avg_p))
    print('SUM Sentiment: {}'.format(sum_p))
    print('AVG Subjectivity: {}'.format(avg_s))
    print('SUM Subjectivtiy: {}'.format(sum_s))
    print('num tweets {}'.format(num_tweets))