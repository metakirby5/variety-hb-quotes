# variety-hb-quotes
Variety (wallpaper changer @ http://peterlevi.com/variety/) plugin to pull quotes from Hummingbird.me

## Installation
1. `wget -P ~/.config/variety/plugins/quotes https://raw.githubusercontent.com/metakirby5/variety-hb-quotes/master/hb_quotes.py`
2. Restart Variety.
3. Activate the plugin under `Effects -> Quotes -> Sources and filtering`.
4. Under `Tags`, enter a comma-separated list of Hummingbird.me anime ID's. To find these, look at the last part of an anime page's URL. For example, the anime ID for "Monogatari Series: Second Season" can be found by visiting `https://hummingbird.me/anime/monogatari-series-second-season` and extracting the last portion, `monogatari-series-second-season`.
5. Enjoy as Senjougahara belittles your existence.

## Notes
* If no `Tags` are entered, quotes from the Monogatari series will be fetched.
* Last tested with `variety 0.5.0`.
