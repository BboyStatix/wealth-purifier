import InterestScraperFactory

def extract_interest(statementType, statements):
  interestEntries = []
  Scraper = InterestScraperFactory.getScraper(statementType)
  for statement in statements:
    statementName = statement.filename
    statementData = statement.read()
    scraper = Scraper(statementName, statementData)
    entries = scraper.scrapeInterestEntries()
    interestEntries.extend(entries)
  return interestEntries