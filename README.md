# wealth-purifier
يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ ٱتَّقُوا۟ ٱللَّهَ وَذَرُوا۟ مَا بَقِىَ مِنَ ٱلرِّبَوٰٓا۟ إِن كُنتُم مُّؤْمِنِينَ ٢٧٨

O you who have believed, fear Allāh and give up what remains [due to you] of interest, if you should be believers.

فَإِن لَّمْ تَفْعَلُوا۟ فَأْذَنُوا۟ بِحَرْبٍۢ مِّنَ ٱللَّهِ وَرَسُولِهِۦ ۖ وَإِن تُبْتُمْ فَلَكُمْ رُءُوسُ أَمْوَٰلِكُمْ لَا تَظْلِمُونَ وَلَا تُظْلَمُونَ ٢٧٩

And if you do not, then be informed of a war [against you] from Allāh and His Messenger. But if you repent, you may have your principal - [thus] you do no wrong, nor are you wronged.

[Quran 278-279](https://quran.com/2/278-279)

---

![Wealth Purifier demo video](wealth-purifier-demo.gif)

Web app that helps purify one's wealth of riba by scraping the interest entries from his/her bank statements. 

As someone who likes his zakat calculations to be precise, this application allows me to download the timestamped interest entries in csv format and integrate it with my existing zakat spreadsheets. This lets me know, in a given zakat year, how much of my wealth I need to multiply by 2.5% and how much of it is interest that needs to be given away entirely.

Currently most HK banks don't provide any sort of Open Banking API. Not only that but the list of transactions that can be downloaded in csv format is usually limited to a period of one month. So the only options you have are to either calculate it manually, or to make use of third party services that require you to directly authenticate with your bank account (which requires a degree of trust). So I opted to go down the route of scraping PDF bank statements instead.

PDF scraping/parsing is normally a tricky endeavor but since this application's purpose is very specific, all I had to do was to linear search for sentences matching `INTEREST_REGEX`.


## Technology
This project makes use of simple HTML, CSS, JavaScript for the frontend. Backend is a simple serverless function written in Python + Flask and deployed on Vercel.

By default, the hobby plan of Vercel has a serverless function upload size limit of 4.5MB and a timeout of 10s. To get around this limitation, I opted to batch files in groups of 5 and make multiple serverless function calls in parallel.

## Supported bank statements
Application currently supports the following bank statements
- HSBC One(HKD, USD)
- Mox Bank
- HSBC Statement Savings (this is a relatively old bank account which is no longer issued nowadays)

For HSBC One I currently only support HKD and USD. Feel free to create an issue on this repo if you want other foreign currencies supported. Or you could either extend an existing scraper or write your own.

## Adding your own Scraper
This project utilises the strategy pattern to encapsulate scraping logic for different types of bank statements.

You can write your own scraper if your bank statement type isn't supported.
It has to implement the following interface
```
class Scraper:
  @staticmethod
  def statementSorter(statementName):

  def scrapeInterestEntries(self):
```

`statementSorter` should return a sorting function that uses the filenames of the bank statements to sort in ascending order.

`scrapeInterestEntries` should return an array of arrays in the format of `[ ['28 Jul 2021', 0.01], ... ]`
