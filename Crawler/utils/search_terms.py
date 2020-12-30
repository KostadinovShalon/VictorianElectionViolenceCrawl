from urllib.parse import urlencode


class SearchTerms:

    def __init__(self, search_text, start_date, end_date):
        self.search_text = search_text
        self.start_date = start_date
        self.end_date = end_date

    def copy(self):
        return SearchTerms(self.search_text, self.start_date, self.end_date)

    def __repr__(self):
        return "Search (search text = '%s', start = '%s', end = '%s')" % (
            self.search_text, self.start_date, self.end_date)

    def to_dict(self):
        return {
            "keyword": self.search_text,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }


class RecoverySearchTerms(SearchTerms):

    def __init__(self, search_id, search_text, start_date, end_date):
        super().__init__(search_text, start_date, end_date)
        self.id = search_id


class AdvancedSearchTerms(SearchTerms):

    def __init__(self, start_date=None, end_date=None, added_start_date=None, added_end_date=None,
                 article_type=None, exact_phrase=None, exact_search=None, exclude_words=None, front_page=None,
                 newspaper_title=None, publication_place=None, all_words=None, some_words=None, sort_by=None, tags=None,
                 timestamp=None):
        self.added_start_date = added_start_date
        self.added_end_date = added_end_date
        self.article_type = article_type
        self.exact_phrase = exact_phrase
        self.exact_search = exact_search
        self.exclude_words = exclude_words
        self.front_page = front_page
        self.newspaper_title = newspaper_title
        self.publication_place = publication_place
        self.all_words = all_words
        self.some_words = some_words
        self.sort_by = sort_by
        self.tags = tags
        self.timestamp = timestamp
        super().__init__(self.get_basic_search_string(), start_date, end_date)

    def copy(self):
        return AdvancedSearchTerms(self.start_date, self.end_date, self.added_start_date, self.added_end_date,
                                   self.article_type, self.exact_phrase, self.exact_search, self.exclude_words,
                                   self.front_page, self.newspaper_title, self.publication_place, self.all_words,
                                   self.some_words, self.sort_by, self.tags, self.timestamp)

    def get_basic_search_string(self):
        basic_search = ''
        if self.all_words is not None:
            for word in self.all_words.strip().split(' '):
                basic_search += '+' + word + ' '
        if self.some_words is not None:
            basic_search += self.some_words.strip() + ' '
        if self.exact_phrase is not None:
            basic_search += '"' + self.exact_phrase + '" '
        if self.exclude_words is not None:
            for word in self.exclude_words.strip().split(' '):
                basic_search += '-' + word + ' '
        return basic_search.strip()

    def get_url(self, from_date=None, to_date=None):
        base = 'https://www.britishnewspaperarchive.co.uk/search/results'
        query_params = {}
        if from_date is not None and to_date is not None:
            base += '/' + from_date
            base += '/' + to_date
            base += '?'
        else:
            if self.start_date is not None:
                base += '/' + self.start_date
                if self.end_date is not None:
                    base += '/' + self.end_date
                base += '?'
            else:
                base += '?'
                if self.end_date is not None:
                    query_params['dateto'] = self.end_date
        query_params['basicsearch'] = self.search_text
        if self.all_words is not None:
            query_params['freesearch'] = self.all_words.strip()
        if self.exact_phrase is not None:
            query_params['phrasesearch'] = self.exact_phrase.strip()
        if self.exclude_words is not None:
            query_params['notsearch'] = self.exclude_words.strip()
        if self.some_words is not None:
            query_params['somesearch'] = self.some_words.strip()
        if self.exact_search is not None:
            if self.exact_search == 1:
                query_params['exactsearch'] = 'true'
        query_params['retrievecountrycounts'] = 'false'
        if self.publication_place is not None:
            query_params['place'] = self.publication_place
            query_params['mostspecificlocation'] = self.publication_place
        if self.newspaper_title is not None:
            query_params['newspapertitle'] = self.newspaper_title
        if self.added_start_date is not None:
            query_params['dateaddedfrom'] = self.added_start_date
        if self.added_end_date is not None:
            query_params['dateaddedto'] = self.added_end_date
        if self.article_type is not None:
            if isinstance(self.article_type, list):
                query_params['contenttype'] = ",".join(self.article_type)
            else:
                query_params['contenttype'] = self.article_type
        if self.front_page is not None:
            if self.front_page == 1:
                query_params['frontpage'] = 'true'
        if self.tags is not None:
            query_params['publictags'] = self.tags.strip()
        if self.sort_by is not None:
            if self.sort_by == 'Relevance':
                query_params['sortorder'] = 'score'
            elif self.sort_by == 'Date (earliest)':
                query_params['sortorder'] = 'dayEarly'
            elif self.sort_by == 'Date (most recent)':
                query_params['sortorder'] = 'dayRecent'
        return base + urlencode(query_params)

    def get_search_input(self):
        basic_input = ''
        if self.all_words is not None:
            basic_input += 'aw-' + self.all_words + '_'
        if self.some_words is not None:
            basic_input += 'sw-' + self.some_words.strip() + '_'
        if self.exact_phrase is not None:
            basic_input += 'ep-' + self.exact_phrase + '_'
        if self.exclude_words is not None:
            basic_input += 'ew-' + self.exclude_words + '_'
        if self.start_date is not None:
            basic_input += 'fd-' + self.start_date
        if self.end_date is not None:
            basic_input += 'td-' + self.end_date
        return basic_input.strip()

    def __repr__(self):
        return "Advanced " + super().__repr__()

    def to_dict(self):
        return {
            "fromDate": self.start_date,
            "toDate": self.end_date,
            "fromDateAddedToSystem": self.added_start_date,
            "toDateAddedToSystem": self.start_date,
            "articleType": self.added_end_date,
            "useExactPhrase": self.article_type,
            "exactSearch": self.exact_search,
            "excludeWords": self.exclude_words,
            "frontPageArticlesOnly": self.front_page,
            "newspaperTitle": self.newspaper_title,
            "publicationPlace": self.publication_place,
            "searchAllWords": self.all_words,
            "searchSomeWords": self.some_words,
            "sortResultsBy": self.sort_by,
            "tags": self.tags,
        }


class RecoveryAdvancedSearchTerms(AdvancedSearchTerms):

    def __init__(self, search_id, start_date=None, end_date=None, added_start_date=None, added_end_date=None,
                 article_type=None, exact_phrase=None, exact_search=None, exclude_words=None, front_page=None,
                 newspaper_title=None, publication_place=None, all_words=None, some_words=None, sort_by=None, tags=None,
                 timestamp=None):
        super().__init__(start_date, end_date, added_start_date, added_end_date,
                         article_type, exact_phrase, exact_search, exclude_words, front_page,
                         newspaper_title, publication_place, all_words, some_words, sort_by, tags,
                         timestamp)
        self.search_id = search_id
