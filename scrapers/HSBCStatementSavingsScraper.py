import pdfplumber
import re
from datetime import datetime
import io

DATE_REGEX = r"^[0-3]?[0-9]-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
INTEREST_REGEX = "CREDITINTEREST"

def extractPDFContent(pdf):
  pdfContent = ""
  for page in pdf.pages:
    pdfContent += page.extract_text()
  return pdfContent

def getDateFromSentence(sentence):
  match = re.search(DATE_REGEX, sentence)
  if match is not None:
    dateStr = match.group(0)
    return datetime.strptime(dateStr, "%d-%b")
  
class HSBCStatementSavingsScraper:
  def __init__(self, statement, statementData):
    self.statement = statement
    with pdfplumber.open(io.BytesIO(statementData)) as pdf:
      self.pdfContent = extractPDFContent(pdf)
  
  def _getFullDateOfCurrentEntry(self, date):
    isJanuaryStatement = self._getStatementDate().month == 1
    isDecemberEntry = date.month == 12
    yearOfEntry = self._getStatementDate().year
    # if we have a January statement, the december entries inside should be currentStatement year - 1
    if isJanuaryStatement and isDecemberEntry:
      yearOfEntry = yearOfEntry - 1
    return f"{date.strftime('%d %b')} {yearOfEntry}"
  
  def _getPdfSentences(self):
    return self.pdfContent.split("\n")
  
  def _getStatementDate(self):
    return datetime.strptime(self.statement.split('_')[0], "%Y-%m-%d")
  
  def _getInterestAmount(self, sentence):
    (_, remainStr) = sentence.split(f"{INTEREST_REGEX} ")
    return float(remainStr.split(" ")[0])

  def scrapeInterestEntries(self):
    sentences = self._getPdfSentences()
    interestEntries = []
    dateOfCurrentEntry = ""
    for sentence in sentences:
      date = getDateFromSentence(sentence)
      if date: dateOfCurrentEntry = date
      if INTEREST_REGEX in sentence:
        fullDate = self._getFullDateOfCurrentEntry(dateOfCurrentEntry)
        interestAmount = self._getInterestAmount(sentence)
        print(f"{fullDate}: {interestAmount}")
        interestEntries.append([fullDate, interestAmount])
    return interestEntries