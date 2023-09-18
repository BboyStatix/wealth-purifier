from HSBCOneInterestScraper import HSBCOneInterestScraper
from MoxInterestScraper import MoxInterestScraper
from HSBCStatementSavingsScraper import HSBCStatementSavingsScraper

def getScraper(bankType):
  match bankType:
    case "hsbc_one":
      return HSBCOneInterestScraper
    case "mox":
      return MoxInterestScraper
    case "hsbc_statement_savings":
      return HSBCStatementSavingsScraper
    case _:
      raise Exception("Bank type: " + bankType + " is currently not supported")