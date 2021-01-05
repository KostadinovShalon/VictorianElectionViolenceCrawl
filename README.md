# Victorian Election Violence Crawler 2
The aim of this project is to crawl news from [British Newspaper Archive](https://www.britishnewspaperarchive.co.uk/).

## Version
The current version of the project is **2.1.5**. The change history can be seen in the [Change Log](/changelog.md)

## Requirements

 **Linux**
 - Python 3
 - npm
 
 **Windows**
 - Anaconda or Miniconda 3
 - npm (installed through node.js)

## Linux

### Installation

**Backend**

1. Create a virtual environment on the project folder 

    ``python3 -m venv venv``

1. Activate the environment 

    `source ./venv/bin/activate`

1. Install the crawler 

    `pip install vev_crawler-2.1.5-py3-none-any.whl`

1. **NEW since version 2.1.2** Create configuration database

	`export FLASK_APP=application`
	
	`flask init-db`


**Frontend**

1. Install serve

    `npm install -g serve`


<a href="http://www.youtube.com/watch?feature=player_embedded&v=F0FTwul4Hdw
" target="_blank"><img src="http://img.youtube.com/vi/F0FTwul4Hdw/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

### Starting the servers

**Backend**

1. Start the backend server

    `waitress-serve --call --port 5000 'application:create_app'`

1. To keep the backend running, keep the terminal open.

**Frontend**


1. In the project folder, run the frontend server

    `serve -s ui -p 8080`

1. Navigate to [http://localhost:8080](http://localhost:8080)

1. To keep the frontend running, keep the terminal open.


## Windows

### Basic Installation (Recommended)

**Backend**

1. Open Anaconda prompt

1. Navigate to the project folder

	`cd C:\Users\path\to\the\project\folder`

1. In the anaconda prompt, run the installation file (*more details about what the installation file is doing in the Advanced Installation Section*)
	
	`windows_install.bat`


**Frontend**

1. Open a command prompt (not PowerShell) and install serve

    `npm install -g serve`

### Starting the servers

**Backend**
1. Open Anaconda prompt

1. Navigate to the project folder

	`cd C:\Users\path\to\the\project\folder`

1. In the anaconda prompt, run the backend server script
	`start_backend_server.bat`

**Frontend**
1. Double click `start_frontend_server.bat`


### Advanced Installation

**Backend**

1. Open Anaconda prompt

1. Create a virtual environment 

    ``conda create -n vevcrawler``

1. Activate the environment 

    `conda activate vevcrawler`

1. On the Anaconda prompt, navigate to the project folder and install the following packages

    `conda install -y Twisted`
    
    `pip install vev_crawler-2.1.5-py3-none-any.whl`
    
    `conda install numpy`

1. Initialize the database

	`set FLASK_APP=application`
	
	`flask init-db`

**Frontend** (same process as the basic installation)

1. Open a command prompt (not PowerShell) and install serve

    `npm install -g serve`

### Advanced start of servers
**Backend**
1. Open Anaconda prompt

1. Activate the enviroment created during installation

	`conda activate vevcrawler`

1. Run the following command

	`waitress-serve --call --port 5000 "application:create_app"`

**Frontend**
1. Open a command prompt (not PowerShell)

1. Navigate to the project folder

	`cd C:\Users\path\to\the\project\folder`

1. Run the following command

	`serve -s ui -p 8080`


## Usage
<a href="http://www.youtube.com/watch?feature=player_embedded&v=dyWr_ATT1lw
" target="_blank"><img src="http://img.youtube.com/vi/dyWr_ATT1lw/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

## Contact
If you have any doubt or experience any problem, contact me (Brian Isaac - brian.k.isaac-medina@durham.ac.uk) 
