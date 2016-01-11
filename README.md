# Mint scripts

Development of Intuit's mint.com has stagnated for a while and the site still
lacks simple filtering tools. I haven't found a site that has Mint's
semi-automated transaction classification with better data analysis, so it
looks like the best I can do is analyze the data myself.

As an alternative, I had some luck uploading my transactions file directly
to Statwing.com.

## summarize_year.py

Log in to Mint and visit
`https://wwws.mint.com/transaction.event?startDate=01/01/2015&endDate=12/31/2015`
to get a year's worth of transactions. Click "Export all NNNN transactions" to
download a CSV file.

After you've downloaded your transactions, you can run:
```
python summarize_year.py transactions.csv
```
to get a quick visual summary of your spending. Some of the hardcoded
categories are based on my custom labels in Mint, so you might have to
edit them.
