WikiParser
==========
This is a simple parser for looking for stuff in Wikipedia XML dumps. 

In the current version, it checks all articles for redirects and <ref>-tags. If an article doesn't redirect, and doesn't contain at least one instance of <ref>, it's likely to be unreferenced. Some exceptions exist, such as articles starting with "List", so these are excluded. 
Articles failing the check (no ref, no redirect, not a List) is logged for future use. 

Please note that this was made more or less in order to learn a bit of Python, so a lot of things can probably be done better and more efficient. 

If anyone else feels like playing with it, it's licensed under the BSD license. Please let me know if you find it useful in any way!


Future plans
==========
-General and per-article statistics
	-Article length, link/extlink count, imagecount per article and average
	-Longest article
	-Number of lists, redirects and comparisons
-Ignorelists; not sure how, but articles on years, months, days, and numbers should be ignored
-For articles lacking <ref>-tags, also indicate the number of external links
	-Possibly also look for any of the cite templates

Future plans not likely to be implemented
==========
Per-article stats between each dump. Basically register the page length per dump, find the diff and list the highs and lows. 
