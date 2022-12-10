# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 00:03:15 2022

@author: nazne
"""

import scrapy
from scrapy import FormRequest
import pandas as pd
from datetime import datetime, timedelta
import os

class PricesSpider(scrapy.Spider):
    name = "prices"
    #https://fcainfoweb.nic.in/reports/report_menu_web.aspx
    # start_urls = ["https://fcainfoweb.nic.in/reports/report_menu_web.aspx", "https://fcainfoweb.nic.in/reports/report_menu_web.aspx", "https://fcainfoweb.nic.in/reports/report_menu_web.aspx", "https://fcainfoweb.nic.in/reports/report_menu_web.aspx"]

    def start_requests(self):
        
        datelist = []
        startDate = datetime.strptime("01/02/2020", "%d/%m/%Y")
        endDate = datetime.strptime("30/04/2020", "%d/%m/%Y")
        delta = endDate - startDate
        for i in range(delta.days +1):
            newDate = (startDate + timedelta(i)).strftime("%d/%m/%Y")
            datelist.append(newDate)
 
        for idx, el in enumerate(datelist):
            print(el)
            yield scrapy.Request("https://fcainfoweb.nic.in/reports/report_menu_web.aspx", self.parse, cb_kwargs={'date1':el}, dont_filter=True)
        # yield scrapy.Request("https://fcainfoweb.nic.in/reports/report_menu_web.aspx?a=1", self.parse, cb_kwargs={'date1':datelist[0]})
        # yield scrapy.Request("https://fcainfoweb.nic.in/reports/report_menu_web.aspx", self.parse, cb_kwargs={'date1':datelist[1]})

    def parse(self, response, date1):
        data = {
            "ctl00_MainContent_ToolkitScriptManager1_HiddenField": "",
            "ctl00$MainContent$Ddl_Rpt_type": "Retail",
            "ctl00$MainContent$ddl_Language": "English",
            "ctl00$MainContent$Rbl_Rpt_type": "Price report",
        }
        print(date1)
        yield FormRequest.from_response(
            response, formdata=data, callback=self.parse_prices_one, cb_kwargs={"date1":date1}, dont_filter=True
        )

    def parse_prices_one(self, response, date1):
        print("one")
        print(date1)
        data = {
            "ctl00_MainContent_ToolkitScriptManager1_HiddenField": "",
            "ctl00$MainContent$Ddl_Rpt_type": "Retail",
            "ctl00$MainContent$ddl_Language": "English",
            "ctl00$MainContent$Rbl_Rpt_type": "Price report",
            "ctl00$MainContent$Ddl_Rpt_Option0": "Daily Prices",
        }
        yield FormRequest.from_response(
            response, formdata=data, callback=self.parse_prices_two, cb_kwargs={"date1":date1}, dont_filter=True
        )
    def parse_prices_two(self, response, date1):
        # datalist = []
        print("two")
        data = {
            "ctl00_MainContent_ToolkitScriptManager1_HiddenField": "",
            "ctl00$MainContent$Ddl_Rpt_type": "Retail",
            "ctl00$MainContent$ddl_Language": "English",
            "ctl00$MainContent$Rbl_Rpt_type": "Price report",
            "ctl00$MainContent$Ddl_Rpt_Option0": "Daily Prices",
            "ctl00$MainContent$Txt_FrmDate": date1,
            "ctl00$MainContent$btn_getdata1": "Get Data",
        }

        print(date1)
        yield FormRequest.from_response(
            response, formdata=data, callback=self.parse_prices, cb_kwargs={"date1":date1}, dont_filter=True
        )
    def parse_prices(self, response, date1):
        print('here')
        df = pd.read_html(response.text)[1]
        print(os.getcwd())
        
        df.to_csv("./data_" + "_".join(date1.split('/')) + ".csv")
        print("done"+date1)
  
