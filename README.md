REQUIREMENTS
- Python 3
- A Google developer account

SETUP
- Firstly, you will need a Google Cloud account. Go to https://cloud.google.com/ and create a developer account
- You will also need to install the Google Cloud SDK on your machine. Go to  https://cloud.google.com/sdk/docs/install and follow the instructions to Initialise the SDK on your machine.
- When you initialise the sdk you will need to create a new project and sign in with your google account (you’ll need to enter a projectID which must be unique)
- After you have initialised the SDK you need to set up the Natural Language Processing API. Go to this link https://cloud.google.com/natural-language/docs/setup and follow the instructions. 
    - You will need to name and create a new  project in the dashboard.
    - Then you need to enable the API (Cloud Natural Language Processing API) for your project in the marketplace. In the dashboard click API Overview -> Library -> search for Cloud Natural Language Processing API -> Enable.
    - Once you have enabled the API you will need credentials. There should be a pop-up asking you to create some, if not go to https://cloud.google.com/natural-language/docs/setup and follow the instructions for creating a service account. 
      NOTE: when you create the service account, for the 'Role' put 'Project -> Owner' and for the key type make sure JSON is selected. Once you click Continue, a file should be downloaded. This is your key.
    - Once your key is downloaded, move it to the folder of this project. NOTE: There cannot be another .json file in this folder, only the key. 
    - Then you need to tell the script to use this file as the key. Copy the filename of your key. Open google_analse_sentiment.py with a text editor and change the variable called  SERVICE_ACCOUNT_JSON to the full filename of your key. It must be in quotations.
- You need to install some external libraries for python. Open the terminal app and type the following commands:
    - pip install --upgrade google-cloud-language  <- For help see https://cloud.google.com/natural-language/docs/reference/libraries#command-line
    - pip install textblob


IMPORTANT NOTE
- If you do not/cannot do the above steps, i.e. setting up and authenticating Google Cloud credentials, then this program will still run. 
  If no Google JSON key is supplied, then the script will use a library called Textblob for sentiment analysis. 
  Textblob is a simple, free text analysis method. The docs are here https://textblob.readthedocs.io/en/dev/ .
  However, this method is not as accurate as the Google NLP API, and you will get different results depending which method you use.
  I have included this because setting up Google Cloud can be difficult, and this will work as a solution if you cannot get it working.
- Depending on whether you use Google Cloud or Textblob, you will get slightly different metrics as results. 
    - Google cloud returns variables Sentiment and Magnitude, these are defined here https://cloud.google.com/natural-language/docs/reference/rest/v1/Sentiment
    - Textblob return variables Sentiment (called Polarity in the documentation) and Subjectivity, the documentation/definition is here https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
    - Subjectivity and Magnitude ARE NOT THE SAME. They correspond to the subjectivity and emotional strength respectively. 
    - However, both methods return Sentiment which ARE THE SAME, and corresponds to the overall emotional leaning. This result will differ between methods due to accuracy.
  


INSTRUCTIONS
- Download this project: This can be done by clicking the green 'Code' button in the top right of this repo. Download the project as a zip and unzip once downloaded.
- Complete the SETUP section to set up Google Cloud SDK and libraries. (Not essential but highly recommended)
- Install external libraries: I tried to write this using as little libs as possible, but you still need some. Open the terminal/command line and type the following commands:
  - pip3 install textblob (if you haven't already from the setup stage)
- In the project there are files and folders. Relevant ones are described:
  - main.py : this is the file you need to run the program. You should have edited this file with your Google Cloud JSON key from the SETUP stage.
  - input folder : This is a folder of CSV files for analysis. 
      - If you are analysing Tweets collected using the TwitterScraper script, then simply copy the contents of the TwitterScraper output into the input folder.
      - If you are NOT analysing Tweets collected using the TwitterScraper script, then the CSVs rows must take the structure [Tweet_ID,Date,Text,Author_ID]. 
        Just set the fields Tweet_ID, Author_ID and date to 0, so that each row takes the form [0,0,text,0].
  - output folder : each file in the input folder will have an output folder with the lines of text analysed. 
    Two fields are appended to the CSV. These will either be (sentiment, magnitude) if using Google, or (sentiment, subjectivity) if using textblob. (See IMPORTANT NOTE section). 
    There is also a summary.csv file created which summarises total and average Sentiment, Magnitude/Subjectivity, and the total number of tweets. Each file in the input folder has one row in the summary.csv file
- open Terminal/Command Line app and change directory to this project folder. If the project is in your downloads folder then run the following command:
  - cd downloads/sentimentAnalysis-main 
- Enter the command 'python main.py'. This will run the application
- The script should run and start logging sentiment analysis. Check the logging to make sure Google credentials work (if you are using them), and for any errors in reading files. Output is stored in the ouutput folder. 