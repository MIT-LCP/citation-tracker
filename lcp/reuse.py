"""
Utilities for tracking reuse of LCP resources
"""

# import time

from Bio import Entrez
import pandas as pd


def search(query, email, db='pubmed', sort='relevance', retmax='9999',
           retmode='xml'):
    """
    Search for relevant publications.
    """
    # Email is required as point of contact for Entrez
    Entrez.email = email
    # Add search critera
    handle = Entrez.esearch(db=db,
                            sort=sort,
                            retmax=retmax,
                            retmode=retmode,
                            term=query)
    # Fetch the results
    results = Entrez.read(handle)
    return results


def fetch_details(id_list, email, db='pubmed', retmode='xml'):
    """
    Fetch details of articles using the search results.
    """
    # Email is required as point of contact for Entrez
    Entrez.email = email
    # Fetch the results
    ids = ','.join(id_list)
    handle = Entrez.efetch(db=db, retmode=retmode, id=ids)
    results = Entrez.read(handle)
    return results


def get_title(id, email):
    """
    Get the paper title.
    """
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=id)
    result = Entrez.read(handle)
    try:
        # Article
        article = result['PubmedArticle'][0]
        citation = article['MedlineCitation']
        """
        citation.keys():

        [u'DateCompleted',
        u'OtherID',
        u'DateRevised',
        u'MeshHeadingList',
        u'OtherAbstract',
        u'CommentsCorrectionsList',
        u'CitationSubset',
        u'KeywordList',
        u'DateCreated',
        u'SpaceFlightMission',
        u'GeneralNote',
        u'Article',
        u'PMID',
        u'MedlineJournalInfo']
        """

        finalarticle = citation['Article']
        """
        finalarticle.keys():
        [u'ArticleDate',
        u'Pagination',
        u'AuthorList',
        u'Language',
        u'PublicationTypeList',
        u'Journal',
        u'ArticleTitle',
        u'ELocationID',
        u'Abstract']
        """

        title = finalarticle['ArticleTitle']

    except IndexError:
        # Book
        book = result['PubmedBookArticle'][0]
        title = book['BookDocument']['Book']['BookTitle']

    # Make them lower case and remove fullstops to make comparable with other
    # search results
    title = title.lower()
    if title.endswith('.'):
        title = title[:-1]

    # Some results get square brackets. Error?
    while '[' in title or ']' in title:
        title = title.replace('[', '')
        title = title.replace(']', '')
    return title


def get_all_info(id, email):
    """
    Get all of the paper information.
    """
    # Fetch information
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=id)
    result = Entrez.read(handle)
    # Generate the DataFrame
    temp_df = {}
    try:
        current_citation = result['PubmedArticle'][0]['MedlineCitation']['Article']
        IS_BOOK = False
    except IndexError:
        # Book instead of article
        current_citation = result['PubmedBookArticle'][0]['BookDocument']['Book']
        IS_BOOK = True
    temp_df['Title'] = get_title(id, email)
    try:
        if not IS_BOOK:
            publication_date = current_citation['ArticleDate'][0]
        else:
            publication_date = current_citation['PubDate']
    except IndexError:
        publication_date = current_citation['Journal']['JournalIssue']['PubDate']
    try:
        pub_day = publication_date['Day']
    except KeyError:
        pub_day = 'XX'
    try:
        pub_month = publication_date['Month']
        month_lookup = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }
        if len(pub_month) == 3:
            pub_month = month_lookup[pub_month]
    except KeyError:
        pub_month = 'XX'
    try:
        pub_year = publication_date['Year']
    except KeyError:
        # Should always be the first 4 characters?
        try:
            pub_year = publication_date['MedlineDate'][:4]
        except KeyError:
            # I don't think this should ever happen?
            pub_year = 'XXXX'
    temp_df['Publication Day'] = pub_day
    temp_df['Publication Month'] = pub_month
    temp_df['Publication Year'] = pub_year
    if not IS_BOOK:
        current_journal = current_citation['Journal']
        temp_df['Journal Name'] = current_journal['Title']
        try:
            temp_df['Journal Volume'] = current_journal['JournalIssue']['Volume']
        except KeyError:
            pass
        try:
            temp_df['Journal Issue'] = current_journal['JournalIssue']['Issue']
        except KeyError:
            pass
        try:
            temp_df['Journal ISSN'] = str(current_journal['ISSN'])
        except KeyError:
            pass
    else:
        temp_df['Publisher Name'] = current_citation['Publisher']['PublisherName']
        temp_df['Publisher Location'] = current_citation['Publisher']['PublisherLocation']
        all_ISBNs = current_citation['Isbn']
        for i,isbn in enumerate(all_ISBNs):
            temp_df[f'ISBN {i+1}'] = isbn
    # Each author information
    if not IS_BOOK:
        author_list = current_citation['AuthorList']
    else:
        author_list = result['PubmedBookArticle'][0]['BookDocument']['AuthorList'][0]
    ca_count = 1
    for i,a in enumerate(author_list):
        try:
            temp_df[f'Author {i+1} First Name'] = a['ForeName']
        except KeyError:
            try:
                # No actual author, just big group of people
                temp_df[f'Collective Author {ca_count}'] = a['CollectiveName']
                ca_count += 1
                continue
            except KeyError:
                # Not sure what's up here
                pass
        temp_df[f'Author {i+1} Last Name'] = a['LastName']
        try:
            temp_df[f'Author {i+1} Affiliation'] = a['AffiliationInfo'][0]['Affiliation']
        except IndexError:
            pass
    return pd.DataFrame([temp_df])


class SearchResult(object):
    def __init__(self, search_string=None, results=None, paper_ids=None,
                 paper_titles=None, all_info=None, count=None):
        self.search_string = search_string
        self.results = results
        self.paper_ids = paper_ids
        self.paper_titles = paper_titles
        self.all_info = all_info
        self.count = count


def search_list(search_strings, email, all=False):
    """
    Search a list of search_strings. Return a dictionary of `SearchResult`
    objects as values for the `search_strings` keys.

    If `all` is True, return all article information, else return only the
    titles.

    """
    search_results = {}
    # Dictionary of {k-v} = {paper ids - titles} for the set of IDs found in all search strings
    if all:
        all_ids = {}
    else:
        all_ids = []

    for ss in search_strings:
        # Overall results
        results = search(ss, email)
        ids = results['IdList']
        sr = SearchResult(search_string=ss, results=results, paper_ids=ids,
                          count=results['Count'])
        # Add the results to the dictionary
        if all:
            all_ids[ss] = set(ids)
        else:
            search_results[ss] = sr
            all_ids += ids

    if not all:
        all_ids = set(all_ids)
    if all:
        for ss in search_strings:
            search_results[ss] = pd.concat([get_all_info(id, email) for id in all_ids[ss]])
    else:
        all_paper_titles = dict(zip(all_ids, [get_title(id, email) for id in all_ids]))
        # Fill in the paper titles
        for ss in search_strings:
            search_results[ss].paper_titles = [all_paper_titles[id] for id in search_results[ss].paper_ids]

    return search_results


def showdiff(results_a, results_b):
    print('Query A: '+results_a.search_string+', '+results_a.count+'results')
    print('Query B: '+results_b.search_string+', '+results_b.count+'results')
    print('(A - B):')
    display(set(results_a.paper_titles) - set(results_b.paper_titles))
    print('(B - A):')
    display(set(results_b.paper_titles) - set(results_a.paper_titles))
    print('\n')
    return


# --------------- Google Scholar ------------------ #



# class TorRequest(object):
#     def __init__(self,
#           proxy_port=9050,
#           ctrl_port=9051,
#           password=None):

#         self.proxy_port = proxy_port
#         self.ctrl_port = ctrl_port

#         self._tor_proc = None
#         if not self._tor_process_exists():
#           self._tor_proc = self._launch_tor()

#         self.ctrl = Controller.from_port(port=self.ctrl_port)
#         self.ctrl.authenticate(password=password)

#         #self.session = requests.Session()
#         #self.session.proxies.update({
#         #  'http': 'socks5://localhost:%d' % self.proxy_port,
#         #  'https:': 'socks5://localhost:%d' % self.proxy_port,
#         #})
#         self.session = dryscrape.Session()
#         self.session.


#     def _tor_process_exists(self):
#         try:
#           ctrl = Controller.from_port(port=self.ctrl_port)
#           ctrl.close()
#           return True
#         except:
#           return False

#     def _launch_tor(self):
#         return launch_tor_with_config(
#           config={
#             'SocksPort': str(self.proxy_port),
#             'ControlPort': str(self.ctrl_port)
#           },
#           take_ownership=True)

#     def close(self):
#         try: 
#           self.session.close()
#         except: pass

#         try: 
#           self.ctrl.close()
#         except: pass

#     if self._tor_proc:
#       self._tor_proc.terminate()

#     def reset_identity_async(self):
#         self.ctrl.signal(stem.Signal.NEWNYM)

#     def reset_identity(self):
#         self.reset_identity_async()
#         time.sleep(self.ctrl.get_newnym_wait())

#     def get(self, *args, **kwargs):
#         return self.session.get(*args, **kwargs)

#     def post(self, *args, **kwargs):
#         return self.session.post(*args, **kwargs)

#     def put(self, *args, **kwargs):
#         return self.session.put(*args, **kwargs)

#     def patch(self, *args, **kwargs):
#         return self.session.patch(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         return self.session.delete(*args, **kwargs)

#     def __enter__(self):
#     return self

#     def __exit__(self, *args):
#     self.close()

