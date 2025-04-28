## DRAINAGE DISCHARGE EVENT ANALYSIS

Catches *EVENTS* separating the event flow from base flow

 
## Instructions 

'''
pip install EVENT_PACKAGE - This allows you install the package in shells like anaconda and powershell
'''

There are two such categories to this package

a. You have the daily event data that can be called when the discharge data is in the daily data resolution 'from EVENT_PACKAGE import daily_event'

b. You have the hourly event data that can be called when the discharge data is in the hourly data resolution 'from EVENT_PACKAGE import hourly_event'

## DATA TYPES

This code would require that you input 2 datas

## DATA A - Discharge data
The discharge data should be saved in a txt file in a single column (i.e you can copy and paste the data column from excel)


## DATA B - DATES

The dates should also be put in a txt file like in the same manner as the discharge data. (single column of dates)

## Hourly

hourly data should be of the form mm/dd/yy hh   example: 10/03/2025 2:00 (for October 3rd 2025 second hour (2nd hour)))

Note the time resolution is in the 24 hours scale 0:00 - 23:00


## Daily

daily date should be in the form dd/mm/yy   example: 10/01/2023 (for 10th January 2023)


## file names

The files names should be

# Daily data

a. Daily_Dates.txt for the daily dates TXT file

b. event_data.txt for the daily drainage discharge TXT file

# hourly data

a. Hourly_Dates.txt for the hourly dates TXT file

b. hourly_event.py for the hourly drainage discharge TXT file

# Location of txt file

The txt files should be save in the external folder holding the code

## EXCUTE THE CODE

To excute the code you need to just call the module depending on what data you want to analyse

# Daily Event Analysis

from EVENT_PACKAGE import daily_event

# hourly Event Analysis

from EVENT_PACKAGE import hourly_event

## NOTES!!!!

1. MISSING DATA DOES NOT AFFECT THE PLOT SO DO NOT WORRY ABOUT CLEANING MISSING DATA