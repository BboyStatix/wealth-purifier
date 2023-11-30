import pdfplumber
import re
from datetime import datetime
import io

DATE_REGEX = {
  "website": r"^[0-3]?[0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
  "app": r"^[0-3]?[0-9](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
}
INTEREST_REGEX_OLD = "CREDIT INTEREST"
INTEREST_REGEX_NEW = "CREDITINTEREST"
INTEREST_REGEX = r"({})|({})".format(INTEREST_REGEX_NEW, INTEREST_REGEX_OLD)

STATEMENT_PREFIX_REGEX =  {
  "website": r"^([0-9]{4})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])", # 2021-06-05_Statement
  "app": r"^eStatementFile_([0-9]{4})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1]).*" # eStatementFile_20231114192229
}

def extractPDFContent(pdf):
  pdfContent = ""
  for page in pdf.pages:
    pdfContent += page.extract_text()
  return pdfContent

def getDateFromSentence(sentence):
  match = re.search(DATE_REGEX['website'], sentence)
  if match is not None:
    dateStr = match.group(0)
    return datetime.strptime(dateStr, "%d %b")
  
  match = re.search(DATE_REGEX['app'], sentence)
  if match is not None:
    dateStr = match.group(0)
    return datetime.strptime(dateStr, "%d%b")

def getDateFromStatementFilename(statement):
  match = re.search(STATEMENT_PREFIX_REGEX["website"], statement)
  if match is not None:
    return datetime.strptime(statement.split('_')[0], "%Y-%m-%d")
  
  match = re.search(STATEMENT_PREFIX_REGEX["app"], statement)
  if match is not None:
    return datetime.strptime(statement.split('_')[1][0:8], "%Y%m%d")
  
  raise Exception("Unsupported statement type!")

class HSBCOneInterestScraper:
  def __init__(self, statement, statementData):
    self.statementDate = getDateFromStatementFilename(statement)
    with pdfplumber.open(io.BytesIO(statementData)) as pdf:
      self.pdfContent = extractPDFContent(pdf)

  def _getFullDateOfCurrentEntry(self, date):
    isJanuaryStatement = self.statementDate.month == 1
    isDecemberEntry = date.month == 12
    yearOfEntry = self.statementDate.year
    # if we have a January statement, the december entries inside should be currentStatement year - 1
    if isJanuaryStatement and isDecemberEntry:
      yearOfEntry = yearOfEntry - 1
    return f"{date.strftime('%d %b')} {yearOfEntry}"
  
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
    # e.g '28Oct CREDITINTEREST 28.08 20,932.88'
    # e.g '28 Jan CREDIT INTEREST 35.48'
    pattern = r'(?:{}|{})\s+(\d+(?:\.\d+)?)'.format(INTEREST_REGEX_OLD, INTEREST_REGEX_NEW)
    match = re.search(pattern, sentence)
    if match is None: raise Exception("Unsupported file type")

    amount = float(match.group(1))
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
      if re.search(INTEREST_REGEX, sentence) is not None:
        fullDate = self._getFullDateOfCurrentEntry(dateOfCurrentEntry)
        interestAmount = self._getInterestAmount(sentence, isUSDSection)
        print(f"{fullDate}: {interestAmount}")
        interestEntries.append([fullDate, interestAmount])
    return interestEntries