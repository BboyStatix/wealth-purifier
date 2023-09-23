import pdfplumber
import re
from datetime import datetime

DATE_REGEX = r"^[0-3]?[0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
INTEREST_REGEX = "CREDIT INTEREST"

def extractPDFContent(pdf):
  pdfContent = ""
  for page in pdf.pages:
    pdfContent += page.extract_text()
  return pdfContent

def getDateFromSentence(sentence):
  match = re.search(DATE_REGEX, sentence)
  if match is not None:
    dateStr = match.group(0)
    return datetime.strptime(dateStr, "%d %b")
  

class HSBCOneInterestScraper:
  def __init__(self, statement, statementPath):
    self.statement = statement
    with pdfplumber.open(statementPath) as pdf:
      self.pdfContent = extractPDFContent(pdf)
  
  @staticmethod
  def sortStatements(statements):
    return sorted(statements)

  def _getFullDateOfCurrentEntry(self, date):
    isJanuaryStatement = self._getStatementDate().month == 1
    isDecemberEntry = date.month == 12
    yearOfEntry = self._getStatementDate().year
    # if we have a January statement, the december entries inside should be currentStatement year - 1
    if isJanuaryStatement and isDecemberEntry:
      yearOfEntry = yearOfEntry - 1
    return f"{date.strftime('%d %b')} {yearOfEntry}"

  def _getStatementDate(self):
    return datetime.strptime(self.statement.split('_')[0], "%Y-%m-%d")
  
  def _getPdfSentences(self):
    return self.pdfContent.split("\n")
  
  def _getUSDExchangeRate(self):
    sentences = self._getPdfSentences()
    for sentence in sentences:
      captureString = "FCYSavings USD "
      if re.search(captureString, sentence) is not None:
        return float(sentence.split(captureString)[1].split(" ")[0])
    raise Exception("No USD Exchange Rate found on PDF")

  def _getInterestAmount(self, sentence, isUSD):
    (_, remainStr) = sentence.split(f"{INTEREST_REGEX} ")
    amount = float(remainStr.split(" ")[0])
    if isUSD:
      return amount * self._getUSDExchangeRate()
    else:
      return amount

  def scrapeInterestEntries(self):
    sentences = self._getPdfSentences()
    isUSDSection = False
    interestEntries = []
    dateOfCurrentEntry = ""
    for sentence in sentences:
      date = getDateFromSentence(sentence)
      if date: dateOfCurrentEntry = date
      if re.search("Foreign Currency Savings", sentence) is not None: isUSDSection = True
      if INTEREST_REGEX in sentence:
        fullDate = self._getFullDateOfCurrentEntry(dateOfCurrentEntry)
        interestAmount = self._getInterestAmount(sentence, isUSDSection)
        print(f"{fullDate}: {interestAmount}")
        interestEntries.append([dateOfCurrentEntry, interestAmount])
    return interestEntries