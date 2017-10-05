# Query punctuation

- The dash, ie mimic-ii is a superset of “mimic ii” in the text. For example, this text is returned http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1442942 searching with dashes only, but in the article there is no "mimic-ii", only "mimic ii".
- Searching mimic ii without the quotations results in more inappropriate freedom/flexibility. ie. the words 'mimic' and 'ii' just need to both appear somewhere in the article, not necessarily together.
- It is needed to add the non-hyphen non-space version. For instance, (mimic-ii OR mimicii) gives more results than just mimic-ii.





# Conclusions


1. The most stringent search case: (mimic-ii OR mimicii) AND (physionet) produces essentially no false positives.
2. There **MUST be an AND case** to restrict the pure 'mimic' search strings. By themselves, they will generate many false positives such as http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0047914. It's usually some biological specimen or molecular compound. mimic something. The importance is further emphasized when using the numbers instead of the i's. Aside from the biological specimens, without the additional restrictions, the article could just be using the word 'mimic' in the literal sense: to mimic or copy something.
3. The restrictive keywords CANNOT include 'database'. Irrelevant articles with both 'mimic' and 'database' are too frequent.
4. Using 'physionet' as the restrictive term by itself is too restrictive. 662 results, no fp.
5. Using 'icu' as the restrictive term by itself gives 1640 results. However many results are returned from this symposium article. https://ccforum.biomedcentral.com/articles/10.1186/cc14358. Out of 300 returned results, 20 were from this pdf. Out of those 20, all were FP. Example fp: 'Performance of amikacin inhale: impact of supplemental oxygen and device orientation'. In the entire pdf, there were two projects using mimic, out of maybe 200.
6. Using 'icu', 'intensive care', and 'physionet' as restrictive words seems reasonable. Produce few false positives only due to repetition of subsections of articles. Likely does not capture everything.


Final query string: `(mimic-ii OR mimic-iii OR mimicii OR mimiciii OR mimic-2 OR mimic-3 OR mimic2 OR mimic3) AND (icu OR “intensive care”)` with 1950 results.



