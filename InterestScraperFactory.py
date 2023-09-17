from HSBCOneInterestScraper import HSBCOneInterestScraper
from MoxInterestScraper import MoxInterestScraper

def getScraper(bankType):
  match bankType:
    case "hsbc_one":
      return HSBCOneInterestScraper
    case "mox":
      return MoxInterestScraper
    case _:
      raise Exception("Bank type: " + bankType + " is currently not supported")