"""
Utilities for tracking reuse of LCP resources
"""

from Bio import Entrez
import stem
from stem.control import Controller
from stem.process import launch_tor_with_config
import requests
import dryscrape

import time

def search(query, email, db='pubmed', sort='relevance', retmax='9999', 
            retmode='xml'):
    """
    Search for relevant publications.
    """
    # email is required as point of contact for Entrez
    Entrez.email = email

    # add search critera
    handle = Entrez.esearch(db=db,
                            sort=sort,
                            retmax=retmax,
                            retmode=retmode,
                            term=query)
    # fetch the results
    results = Entrez.read(handle)
    return results

def fetch_details(id_list, email, db='pubmed', retmode='xml'):
    """
    Fetch details of articles using the search results
    """
    # email is required as point of contact for Entrez
    Entrez.email = email

    # fetch the results
    ids = ','.join(id_list)
    handle = Entrez.efetch(db=db, retmode=retmode, id=ids)
    results = Entrez.read(handle)
    
    return results

# Get the paper title
def get_title(id, email):
    
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=id)
    result = Entrez.read(handle)
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
    
    # make them lower case and remove fullstops to make comparable with other
    # search results
    title = title.lower()
    if title.endswith('.'):
        title = title[:-1]
    return title

class SearchResult(object):
    def __init__(self, search_string=None, results=None, paper_ids=None, paper_titles=None, count=None):
        self.search_string = search_string
        self.results = results
        self.paper_ids = paper_ids
        self.paper_titles = paper_titles
        self.count = count
        
def search_list(search_strings, email):
    """
    Search a list of search_strings.
    Return a dictionary of SearchResult objects as values for the search_string keys
    """
    search_results = {}
    # Dictionary of {k-v} = {paper ids - titles} for the set of IDs found in all search strings
    all_paper_titles = []

    for ss in search_strings:

        # Overall results
        results = search(ss, email)
        ids = results['IdList']
        sr = SearchResult(search_string = ss, results = results, paper_ids = ids, count = results['Count'])

        # Add the results to the dictionary
        search_results[ss] = sr
        all_paper_titles += ids

    all_paper_titles = set(all_paper_titles)
    all_paper_titles = dict(zip(all_paper_titles, [get_title(t, email) for t in all_paper_titles]))

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

