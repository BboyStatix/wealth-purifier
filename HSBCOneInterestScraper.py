import pdfplumber
import re

DATE_REGEX = "^[0-3]?[0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
INTEREST_REGEX = "CREDIT INTEREST"

def extractPDFContent(pdf):
  pdfContent = ""
  for page in pdf.pages:
    pdfContent += page.extract_text()
  return pdfContent

def getDateFromSentence(sentence):
  match = re.search(DATE_REGEX, sentence)
  if match is not None:
    date = match.group(0)
    return date
  

class HSBCOneInterestScraper:
  def __init__(self, statement, statementPath):
    self.statement = statement
    with pdfplumber.open(statementPath) as pdf:
      self.pdfContent = extractPDFContent(pdf)
  
  @staticmethod
  def sortStatements(statements):
    return sorted(statements)
  
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
    dateOfCurrentEntry = ""
    interestEntries = []
    for sentence in sentences:
      date = getDateFromSentence(sentence)
      if date: dateOfCurrentEntry = date
      if re.search("Foreign Currency Savings", sentence) is not None: isUSDSection = True

      if INTEREST_REGEX in sentence:
        interestAmount = self._getInterestAmount(sentence, isUSDSection)
        print(f"{dateOfCurrentEntry}: {interestAmount}")
        interestEntries.append([dateOfCurrentEntry, interestAmount])
    return interestEntries