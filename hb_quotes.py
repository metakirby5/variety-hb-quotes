from variety.plugins.IQuoteSource import IQuoteSource
from gettext import gettext as _
from urllib2 import urlopen, Request
from urllib import quote as escape
import logging
import itertools
import json

logger = logging.getLogger("variety")

class IHBQuotes(IVarietyPlugin):

  @classmethod
  def get_info(cls):
    return {
      "name": "Hummingbird.me",
      "description": _("Grabs quotes from Hummingbird.me.\n"
                       "Keyword search is by anime_id. If none provided,"
                       "Monogatari Series quotes are used."
                       "Example:\n"
                       "  monogatari-series-second-season\n\n"
                       "No support for author search."),
      "author": "Ethan Chan",
      "version": "0.1"
    }

  REQ_URL = "https://hummingbird.me/quotes?anime_id=%s"
  REQ_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
  }
  # A list with as many entries as favorite counts
  FORMAT_ENTRY = lambda q: [{
    'quote': q['content'],
    'author': q['character_name'],
    'sourceName': 'Hummingbird',
    'link': "https://hummingbird.me/anime/%s/quotes" % q['anime_id'],
  }] * q['favorite_count']

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
    anime_id = escape(anime_id, '')
    req = Request(REQ_URL % anime_id, headers=REQ_HEADERS)
    with urlopen(req) as f:
      return json.loads(f.read())['quotes']

  # Returns a list of series quotes, multiplicity=favorite_count
  def get_series_quotes(self, anime_id):
    try:
      return itertools.chain(*map(FORMAT_ENTRY, quote_json(anime_id)))
    except URLError:
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

    self.default_quotes =
      itertools.chain(*[get_series_quotes(s) for s in DEFAULT_SERIES])

  def deactivate(self):
    super(IHBQuotes, self).deactivate()
    self.default_quotes = []

  def get_random(self):
    return self.default_quotes

  # Keyword = series
  def get_for_keyword(self, keyword):
    return get_series_quotes(keyword)

