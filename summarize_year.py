import calendar
from collections import defaultdict
import copy
import csv
import datetime
import optparse
import sys

categories = [
    ['Air Travel'],
    ['Alcohol'],
    ['Books'],
    ['Clothing'],
    ['Coffee'],
    ['Entertainment', 'Concerts', 'Music', 'Museums', 'Arts'],
    ['Groceries'],
    ['Gym'],
    ['Paycheck'],
    ['Public Transportation'],
    ['Rental Car'],
    ['Fast Food'],
    ['Restaurants'],
    ['Groceries', 'Fast Food', 'Restaurants'],
    ['Rideshare', 'Taxi'],
    ['Shopping', 'Electronics', 'Sporting Goods'],
]

usage = 'python summarize_year.py [options] transactions_filename.csv'
parser = optparse.OptionParser(usage=usage)
parser.add_option('-s', '--spreadsheet', action='store_true',
    dest='spreadsheet',
    help='Whether to output in a more spreadsheet-friendly format')
options, args = parser.parse_args()
if len(args) == 0:
  print 'Error: must provide the name of the transactions file exported from Mint'
  sys.exit()

def parse_transaction_list():
  transactions = []
  with open(args[0]) as f:
    reader = csv.reader(f, delimiter=',')
    next(reader) # skip headers
    for row in reader:
      # parse dates in column 0 and amounts in column 3
      newrow = copy.deepcopy(row)
      parts = row[0].split('/')
      newrow[0] = datetime.date(int(parts[2]), int(parts[0]), int(parts[1]))
      newrow[3] = float(newrow[3])
      transactions.append(newrow)
  return transactions

def matches(transaction, words):
  for word in words:
    if word in transaction[5]:
      return True
  return False

def get_by_month_for_category(transactions, category_wordlist):
  # Month -> spend that month
  month_dict = defaultdict(float)
  for transaction in transactions:
    if matches(transaction, category_wordlist):
      month_dict[transaction[0].month] += transaction[3]
  for i in xrange(1, 13):
    if i not in month_dict:
      month_dict[i] = 0
  return month_dict

def print_month_dict(month_dict):
  if options.spreadsheet:
    for month, cost in month_dict.iteritems():
      print '%s;$%.02f' % (calendar.month_name[month][:3], cost)
  else:
    total = sum(month_dict.values())
    divisor = total / 100
    for month, cost in month_dict.iteritems():
      print '%s $%.02f\t%s' % (calendar.month_name[month][:3], cost,
          '#'*int(cost/divisor))
    print 'TOTAL: $%.02f' % (total,)

transactions = parse_transaction_list()
for category in categories:
  month_dict = get_by_month_for_category(transactions, category)
  print ', '.join(category)
  print_month_dict(month_dict)
  print
  print


credit = 0
debit = 0
for transaction in transactions:
  if transaction[4] == 'debit':
    debit += transaction[3]
  else:
    credit += transaction[3]
print 'Cashflow (includes transfers between accts, credit card payments, etc):'
print 'ALL CREDITS: $%.02f' % (credit, )
print 'ALL DEBITS: $%.02f' % (debit, )
