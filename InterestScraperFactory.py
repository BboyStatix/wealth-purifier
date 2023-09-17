from HSBCOneInterestScraper import HSBCOneInterestScraper

def getScraper(bankType):
  match bankType:
    case "hsbc_one":
      return HSBCOneInterestScraper
    case _:
      raise Exception("Bank type: " + bankType + " is currently not supported")