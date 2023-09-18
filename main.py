import os
import csv
import InterestScraperFactory
from constants import SUPPORTED_BANK_STATEMENTS

def generateCSV(interestEntries, statementType):
  with open(f'./generated/{statementType}.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Interest"])
    for row in interestEntries:
      writer.writerow(row)

def askForStatementType():
  print("What type of bank statement? Pick an option:")
  for statementType in SUPPORTED_BANK_STATEMENTS:
    print(f'* {statementType}')
  inputMessage = 'Your choice: '
  statementType = input(inputMessage)
  while statementType not in SUPPORTED_BANK_STATEMENTS:
    print("Please try again: ")
    statementType = input(inputMessage)
  return statementType

def askForStatementDir():
  directory = input("Please input the directory of your bank statement files: ")
  return directory

# statementType = askForStatementType()
statementType = "hsbc_statement_savings"
# statementType = "hsbc_one"
# statementDir = askForStatementDir()
# statementDir = "./examples/HSBCOneStatements"
statementDir = "./examples/HSBCStatementSavingsStatements"
print("Calculating...")
statements = os.listdir(statementDir)
interestEntries = []
for statement in sorted(statements):
  statementPath = f'{statementDir}/{statement}'
  scraper = InterestScraperFactory.getScraper(statementType)(statement, statementPath)
  entries = scraper.scrapeInterestEntries()
  interestEntries.extend(entries)
generateCSV(interestEntries, statementType)
totalInterest = sum([entry[1] for entry in interestEntries])
print(f"Total Interest: {totalInterest}")