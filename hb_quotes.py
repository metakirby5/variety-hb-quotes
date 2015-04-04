from variety.plugins.IQuoteSource import IQuoteSource
from gettext import gettext as _
from urllib2 import urlopen, Request, HTTPError, URLError
from urllib import quote as escape
import logging
import itertools
import json

logger = logging.getLogger("variety")

class IHBQuotes(IQuoteSource):

  @classmethod
  def get_info(cls):
    return {
      "name": "Hummingbird.me",
      "version": "0.1",
      "description": _("Grabs quotes from Hummingbird.me.\n"
                       "Keyword search is by anime_id. If none provided,"
                       "Monogatari Series quotes are used."
                       "Example:\n"
                       "  monogatari-series-second-season\n\n"
                       "No support for author search."),
      "author": "Ethan Chan",
      "url": "https://github.com/metakirby5/variety-hb-quotes",
    }

  REQ_URL = "https://hummingbird.me/quotes?anime_id=%s"
  REQ_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
  }

  DEFAULT_SERIES = [
    'bakemonogatari',
    'nisemonogatari',
    'nekomonogatari-kuro',
    'monogatari-series-second-season',
    'hanamonogatari',
  ]

  # JSON request to API
  def quote_json(self, anime_id):
    # Make series safe to search for
    anime_id = escape(anime_id.strip(), '')
    req = Request(self.REQ_URL % anime_id, headers=self.REQ_HEADERS)
    f = urlopen(req)
    quotes = json.loads(f.read())['quotes']
    f.close()
    logger.info('Got quotes for anime_id: %s' % anime_id)
    return quotes

  # Formats from HB to Variety
  # Returns a list with as many entries as favorite counts
  def format_entry(self, q):
    return [{
      'quote': q['content'],
      'author': q['character_name'],
      'sourceName': 'Hummingbird',
      'link': "https://hummingbird.me/anime/%s/quotes" % q['anime_id'],
    }] * q['favorite_count']

  # Returns a list of series quotes, multiplicity=favorite_count
  def get_series_quotes(self, anime_id):
    try:
      return itertools.chain(*map(self.format_entry,
                                  self.quote_json(anime_id)))
    except HTTPError:
      logger.error("No series found matching anime_id: %s" % anime_id)
      return []
    except URLError:
      logger.error('No internet connection')
      return []

  #####

  def __init__(self):
    super(IHBQuotes, self).__init__()
    self.default_quotes = []

  def supports_search(self):
    return True

  def activate(self):
    if self.active:
      return
    super(IHBQuotes, self).activate()

    self.default_quotes = \
      itertools.chain(*[self.get_series_quotes(s)
                        for s in self.DEFAULT_SERIES])
    logger.info('Created default quotes for %s' % self.DEFAULT_SERIES)

  def deactivate(self):
    super(IHBQuotes, self).deactivate()
    self.default_quotes = []

  def get_random(self):
    return self.default_quotes

  # Keyword = series
  def get_for_keyword(self, keyword):
    return self.get_series_quotes(keyword)

