"""
Utilities for tracking reuse of LCP resources
"""

from Bio import Entrez

def helloworld():

    a = ['h','l','o','o','l']
    b = ['e','l',' w','r','d']
    c = ''
    
    for i in zip(a,b):
        c = c + i[0] + i[1]
    
    return c

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
