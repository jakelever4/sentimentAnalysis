from google.cloud import language_v1
import Sentiment
from google.api_core import exceptions
import mutil


def analyse(writer, summary_writer, reader, filename, SERVICE_ACCOUNT_JSON):
    writer.writerow(['Tweet_ID', 'Date', 'Text', 'Author_ID', 'sentiment', 'magnitude'])
    sentiment = []
    magnitude = []
    for row in reader:
        try:
            tweet_id, date, full_text, author_id = row[0], row[1], mutil.remove_url(row[2]), row[3]
        except KeyError:
            print('File structure unknown. Cannot Analyse')
            return

        sent = SA_text(full_text, service_account=SERVICE_ACCOUNT_JSON)
        if sent is None:
            return

        sentiment.append(sent.score)
        magnitude.append(sent.magnitude)
        writer.writerow([row[0], row[1], row[2], row[3], sent.score, sent.magnitude])

    print('Sentiment analysis results for index: {}'.format(filename))
    sum_s, sum_m, num_tweets = sum(sentiment), sum(magnitude), len(magnitude)
    avg_s = sum_s / len(sentiment)
    avg_m = sum_m / len(magnitude)
    summary_writer.writerow([filename.replace('.csv', ''), avg_s, sum_s, avg_m, sum_m, num_tweets])

    print('AVG Sentiment: {}'.format(avg_s))
    print('SUM Sentiment: {}'.format(sum_s))
    print('AVG Magnitude: {}'.format(avg_m))
    print('SUM Magnitude: {}'.format(sum_m))
    print('num tweets {}'.format(num_tweets))


def SA_text(text_content, service_account):
    client = language_v1.LanguageServiceClient.from_service_account_json(service_account)
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type_": type_}
    encoding_type = language_v1.EncodingType.UTF8

    try:
        response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
    except exceptions.InvalidArgument as e:
        # if there is an invalid exception
        print('ERROR ANALYSING TEXT USING GOOGLE ANALYSIS:')
        print(e.message)
        return None

    # Score is the overall emotional learning of the text
    # Magnitude indicates the overall strength of the emotion.

    score = response.document_sentiment.score
    magnitude = response.document_sentiment.magnitude
    sentimemt = Sentiment.Sentiment(score, magnitude)
    print('SA RESULTS TEXT: {}'.format(text_content))
    print(sentimemt)

    return sentimemt
