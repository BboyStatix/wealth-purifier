from scrapers.HSBCOneInterestScraper import HSBCOneInterestScraper
from scrapers.MoxInterestScraper import MoxInterestScraper
from scrapers.HSBCStatementSavingsScraper import HSBCStatementSavingsScraper

def getScraper(bankType):
  if bankType == "hsbc_one":
    return HSBCOneInterestScraper
  elif bankType == "mox":
    return MoxInterestScraper 
  elif bankType == "hsbc_statement_savings":
    return HSBCStatementSavingsScraper 
  else:
    raise Exception("Bank type: " + bankType + " is currently not supported")