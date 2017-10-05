# Citation Tracker

The goal is to create a reusable tool for tracking use of LCP resources in research papers. e.g. So we can answer the questions, "which research papers were carried out with the use of MIMIC" and "which research papers were carried out with the use of the eICU Collaborative Research Database"?



## Python Requirements

biopython http://biopython.org/
stem (Tor interface. Requires installation and configuration of tor) http://stem.torproject.org/ 
dryscrape (For js enabled queries. Requires additional software libraries. See github readme) https://github.com/niklasb/dryscrape


# Citation Tracking Services

# Google Scholar

# Medline

MEDLINE is the National Library of Medicine (NLM) journal citation database. It provides millions of references to biomedical and life sciences journal articles from thousands of scholarly journals.

Publishers submit journals to an NIH-chartered advisory committee (the LSTRC) which reviews and recommends journals for MEDLINE. The LSTRC considers the quality of the scientific content of a journal including originality and the importance of the content for the MEDLINE global audience, using the guidelines found on the NLM Fact Sheet MEDLINE Journal Selection.

In addition to the comprehensive journal selection process, what sets MEDLINE apart from the rest of PubMed is the added value of using the NLM controlled vocabulary, Medical Subject Headings, to index citations.

Medline topics include the fields of medicine, nursing, dentistry, veterinary medicine, health care systems, and preclinical sciences.

## Resources

- Search URL: https://www.ncbi.nlm.nih.gov/nlmcatalog/
- Fact sheet describing medline: https://www.nlm.nih.gov/pubs/factsheets/medline.html
- FAQ - Finding Medline indexed journals: https://www.nlm.nih.gov/services/medline_titles.html
- Currently indexed Medline journals: https://www.ncbi.nlm.nih.gov/nlmcatalog/?term=currentlyindexed
- MEDLINE Journal Selection: https://www.nlm.nih.gov/pubs/factsheets
- Fact sheet describing Medline, Pubmed, and PMC differences: https://www.nlm.nih.gov/pubs/factsheets/dif_med_pub.html

# Pubmed

Pubmed's contents are a superset of Medline's. PubMed provides millions of references which include the MEDLINE database plus the following types of citations:
- In-process citations, which provide records for articles before those records are indexed with MeSH or converted to out-of-scope status.
- Citations to articles that are out-of-scope (e.g., covering plate tectonics or astrophysics) from certain MEDLINE journals, primarily **general science and general chemistry journals**, for which only the life sciences articles are indexed with MeSH.
- "Ahead of Print" citations that precede the article's final publication in a MEDLINE indexed journal.
- Citations that precede the date that a journal was selected for MEDLINE indexing (when supplied electronically by the publisher).
- Pre-1966 citations that have not yet been updated with current MeSH and converted to MEDLINE status.
- Citations to some additional life sciences journals that submit full text to PMC (PubMed Central) and receive a qualitative review by NLM.
- Citations to author manuscripts of articles published by NIH-funded researchers.
- Citations for the majority of books available on the NCBI Bookshelf (a citation for the book and in some cases each chapter of the book).

## Resources

- Search URL: https://www.ncbi.nlm.nih.gov/pubmed/
- Fact sheet describing pubmed: https://www.nlm.nih.gov/pubs/factsheets/pubmed.html
- FAQ - Finding Pubmed indexed journals: https://www.nlm.nih.gov/services/pubmed_titles.html
- Currently indexed Pubmed journals: https://www.ncbi.nlm.nih.gov/nlmcatalog/?term=currentlyindexed+OR+journalspmc
- Pubmed journal list: https://www.nlm.nih.gov/bsd/serfile_addedinfo.html


- https://www.nlm.nih.gov/bsd/serfile_addedinfo.html
List of all: ftp://ftp.ncbi.nih.gov/pubmed/J_Medline.txt

# Pubmed Central

PMC is a free archive for full-text biomedical and life sciences journal articles. PMC serves as a digital counterpart to the NLM extensive print journal collection; it is a repository for journal literature deposited by participating publishers, as well as for author manuscripts that have been submitted in compliance with the NIH Public Access Policy and similar policies of other research funding agencies.

Some PMC journals are also MEDLINE journals. For publishers, there are a number of ways to participate and deposit their content in this archive, explained on the NLM Web pages Add a Journal to PMC and PMC Policies.

Journals must be in scope according to the NLM Collection Development Manual. Although free access is a requirement for PMC deposit, publishers and individual authors may continue to hold copyright on the material in PMC and publishers can delay the release of their material in PMC for a short period after publication. There are reciprocal links between the full text in PMC and corresponding citations in PubMed. PubMed citations are created for content not already in the MEDLINE database. Some PMC content, such as book reviews, is not cited in PubMed.

## Resources

- Searching PMC: https://www.ncbi.nlm.nih.gov/pmc/
- PMC FAQ: https://www.ncbi.nlm.nih.gov/pmc/about/faq/

# Medline Pubmed PMC Summary

In conclusion, PubMed citations come from:
- MEDLINE indexed journals
- Journals/manuscripts deposited in PMC
- NCBI Bookshelf

Both MEDLINE and other PubMed citations may have links to full-text articles or manuscripts in PMC, NCBI Bookshelf, and publishers' Web sites.



# Web of Science

# SCOPUS

## Resources

- Search URL: https://www.scopus.com/search/form.uri?display=basic
- 

# Individual Search Result Numbers

Using search query: `(mimic-ii OR mimic-iii OR mimicii OR mimiciii OR mimic-2 OR mimic-3 OR mimic2 OR mimic3) AND (physionet OR icu OR “intensive care” OR “critical care”)`on 2 October 2017:
- Google Scholar (do not include citations, do not include patents, include all languages): "about 2180"
- Pubmed: 121
- Pubmed Central: 230
- Web of Science: 132
- SCOPUS: 171


