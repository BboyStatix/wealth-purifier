import pdfplumber
import re

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
    date = match.group(0)
    return date
  
class HSBCStatementSavingsScraper:
  def __init__(self, statement, statementPath):
    self.statement = statement
    with pdfplumber.open(statementPath) as pdf:
      self.pdfContent = extractPDFContent(pdf)
      # with open(f"./generated/HSBCStatementSavings/{statement.split('.')[0]}.txt" , 'w') as f:
      #   f.write(self.pdfContent)
  
  def _getPdfSentences(self):
    return self.pdfContent.split("\n")

  def _getStatementYear(self):
    return self.statement[:4]
  
  def _getInterestAmount(self, sentence):
    (_, remainStr) = sentence.split(f"{INTEREST_REGEX} ")
    return float(remainStr.split(" ")[0])

  def scrapeInterestEntries(self):
    sentences = self._getPdfSentences()
    interestEntries = []
    dateOfCurrentEntry = ""
    statementYear = self._getStatementYear() 
    for sentence in sentences:
      date = getDateFromSentence(sentence)
      if date: dateOfCurrentEntry = f"{date} {statementYear}" 
      if INTEREST_REGEX in sentence:
        interestAmount = self._getInterestAmount(sentence)
        print(f"{dateOfCurrentEntry}: {interestAmount}")
        interestEntries.append([dateOfCurrentEntry, interestAmount])
    return interestEntries





    #   isInterestSentenceMatch = re.search(INTEREST_REGEX, sentence)
    #   if isInterestSentenceMatch:
    #     date = f"{getDateFromSentence(sentence)} {statementYear}" 
    #     matchGroup = isInterestSentenceMatch.group(0)
    #     (_, amount) = sentence.split(matchGroup)
    #     print(f"{date}: {amount}")
    #     interestEntries.append([date, float(amount)])
    # return interestEntries