# wealth-purifier
يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ ٱتَّقُوا۟ ٱللَّهَ وَذَرُوا۟ مَا بَقِىَ مِنَ ٱلرِّبَوٰٓا۟ إِن كُنتُم مُّؤْمِنِينَ ٢٧٨

O you who have believed, fear Allāh and give up what remains [due to you] of interest, if you should be believers.

فَإِن لَّمْ تَفْعَلُوا۟ فَأْذَنُوا۟ بِحَرْبٍۢ مِّنَ ٱللَّهِ وَرَسُولِهِۦ ۖ وَإِن تُبْتُمْ فَلَكُمْ رُءُوسُ أَمْوَٰلِكُمْ لَا تَظْلِمُونَ وَلَا تُظْلَمُونَ ٢٧٩

And if you do not, then be informed of a war [against you] from Allāh and His Messenger. But if you repent, you may have your principal - [thus] you do no wrong, nor are you wronged.

[Quran 278-279](https://quran.com/2/278-279)

---

![Wealth Purifier demo video](wealth-purifier-demo.gif)

Web app that helps purify one's wealth of riba by scraping the interest entries from supported bank statements and returning the total.

## Technology
This project makes use of simple HTML, CSS, JavaScript for the frontend. Backend is a simple serverless function written in Python + Flask deployed on Vercel.

By default, the hobby plan of Vercel has a serverless function upload size limit of 4.5MB and a timeout of 10s. To get around this limitation, I opted to batch files in groups of 5 and make multiple serverless function calls in parallel.

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

`scrapeInterestEntries` should return an array of arrays in the format of e.g. `[ ['28 Jul 2021', 0.01], ... ]`
