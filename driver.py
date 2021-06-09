
from os import path
import PyPDF4

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

import modules.Robinhood as RH

def process(pdf_file):
	rh = RH.Robinhood()
	rh.load_pdf(pdf_file)
