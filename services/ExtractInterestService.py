import InterestScraperFactory

def extract_interest(statementType, statements):
  interestEntries = []
  Scraper = InterestScraperFactory.getScraper(statementType)
  sortedStatements = sorted(
    statements, 
    key=lambda statement: Scraper.statementSorter(statement.filename)
  )
  for statement in sortedStatements:
    statementName = statement.filename
    statementData = statement.read()
    scraper = Scraper(statementName, statementData)
    entries = scraper.scrapeInterestEntries()
    interestEntries.extend(entries)
  return interestEntries