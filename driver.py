
from os import path

import modules.Robinhood as RH

def process(output_dir):
    rh = RH.Robinhood()
    rh.login()
    rh.get_all_positions(output_dir)
    rh.get_current_stocks_positions(output_dir)
    rh.logout()

def process_data(input_dir):
    rh = RH.Robinhood()
    rh.load_data_from_file(input_dir)

