<h1 align="center"> PETRINET - GRAPHVIZ</h1>
<p align="center">
  <a href="https://github.com/facebook/react-native/blob/HEAD/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="React Native is released under the MIT license." />
  </a>
  <a href="https://reactnative.dev/docs/contributing">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome!" />
  </a>
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

## 🤔 About this app

## How to run this app
First, clone this repository and open a terminal inside the root folder.

Create and activate a new virtual environment (recommended) by running
the following:

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```
Run the app:

```bash
python app.py
```
Open a browser at http://127.0.0.1:5050

## 👌 Demo



https://user-images.githubusercontent.com/13111806/185759656-e7d96783-bd94-43e9-936d-024484b0c6f6.mp4



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

## How to embed user-tracking code into a website
Insert the following Javascript in a particular shared region of a web application
A copy of `tracking.js` is also saved in `user_tracking/tracking.js`.

```
<script src='https://raw.githack.com/aust-ase2/crawling/main/tracking.js'></script>
<script>const instance = new AutoCapture({  persistence: 'memory', capture: ['tap', 'form', 'page'], onEventCapture: (event) => { 

    console.log('Event stored', event)
    $.ajax({ url: 'http://localhost:6200/push_data/', method: 'POST', crossDomain: true, headers: {  'Access-Control-Allow-Origin': '*'}, data: event, type: 'json', success: function(jsondata){console.log('success!!') } })

    } })
 instance.start()

 </script>
```

## How to parse test case that you have recorded using Katalon Studio

### Step 1: Install `Groovy` 
To install Groovy, you can follow this tutorial: https://pvital.wordpress.com/2018/03/22/installing-groovy-on-mac-os/


### Step 2:
You must have project include all your test cases and auxiliary files (you can obtain using Katalon Studio) <br>
> Ex: /Users/user.name/Katalon Studio/name.of.your.project

<br>

### Step 2
Run the crawling process for parsing and crawling information of each place using:
```python
python place_crawler.py --project '/Users/user/Katalon Studio/Test' --url 'http://test.com' -tc 'test 1' -tc 'test 2'
```

with

```python
python place_crawler.py -h
usage: place_crawler.py [-h] [-p PROJECT] [-u URL] [-tc TESTCASE]

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                                Assign path of your project (record test case use Katalon).
                                    + ex: --project '/Users/user/Katalon Studio/Test'
                            
  -u URL, --url URL     
                                Specify URL of page you want to crawl. Otherwise it will use default URL of your test case.
                                    + Ex: --url 'helloworld.com'
                            
  -tc TESTCASE, --testcase TESTCASE
                        
                                Specify name of test cases you want to spare and crawl. Otherwise it will parse all test cases included in your project.
                                    + Ex: --testcase 'test 1' --testcase 'test 2'
```
