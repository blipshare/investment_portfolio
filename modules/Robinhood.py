
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import tabula
import modules.PortfolioInterface as PI
import modules.Robinhood as RH

import re

class Robinhood(PI.PortfolioInterface):
    def __init__(self):
        self._build_keys()

    def load_pdf(self, pdf_file):
        print('Robinhood: loading pdf file ...')
         
        for page_layout in extract_pages(pdf_file):
            self.curr_key = None

            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    self.extract_text(element)

        print(self.summary)

    def _build_keys(self):
        """ Keys that are interesting for processing """
        self.summary = {
            'Net Account Balance': [],
            'Total Securities': [],
            'Portfolio Value': [],
            'Dividends': [],
            'Capital Gains Distributions': [],
            'Interest Earned': []
        }


    def extract_text(self, element):
        for text_line in element:
            text_line = text_line.get_text().strip()

            # check to see which of the following cases we need to parse
            # 1. Ex:
            #       Total Securities
            #       Portfolio Summary
            #       Open $ value  (For Total Securities)
            #       Close $ value (For Total Securities)
            #       Open $ value  (For Portfolio Summary)
            #       Close $ value (For Portfolio Summary)
            #
            # 2. Ex:
            #       Total Securities
            #       Open $ value  (For Total Securities)
            #       Close $ value (For Total Securities)
            #       Portfolio Summary
            #       Open $ value  (For Portfolio Summary)
            #       Close $ value (For Portfolio Summary)
            print(text_line)
            if self.curr_key and self.num_read_lines == 0:
                # if this line contains text, it is case 1. Else it is case 2
                if len(re.findall('[a-zA-Z ]+', text_line)) > 0:
                    self._parse_account_summary(text_line)
                else:
                    self._parse_account_summary_normal(text_line)
            else:
                self._parse_account_summary_normal(text_line)
            #self._parse_portfolio_summary(element)


    """
    Parse the Account Summary page of the Robinhood Statement
    """
    def _parse_account_summary(self, text_line):
        # check to see if the text read is 'Net Account Balance'
        # if yes, the next two lines will be its closing and opening values
        if 'Net Account Balance' in text_line:
            self.curr_key = 'Net Account Balance'
            self.next_num_lines_to_read = 2
            self.num_read_lines = 0

        # check to see if the text read is 'Portfolio Value'
        # if yes, the next two lines will be its Total Security and the 
        # following two lines after that will be Portfolio Value
        elif 'Portfolio Value' in text_line:
            self.curr_key = 'Total Securities'
            self.next_num_lines_to_read = 4
            self.num_read_lines = 0
 
        # check to see if the text read is 'Income and Expenses Summary'
        # if yes, the next two lines will be Dividends, the 
        # following two lines after that will be Capital Gains Distributions
        # and the last two lines  will be Interest Earned
        elif 'Interest Earned' in text_line:
            self.curr_key = 'Dividends'
            self.next_num_lines_to_read = 6
            self.num_read_lines = 0
        
        elif self.curr_key:
            if self.num_read_lines >= self.next_num_lines_to_read:
                self._reset()
            else:
                if 'Total Securities' in self.curr_key and self.num_read_lines >= 2:
                    self.curr_key = 'Portfolio Value'
                elif 'Dividends' in self.curr_key and self.num_read_lines >= 2:
                    self.curr_key = 'Capital Gains Distributions'
                elif 'Capital Gains Distributions' in self.curr_key and self.num_read_lines >= 4:
                    self.curr_key = 'Interest Earned'

                # make sure we are adding dollar values only
                if len(re.findall('[$0-9]+', text_line)) > 0:
                    self.summary[self.curr_key].append(text_line)
                    self.num_read_lines += 1

    def _parse_account_summary_normal(self, text_line):
        if text_line in self.summary:
            self.curr_key = text_line
            self.next_num_lines_to_read = 2
            self.num_read_lines = 0
        elif self.curr_key:
            self.summary[self.curr_key].append(text_line)
            self.num_read_lines += 1
            if self.num_read_lines >= self.next_num_lines_to_read:
                self._reset()


    """
    Parse the Portfolio Summary of the Robinhood Statement
    """
    def _parse_portfolio_summary(self, element): 
        #print(element)
        pass

    def _reset(self):
        self.curr_key = None
        self.next_num_lines_to_read = 0
        self.num_read_lines = 0
