from urllib.parse import urlencode


class AdvancedSearch:

    def __init__(self, all_words, some_words, exact_phrase, exclude_words, exact_search,
                 place, newspaper_title, fromdate, todate, fromaddeddate, toaddeddate,
                 article_type, front_page, tags, sort):
        self.all_words = all_words
        self.some_words = some_words
        self.exact_phrase = exact_phrase
        self.exclude_words = exclude_words
        self.exact_search = exact_search
        self.place = place
        self.newspaper_title = newspaper_title
        self.fromdate = fromdate
        self.todate = todate
        self.fromaddeddate = fromaddeddate
        self.toaddeddate = toaddeddate
        self.article_type = article_type
        self.front_page = front_page
        self.tags = tags
        self.sort = sort

    @classmethod
    def from_row(cls, row):
        return cls(row[0].value, row[1].value, row[2].value, row[3].value,
                   row[4].value, row[5].value, row[6].value, row[7].value,
                   row[8].value, row[9].value, row[10].value, row[11].value,
                   row[12].value, row[13].value, row[14].value)

    @classmethod
    def copy_item(cls, instance):
        return cls(instance.all_words, instance.some_words, instance.exact_phrase, instance.exclude_words,
                   instance.exact_search, instance.place, instance.newspaper_title, instance.fromdate,
                   instance.todate, instance.fromaddeddate, instance.toaddeddate, instance.article_type,
                   instance.front_page, instance.tags, instance.sort)

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
            if self.fromdate is not None:
                base += '/' + self.fromdate
                if self.todate is not None:
                    base += '/' + self.todate
                base += '?'
            else:
                base += '?'
                if self.todate is not None:
                    query_params['dateto'] = self.todate
        query_params['basicsearch'] = self.get_basic_search_string()
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
        if self.place is not None:
            query_params['place'] = self.place
            query_params['mostspecificlocation'] = self.place
        if self.newspaper_title is not None:
            query_params['newspapertitle'] = self.newspaper_title
        if self.fromaddeddate is not None:
            query_params['dateaddedfrom'] = self.fromaddeddate
        if self.toaddeddate is not None:
            query_params['dateaddedto'] = self.toaddeddate
        if self.article_type is not None:
            query_params['contenttype'] = self.article_type
        if self.front_page is not None:
            if self.front_page == 1:
                query_params['frontpage'] = 'true'
        if self.tags is not None:
            query_params['publictags'] = self.tags.strip()
        if self.sort is not None:
            if self.sort == 'Relevance':
                query_params['sortorder'] = 'score'
            elif self.sort == 'Date (earliest)':
                query_params['sortorder'] = 'dayEarly'
            elif self.sort == 'Date (most recent)':
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
        if self.fromdate is not None:
            basic_input += 'fd-' + self.fromdate
        if self.todate is not None:
            basic_input += 'td-' + self.todate
        return basic_input.strip()
