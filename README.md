# TwitterDataAnalyser
[![Generic badge](https://img.shields.io/badge/version-3.09.10-<COLOR>.svg)](https://shields.io/)
[![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Generic badge](https://img.shields.io/badge/contributors-2-blue)](https://shields.io/)  
[![forthebadge made-with-python](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  	

# About
A Twitter Data Analyzer that fecths user posts and posts comments to do some analysis like Sentiment Analysis and Data Vizualisation

This is project aims to analyze Twitter data such as posts and posts replies, it show things like most common words used in replies to an user, most mentioned organizations, data sentiment analysis, compare users data.

# How to start
It is necessary to mention that the program is written in Python, under versions greater than or equal to Python 3.6, so it is advisable to update your computer to the most recent Python version, otherwise some failures could occur, and in the same way We recommend running on computers with GNU LINUX Operating System in any of its versions.
It is also necessary to install some extra libraries.

## Requerimients
* Check to use a version higher than Python3.6:
```
python --version
```
> `Python 3.6 +` is adviced

  Note, on some Linux distros, you will run it like:
  ```
  python3 --version
  ```


* You can check if you have PyPI installed as well as Python
  Available in the following article
  [PyPI] (https://www.tecmint.com/install-pip-in-linux/) up.

* Have installed pip "Pip Installs Packages" to install the necessary libraries

## Installation

* First of all you must install all the libraries that are needed for the program to run, for this just run the following command


```
pip install -r requirements.txt
```

# Use
* Usually you will run like this

If you want just do the data analysis for one user
```
python3 MainHanddler.py cp <user> <start_date> <end_date>
```
In case you want to compare two users
```
python3 MainHanddler.py cp <user1> <user2> <start_date> <end_date>
```

The dates have to follow this format:
```
YY-MM-DD
```
* But at the moment you can run't directly using the MainHanddle.py file, because there when you try to run it, it raises a problem with the date formats.

* But using it doing all the process that MainHanddler.py is supposed to do on a Jupyter Notebook works perfectly fine.
* That's why in DEMO.ipynb you can look at how you can use this repository.

* But we're still looking how to fix the Date format issue.

# What is next?
* This is just a start, we're thinking about new ideas about how to get and analyse usefull data to work with and perform a great job.

* Any ideas are welcomed, just send me an email and I will be glad to read it and discuss about it!





# Developed by:
#### David Hernández Urióstegui

[<img src="https://img.shields.io/badge/gmail-D14836?&style=for-the-badge&logo=gmail&logoColor=white"/>](https://mail.google.com/mail/?view=cm&source=mailto&to=Dhdezu@ciencias.unam.mx)





---
![forthebadge biult-with-love](https://forthebadge.com/images/badges/built-with-love.svg) 
[![forthebadge powered-by-electricity](https://forthebadge.com/images/badges/powered-by-electricity.svg)](http://ForTheBadge.com)  
