import pdfplumber
import re
from datetime import datetime
import io

DATE_REGEX = r"^[0-3]?[0-9] (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
INTEREST_REGEX = r"^.*Interest 利息 \+"
STATEMENT_YEAR_REGEX = r"\d{4}"

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

def extractDate(statement):
  match = re.search(r'[A-Za-z]{3}(\d{4})', statement)
  if match:
    return datetime.strptime(match.group(0), '%b%Y')
  else:
      return 0
  
class MoxInterestScraper:
  def __init__(self, statement, statementData):
    self.statement = statement
    with pdfplumber.open(io.BytesIO(statementData)) as pdf:
      self.pdfContent = extractPDFContent(pdf)

  def _getPdfSentences(self):
    return self.pdfContent.split("\n")

  def _getStatementYear(self):
    match = re.search(STATEMENT_YEAR_REGEX, self.statement)
    if match:
      return match.group(0)

  def scrapeInterestEntries(self):
    sentences = self._getPdfSentences()
    interestEntries = []
    statementYear = self._getStatementYear() 
    for sentence in sentences:
      isInterestSentenceMatch = re.search(INTEREST_REGEX, sentence)
      if isInterestSentenceMatch:
        date = f"{getDateFromSentence(sentence)} {statementYear}" 
        matchGroup = isInterestSentenceMatch.group(0)
        (_, amount) = sentence.split(matchGroup)
        print(f"{date}: {amount}")
        interestEntries.append([date, float(amount)])
    return interestEntries