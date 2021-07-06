
from os import environ, path
import modules.PortfolioInterface as PI
import robin_stocks.robinhood as rs

import re
import pandas as pd

class Robinhood(PI.PortfolioInterface):
    def __init__(self):
        self.access_info = None

    def login(self):
       self.access_info = rs.authentication.login(
           environ['rh_username'],
           environ['rh_pass'],
           expiresIn=86400,
           store_session=True,
           by_sms=True)

    def logout(self):
        rs.authentication.logout()

    def get_all_positions(self, output_dir):
        # make sure user is logged in and there is access token available
        if self.access_info and self.access_info['access_token']:
            # get all the stocks the user currently holds
            data = rs.account.get_all_positions()
            if data:
                # build a dataframe
                data = pd.DataFrame(data)

                # write to an output file for now for testing purposes
                self._write_to_output_file(data, 'all_positions', output_dir)

    def get_current_stocks_positions(self, output_dir):
        # make sure user is logged in and there is access token available
        if self.access_info and self.access_info['access_token']:
            # get all the stocks the user currently holds
            data = rs.account.build_holdings(with_dividends=True)
            if data:
                # build a dataframe
                data = pd.DataFrame(data)

                # write to an output file for now for testing purposes
                self.write_to_output_file(data, 'current_stocks_info', output_dir)


    def load_data_from_file(self, input_dir):
        # load current holding stocks
        current_stocks_data_file = path.join(input_dir, 'current_stocks_info.parquet')
        if path.exists(current_stocks_data_file):
            data = self.load_parquet_file(current_stocks_data_file)
            print(data.head())

        # load the all stocks data
        all_stocks_data_file = path.join(input_dir, 'all_positions.parquet')
        if path.exists(all_stocks_data_file):
            data = self.load_parquet_file(all_stocks_data_file)
            #print(data.head())
