"""
Basic Browser Handle
-------------------------------------
Module to open a window of chrome with tabs of google searches for questions that it takes in as input.
Note: This is meant to be a temporary fix to be a placeholder until the module for extracting answers from diff educational websites is completed.
      Can also be used as fallback solution for upcoming update incase no recognized website has the question  
"""
# Imports
import time
import chromedriver_autoinstaller
from selenium import webdriver
from googlesearch import search


sitelist = ['brainly.in', 'sarthaks.com', 'doubtnut.com']  # List of recognized websites to extract answer from. Toppr.com has been removed due to cloudflare protection


class browser_handle:
    """Object to take in list of questions and open browser pages for them.
       TODO: Make it capable of scraping answers from websites.
    """
    def __init__(self, qlist, open_direct=False):
        
        self.qlist = qlist
        self.url_dct = {}
        for q in qlist:
            key, value = browser_handle.get_answer_url(q, open_direct=open_direct)  # ALWAYS FALLBACK SET TO TRUE UNTIL GOOGLE MODULE CAN WORK WITHOUT HTTP 429 ERROR
            self.url_dct[key] = value

    
    @staticmethod
    def get_answer_url(question, open_direct=False):
        """
        Function to generate the url for a given question. It checks Google search results and
        if it finds a recognized website (see sitelist), it returns the url for that result else, 
        returns Google search page url for the question.

        Args:
            question ([str]): question which has to be solved
            open_direct (bool, optional): Option to always return Google search result page for
                                              the question. To be used for debugging to bypass google search query.
                                              Defaults to False.

        Returns:
            str: returns url to be opened by browser or to be scraped (in later versions).
        """       
        matches = []
        if open_direct:
            time.sleep(3)
            for result_url in search(question, num=10, pause=2.0, stop=10):
                for site in sitelist:  # Go through list of recognized websites and append them to matches if any of search result urls match
                    if result_url.find(site) != -1:  # If match is found anywhere in string
                        matches.append(result_url)
        
        if len(matches) == 0:
            matches.append(f'https://www.google.com/search?q={question}')  # Fallback to google search page url incase no matches are found or query is bypassed by option

        return question, matches  # Return tuple of question and matches

    def open_tabs(self):
        """
        Opens browser tabs for a given dictionary of urls. Placeholder for until scraping module is built (in later versions).
        """
        chromedriver_autoinstaller.install()  # Install chromedriver if it is not installed 

        assert len(self.url_dct) != 0, 'url_dct is empty. Try running for loop'  # Make sure url_dct has inside it
        
        options = webdriver.ChromeOptions()  # Initialize options object
        options.add_experimental_option("detach", True)  # Option to make sure browser window stays open after script has run
        # driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=options)  # Initialize driver
        driver = webdriver.Chrome(options=options)  # Initialize driver

        window_number = 1  # Keep track of which window to have focus on
        for key in self.url_dct.keys():
            driver.get(self.url_dct[key][0])  # Open the answer url in the tab
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[window_number]) # Switch focus to latest window
            window_number += 1


if __name__ == '__main__':
    def test():
        """
        Basic test with a question list of 2 basic questions.
        """
        browser_handle(['What is the time', 'Where am I']).open_tabs()

    test()
