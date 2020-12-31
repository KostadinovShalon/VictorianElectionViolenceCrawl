# Victorian Election Violence Crawler 2.0.5
The aim of this project is to crawl news from [British Newspaper Archive](https://www.britishnewspaperarchive.co.uk/) and [Welsh Newspapers Online](http://newspapers.library.wales/) sites.

## Version
The current version of the project is **2.0.5**. The change history can be seen in the [Change Log](/changelog.md)

## Requirements

 **Linux**
 - Python 3
 - npm
 
 **Windows**
 - Anaconda or Miniconda 3
 - npm (installed through node.js)

## Installation

### Linux

**Backend**

1. Create a virtual environment on the project folder 

    ``python3 -m venv venv``

1. Activate the environment 

    `source ./venv/bin/activate`

1. **IMPORTANT** (I forgot to mention this on the video): install mysqlclient
    
    `pip install mysqlclient`

1. Install the crawler 

    `pip install vev_crawler-2.0.5-py3-none-any.whl`

1. Start the backend server

    `waitress-serve --call --port 5000 'application:create_app'`

1. To keep the backend running, keep the terminal open. If you close the terminal, repeat steps
2 and 5 to start it again.

**Frontend**

1. Install serve

    `npm install -g serve`

1. In the project folder, run the frontend server

    `serve -s ui -p 8080`

1. Navigate to [http://localhost:8080](http://localhost:8080)

1. To keep the frontend running, keep the terminal open. If you close the terminal, repeat step 2.


<a href="http://www.youtube.com/watch?feature=player_embedded&v=F0FTwul4Hdw
" target="_blank"><img src="http://img.youtube.com/vi/F0FTwul4Hdw/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

### Backend 

#### 0. Create and activate virtual environment

Run the command `python3 -m venv venv` to install a virtual environment in this folder. 

To activate the environment:

On Windows: `.\venv\Scripts\activate`
On Linux: `source ./venv/bin/activate`

The environment will be installed if you see a "(venv)" at the beginning of the command prompt

#### 1. Install the backend

Run the command `pip install vev_crawler-2.0.5-py3-none-any.whl`

## Contact
If you have any doubt or experience any problem, contact me (Brian Isaac - brian.k.isaac-medina@durham.ac.uk) 
