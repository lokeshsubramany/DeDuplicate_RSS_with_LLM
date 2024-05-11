from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

def get_feed_article_titles_df(feedname,url):
    """
    Get article titles and create a DataFrame.
    
    Args:
        feedname (str): Name of the feed.
        url (str): URL of the XML feed.
    
    Returns:
        pandas.DataFrame: DataFrame containing article titles and feed name.
    """
    try:
        result = requests.get(url, headers=headers)

        soup = BeautifulSoup(result.text, "xml")        
        article_urls = [i.text for i in soup.findAll('link')]

        #The verge has the links in the id tag, if the list is empty with the link tag, try the id tag
        if len([item for item in article_urls if bool(item)])  == 0: 
            article_urls = [i.text for i in soup.findAll('id')]      
        
       
        #Parse it as html to get the links correctly, other wise In some websites, <media:title> is also returned as a link
        soup = BeautifulSoup(result.text, "html.parser")
        article_titles = [i.text for i in soup.findAll('title')]      
        
        df = pd.DataFrame({'Article_title': article_titles, 'Article_URL': article_urls[-len(article_titles):], 'Feedname': feedname})
        
        #Remove homepage from url list and empty url rows
        homepage = url.split('.com')[0] + '.com/'
        df = df[(df['Article_URL'] != homepage) & (df['Article_URL'] != '') ]        
        
        # Drop duplicate URLs
        df = df.drop_duplicates(subset=['Article_URL'], keep='first')

        df['Fetch_Date'] = str(datetime.datetime.now())

        return df

    except Exception as e:
        print("Error getting feed: ", e)
        return pd.DataFrame()

def get_article_text(url):
    try:
        result = requests.get(url[0][0], headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")   
        return (soup.text)     
    except Exception as e:        
        try:
            result = requests.get(url[0], headers=headers)
            soup = BeautifulSoup(result.text, "html.parser")   
            return (soup.text)    
        except Exception as e:
            try:
                result = requests.get(url, headers=headers)
                soup = BeautifulSoup(result.text, "html.parser")   
                return (soup.text)    
            except Exception as e:
                print(e)
                return None
