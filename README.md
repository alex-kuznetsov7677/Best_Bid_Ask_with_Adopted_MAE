
# Trading_strategy

This project implements a trading strategy based on tick data on best-bid and best-ask. The strategy is based on an algorithm for calculating the exponential moving average (EMA) with a variable averaging window.

## Project structure  
- strategy.py — the trading algorithm accepts data_example.csv as input and creates trade_results.csv with the results.  
- visualization.py — builds charts based on trade_results.csv, helping to analyze the strategy.  
- data_example.csv is an example of input data (price tick best_bid and best_ask).  
- trade_results.csv file with the results of the strategy (generated automatically).  
- README.md — this file contains instructions on how to use the project.  

## Installation and launch  
### 1. Installing dependencies  

To work with this code, you will need to install the pandas and matplotlib libraries. You can do this using the pip package manager.

If you do not have these libraries installed yet, run the following commands in the terminal:

pip install pandas matplotlib

###2. Launching a trading strategy
Start it up first strategy.py , which will process data.csv and create trade_results.csv:

python strategy.py

### 3. Visualization of results
After the strategy is working, you can build graphs by running visualization.py:

python visualization.py

## Requirements

Python
Pandas
Matplotlib

## TODO

Optimization of parameters

Adding regression methods to the algorithm

## Contacts

Email:a.kuznetsov7677@gmail.com

Github:alex-kuznetsov7677
