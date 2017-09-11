"""
Utilities for tracking reuse of LCP resources
"""

from Bio import Entrez

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

