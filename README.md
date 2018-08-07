# Victorian Election Violence Crawler
The aim of this project is to crawl news from [British Newspaper Archive](https://www.britishnewspaperarchive.co.uk/) and [Welsh Newspapers Online](http://newspapers.library.wales/) sites.

## Version
The current version of the project is **v1.28.2**. The change history can be seen in the [Change Log](/changelog.md)

## Requirements
This project is developed and maintained using Python 2.7. A list of requirements can be found [here](/requirements.txt). 
The last version of the project uses **openpyxl 2.5.5**. You can install it by using `$ pip install openpyxl` or using Anaconda.

## Usage
### Crawling
To execute the crawler, first go to the root directory (where this README.md file is) and open the console. The most basic form of running the crawler is by typing `scrapy crawl (BNA|WNO)`, where BNA refers to British Newspaper Archive and WNO to Welsh Newspapers Online.

#### BNA
To crawl on the BNA site, you have to define the search terms. Currently, there are two ways of defining this search terms: a *basic* and an *advanced* mode. 
For the *basic* mode, you have to define the search terms in the 'Crawler/spiders/BNA_search_input.csv'. This CSV file needs to have the following format. An example is found [here](/Crawler/spiders/BNA_search_input.csv).

keyword | start day(xxxx-xx-xx) | end day(xxxx-xx-xx)
------- | --------------------- | ------------------|
Election riot | 1850-05-14 | 1870-02-27
Election Violence | 1800-02-01 | 1810-01-31

By default, the crawler runs in the basic mode. You can specify this option explicitly adding the *search* option on the command (see below).

To activate *advanced* mode, you have to set the option (see below). Search terms are defined at 'Crawler/spiders/BNA_advanced_search.xlsx'. Excel 2010+ or any software supporting xlsx files is needed. In this file, a table with the required fields is shown. Each field is optional, but you have to define at least one keyword on the first 4 columns. The fields for the advanced search are the following.

* **Search all words**
  * Type: text
  * Description: all the words written here have to appear in the result
* **Search some words**
  * Type: text
  * Description: at least one word of these has to appear in the result
* **Use exact phrase**
  * Type: text
  * Description: the exact phrase must appear on the result
* **Exclude words**
  * Type: text
  * Description: the result must not have any of these words
* **Exact search**
  * Type: integer (either 1 or 0 )
  * Description: if 1, search the exact terms (E.g. search for "fish" and not "fishing" or "fished").
* **Publication place**
  * Type: text (you must select one of the elements on the list)
  * Description: the place where the news was published
  * Comment: if no dropdown list appears, you can go to the *Places* tab and copy one location
* **Newspaper title**
  * Type: text (you must select one of the elements on the list)
  * Description: the newspaper which published the news
  * Comment: if no dropdown list appears, you can go to the *Newspapers* tab and copy one newspaper
* **From date**
  * Type: date text in *yyyy-mm-dd* format
  * Description: the start date to look for news
* **To date**
  * Type: date text in *yyyy-mm-dd* format
  * Description: the end date to look for news
* **From date added**
  * Type: date text in *yyyy-mm-dd* format
  * Description: the start date where the news was added to the system
* **To date added**
  * Type: date text in *yyyy-mm-dd* format
  * Description: the end date where the news was added to the system
* **Article type**
  * Type: text (you have to choose from *Advertisement, Article, FamilyNotice, Illustrated* or *Miscellaneous*)
  * Description: the type of news looked
  * Comment: if you want to search for more than two types of news, you can specify them separating with a comma. (E.g. Advertisement,FamilyNotice)
* **Front page articles only**
  * Type: integer (either 1 or 0)
  * Description: select 1 if you are looking only for front page articles only.
* **Tags**
  * Type: text
  * Description: search for articles with the specified tags (however, many articles have no tags)
* **Sort results by**
  * Type: text (you have to choose from *Relevance*(default), *Date (earliest)* or *Date (most recent)*)
  * Description: sets the order of the articles. 
  
##### Options
When crawling the BNA site, you can define some options as arguments in the console. Each option has to be added as `-a option=value`. The BNA spider has the following options

* **search**
  * Values: basic (default) | advanced
  * Description: sets the search mode.
* **mode**
  * Values: slow (default) | fast
  * Description: when mode is slow, OCRs are downloaded. To achieve this, the system must login into the BNA site, and sometimes this may slowdown the project. When mode is fast, the OCRs are omitted (thus, no login is required).
* **generate_json**
  * Values: false (default) | true
  * Description: when this option is true, a json file is generated at Crawler/Records. If it is set to false, no json file is generated and search results are only stored at the database.

An example of a crawl with advanced search, fast mode and json generation is obtained by typing `scrapy crawl BNA -a search=advanced -a mode=fast -a generate_json=true`

#### WNO
To crawl on the WNO site, search terms are defined in [Crawler/spiders/BNA_search_input.csv](/Crawler/spiders/WNO_search_input.csv). The format is the following

keyword | start_date(xxxx) | end_date(xxxx)
------- | --------------------- | ------------------|
Election riot | 1850| 1870
Victorian | 1800 | 1810

Currently, WNO site has no options.

#### Results
If generate_json is set to true, results are stored in a json file on Crawler/Records (except if you are crawling the BNA with generate_json=false). Candidate documents with status different from 1 or 0 are downloaded in a csv file (a csv and a json file is generated for each row on the search input files). The name of these files are constructed as *site_keyword_startdate_enddate.csv*. For example, *britishnewspaperarchive_Violence_1800-01-05_1800-01-06.csv*

### Download Candidates
After a crawling, you will have to download the documents you are interested. Before executing the script to download these documents, you have to select which candidate documents you need. For this, go to the csv file generated on Crawler/Records. In the Status field, you have to type one of the following: __0__ if you want to discard the document, __1__ if you want to download it or __2+__ if you want to see it later.
To update these status into the database and to download the candidate documents with status 1, on the root folder (**Note: this is important, because for previous versions you have to go to the Tools folder, which was removed**) type `python download_candidates.py`.
Then, the script will ask you the file with the results. Enter the name of the file without extension (E.g., if the file is named *britishnewspaperarchive_Violence_1800-01-05_1800-01-06.csv*, you have to write *britishnewspaperarchive_Violence_1800-01-05_1800-01-06*). The system will automatically detect if the JSON file is present. If this is not the case, the program will automatically download the OCR for the Portal documents (and **not** for the corresponding candidate document record).
If you are downloading candidates searched on the WNO site, you will be asked if you want to download the High Resolution version. You should always write 'Y'. This option is now deprecated (kept for legacy) and may be removed later.

### Update PDF files
Sometimes, an error occurs while downloading the article PDF. In these cases, the article information is in the database but its corresponding PDF file is not in the server. Thus, a script is provided to try to download again those files. 
To use this script, type `python update_pdf_files.py`. When executing this, a csv file called *nopdfarticles.csv* is generated and the script is halted with a *Press Enter to continue* message. Before you press enter, check the csv file and delete the candidate documents you are not interested. Then, go back to the script and press enter. It will try to download all candidate documents specified in the csv. If you have tried this more than 3 times and a candidate is not being downloaded, please contact the developer team.

### OCR updater
When the advanced mode for the BNA is used, the OCR of the candidates are not downloaded. If you want to download the OCR of those candidate documents with a blank OCR, type `python ocr_updater.py` on the root folder

## Contact
If you have any doubt or experience any problem, contact me (Brian Isaac - brian.k.isaac-medina@durham.ac.uk) 
