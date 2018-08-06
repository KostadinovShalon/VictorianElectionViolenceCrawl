from urllib import urlencode


class AdvancedSearch:

    def __init__(self, row):
        self.all_words = row[0].value
        self.some_words = row[1].value
        self.exact_phrase = row[2].value
        self.exclude_words = row[3].value
        self.exact_search = row[4].value
        self.place = row[5].value
        self.newspaper_title = row[6].value
        self.fromdate = row[7].value
        self.todate = row[8].value
        self.fromaddeddate = row[9].value
        self.toaddeddate = row[10].value
        self.article_type = row[11].value
        self.front_page = row[12].value
        self.tags = row[13].value
        self.sort = row[14].value

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

    def get_url(self):
        base = 'https://www.britishnewspaperarchive.co.uk/search/results'
        query_params = {}
        if self.fromdate is not None:
            base += '/' + self.fromdate.strftime('%Y-%m-%d')
            if self.todate is not None:
                base += '/' + self.todate.strftime('%Y-%m-%d')
            base += '?'
        else:
            base += '?'
            if self.todate is not None:
                query_params['dateto'] = self.todate.strftime('%Y-%m-%d')
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
            query_params['dateaddedfrom'] = self.fromaddeddate.strftime('%Y-%m-%d')
        if self.toaddeddate is not None:
            query_params['dateaddedto'] = self.toaddeddate.strftime('%Y-%m-%d')
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
            basic_input += 'fd-' + self.fromdate.strftime('%Y-%m-%d')
        if self.todate is not None:
            basic_input += 'td-' + self.todate.strftime('%Y-%m-%d')
        return basic_input.strip()
