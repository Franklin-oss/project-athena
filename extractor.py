'''
Extractor Module
---------------------------------
Intended to read a given pdf file and return a dictionary of workbook questions
Note: Questions do NOT have to be extracted exactly as google only needs teh keywords
      to determine which question it is
'''

# Imports
import pdftotext as reader
import re 
import os

class InvalidPdfPathException(Exception):
    pass

class Extractor:
    """Extractor object that contains functions to extract questions from pdf
    """
    def __init__(self, inpdf_path: str, page_range: tuple) -> None:
        """Initialize Extractor object

        Args:
            inpdf_path (str): path to workbook pdf

            page_range (tuple): page number range to solve. Eg: (10, 30) extracts questions found in pages 10 - 30.
        """
        # Check if path is a valid file
        assert os.path.isfile(inpdf_path), InvalidPdfPathException(f'{inpdf_path} is not a valid file path')

        self.inpdf_path = inpdf_path
        self.pg_range = page_range
        self.raw = self.get_raw_text()


    def get_raw_text(self):
        """Get file from path and extract raw text from pdf in the given page range
        """

        # Get file from path
        with open(self.inpdf_path, 'rb') as file:
            pdf = reader.PDF(file)  # get pdf object

        # Iterate through every page in range and add their raw text to pages string
        pages = ''
        for page in range(self.pg_range[0], self.pg_range[1] + 1):  # + 1 cuz range does not include the ending number
            pages += (pdf[page] + ' \n\n\n' )  # Add \n so pages don't stick together with no separation (important for regex model)
        
        return pages
    
    def extract_questions(self):
        """Function to extract questions from raw text input
        """
        
        assert self.raw is not None, "self.raw is None"  # Ensure get_raw_text has been run and self.raw is not empty
        question_split_regex = re.compile(r'\n[0-9][0-9]*.\s+')  # Compile regex to match question numbers at the beginning of every question
        splt = re.split(question_split_regex, self.raw)
        
        return splt[1:]  # Slice off first element cuz its the header
