# Victorian Election Violence Crawler
The aim of this project is to crawl news from [British Newspaper Archive](https://www.britishnewspaperarchive.co.uk/) and [Welsh Newspapers Online](http://newspapers.library.wales/) sites.

## Version
The current version of the project is **v1.31.4**. The change history can be seen in the [Change Log](/changelog.md)

## Requirements
This project is developed and maintained using Python 2.7. A list of requirements can be found [here](/requirements.txt). 

## Quick Start
1. Write the search terms either in BNA_search_input.csv | WNO_search_input.csv for basic search or BNA_advanced_search.xlsx for advanced search
1. Run the crawler using `scrapy crawl BNA|WNO [options]`
1. Generate the candidate documents list with `python generate_candidates.py`
1. Change the status of the candidate documents
1. Download the pdf files using `python download_candidates.py`

## Usage
### Crawling
To execute the crawler, go to the root directory (where this README.md file is) and open the console. The most basic form of running the crawler is by typing `scrapy crawl (BNA|WNO)`, where BNA refers to British Newspaper Archive and WNO to Welsh Newspapers Online.

#### BNA
To crawl on the BNA site, you have to define the search terms. Currently, there are two ways of defining these search terms: a *basic* and an *advanced* mode. 
For the *basic* mode, you have to define the search terms in the 'Crawler/spiders/BNA_search_input.csv'. This CSV has the following format. An example is found [here](/Crawler/spiders/BNA_search_input.csv).

keyword | start day(xxxx-xx-xx) | end day(xxxx-xx-xx)
------- | --------------------- | ------------------|
Election riot | 1850-05-14 | 1870-02-27
Election Violence | 1800-02-01 | 1810-01-31

By default, the crawler runs in the basic mode. You can specify this option explicitly adding the *search* option on the command (see below).

To crawl in *advanced* mode, you have to set the option (see below). Search terms are defined at 'Crawler/spiders/BNA_advanced_search.xlsx'. Excel 2010+ or any software supporting xlsx files is needed. In this file, a table with the required fields is shown. Each field is optional, but you have to define at least one keyword on the first 4 columns. The fields for the advanced search are the following.

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
  * Values: slow (default) | fast | recovery | count *(new)*
  * Description: when mode is slow, OCRs are downloaded. To achieve this, the system must login into the BNA site, 
  and sometimes this may slowdown the project. When mode is fast, the OCRs are omitted (thus, no login is required).
  Recovery mode continues the search after a failed crawling (see *Recovery mode* section). Count mode only counts the
  number of articles in a particular search (see *Count mode* section).
* **generate_json**
  * Values: false (default) | true
  * Description: when this option is true, a json file is generated at Crawler/Records. If it is set to false, no json file is generated and search results are only stored at the database.
* **split**
  * Values: none (default) | day | week | month | year | *integer*
  * Description: this option defines how searches will be divided in different time intervals. When *none* is selected,
  there will be only one search corresponding to the defined start and end dates. When another option is selected,
  the search will be divided in several searches, each one covering a time interval defined this option. For example,
  if the search start and end dates are 1918-01-19 and 1918-02-19, and if the split value is *week*, five searches will 
  be processed: 1918-01-19 to 1918-01-25, 1918-01-26 to 1918-02-01, 1918-02-02 to 1918-02-08, 1918-02-09 to 1918-02-15
  and 1918-02-16 to 1918-02-19. A positive integer can be passed to the split option define the number of days for 
  dividing the search. Although it has been tested with no problems, **this mode is not fully compatible with recovery 
  mode yet**
* **download_delay**
  * Decimal number (default = 2)
  * Description: This value sets a delay between requests in order to avoid a big load to the crawled server. 

An example of a crawl with advanced search, fast mode and json generation is obtained by typing `scrapy crawl BNA -a search=advanced -a mode=fast -a generate_json=true`

##### Recovery mode
After crawling a page, a **recovery** file is generated. This file contains the information
about the search inputs and the next page to be crawled, so it can be used if an error arises during
the crawling process. To use this recovery file, define the search mode as recovery (`-a mode=recovery`). It will use
the configurations from the last search, including the search type and mode, and it will run from the 
last page crawled (so, it is possible that some search results will be duplicated). 
**Note**: recovery mode must be used AFTER the failed crawled. If a search is performed after the failed
crawl, the recovery file will be overwritten with the new search.

##### Count mode
Count mode counts the articles in a search. The result will be shown in the console and it will be 
saved in the portal_archivesearchsummaryonly table. This mode can be used along with the split
option.

#### WNO
To crawl on the WNO site, search terms are defined in [Crawler/spiders/BNA_search_input.csv](/Crawler/spiders/WNO_search_input.csv). The format is the following

keyword | start_date(xxxx) | end_date(xxxx)
------- | --------------------- | ------------------|
Election riot | 1850| 1870
Victorian | 1800 | 1810

Currently, WNO site has no options.

#### Advanced
To avoid suspicion of an attack into the crawled sites, a delay of 3 seconds between each crawl is defined. 
If you **need** to speed up the crawling process, you can modify the DOWNLOAD_DELAY parameter in the [Crawler/settings.py](/Crawler/settings.py) file. 
This is not recommended because the site can block your IP if it detects the crawl as a hacker attack.

#### Results
If generate_json is set to true, results are stored in a json file on Crawler/Records. Otherwise, they're only stored in the data base. 
Also, a search_ids.csv file is created, which will be used to generate a list with the candidate documents related to the performed searchs.
The structure of this csv file is the following

id | filename 
------- | --------------------- 
630 | britishnewspaperarchive_election riot_1859-02-02_1859-05-02
631 | britishnewspaperarchive_election riot_1860-02-02_1860-05-02

The id column is the id of the search and the filename is the name of the CSV file that will be created when using the generate_candidates.csv script.

### Generate Candidates
In order to download candidates files (as their article or page pdf), it is needed to generate a CSV containing the candidates related with the search. Since version 1.29.0, this list is generated using the command `python generate_candidates.py`. The script will look for the file *search_ids.csv* generated after the crawl. Alternatively, this file can be manually created using the fields described in the previous section.
This script will download the information of candidate documents with status different from 1 or 0. The name of these files are constructed as *site_keyword_startdate_enddate.csv* (although you may manually write the filename in the search_ids.csv file). For example, *britishnewspaperarchive_Violence_1800-01-05_1800-01-06.csv*

### Download Candidates
After a crawling, you will have to download the documents you are interested. Before executing the script to download these documents, you have to select which candidate documents you need. For this, go to the csv file generated on Crawler/Records. In the Status field, you have to type one of the following: __0__ if you want to discard the document, __1__ if you want to download it or __2+__ if you want to see it later.
To update these status into the database and to download the candidate documents with status 1, on the root folder (**Note: this is important, because for previous versions you have to go to the Tools folder, which was removed**) type `python download_candidates.py`.
Then, the script will ask you the file with the results. Enter the name of the file without extension (E.g., if the file is named *britishnewspaperarchive_Violence_1800-01-05_1800-01-06.csv*, you have to write *britishnewspaperarchive_Violence_1800-01-05_1800-01-06*). The system will automatically detect if the JSON file is present. If this is not the case, the program will automatically download the OCR for the Portal documents (and **not** for the corresponding candidate document record).
If you are downloading candidates searched on the WNO site, you will be asked if you want to download the High Resolution version. You should always write 'Y'. This option is now deprecated (kept for legacy) and may be removed later.

### Update PDF files
While downloading portal article PDFs, some errors may occur. In these cases, the article information is in the database but its corresponding PDF file is not in the server. Thus, a script is provided to try to download again those files. 
To use this script, type `python update_pdf_files.py`. When executing this, a csv file called *nopdfarticles.csv* is generated and the script is halted with a *Press Enter to continue* message. Before you press enter, check the csv file and delete the candidate documents you are not interested. Then, go back to the script and press enter. It will try to download all candidate documents specified in the csv. If you have tried this more than 3 times and a candidate is not being downloaded, please contact the developer team.

Sometimes, an article PDF is too big to be downloaded with the current algorithm (E.g., when an article has many pages, such as portal document with id = 1281). When this happens, a memory error may arise because the RAM assigned to the script is not enough. To solve this problem, an *slow* option can be added to the script with the command `python update_pdf_files.py slow`. This *slow* mode saves some temporary files in the disk and then removes them. It is significantly slower than normal operation and is not set as the default mode
because it has been only needed on portal document 1281. Thus, if you see a MemoryError after using this script in its normal mode, try with this *slow* option.

### OCR updater
This tool provides an option to get the OCR info from some **candidate documents** pre-selected
by the user.
A file is needed to use this function. This must be a CSV file with the following characteristics:
   - The first row is not used (column names should be in the first row).
   - The first field from each row must be the candidate id number
   - Other fields after the id are allowed, but they will not be used

Record files (those with candidates, created after running generate_candidates.py) are a good example
of a document with the previous characteristics.

To use this function type `python ocr_updater.py` in the root folder. The script will prompt the user
to input the filename. This filename must be relative to the root folder, so if the file is
in Crawler/Records, the filename must be introduced as *Crawler/Records/the_name_of_the_file* (**with no extension**).

Only previously blank OCRs are updated.


## Contact
If you have any doubt or experience any problem, contact me (Brian Isaac - brian.k.isaac-medina@durham.ac.uk) 
