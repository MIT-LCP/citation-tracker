"""
Utilities for tracking reuse of LCP resources
"""

from Bio import Entrez

def search(query, email, db='pubmed', sort='relevance', retmax='20', 
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
    
