# Thiago R. - 2/2/2024

'''This program is designed to be modified manually in order to be able to read OCR'd PDFs and then
return text files containing pages containing select terms
after doing both a direct and then fuzzy search with a 65%
threshold for terms relating to Rachmaninoff,
friend of Igor Sikorsky. Meant to be in the same directory as the files being data scraped.'''

'''KNOWN ISSUES:
- When iterating through large volumes of PDFs, will not execute successfully if one of those files has no valid EOF marker.
 * Could be fixed by re-OCRing all scannned files separately, but unsure yet.
'''

from PyPDF2 import PdfReader
import os 
from fuzzywuzzy import fuzz


# Delete any pre-existing text files to avoid appending new iterations of content after updating the algorithim for new searches

for deprecated_file in os.listdir():
    if deprecated_file.endswith('.txt'):
        print(f"Deleting {deprecated_file} before the new iteration of file scraping!\n")
        os.remove(deprecated_file)

# Iterate through all files, in local directory, ignore any file other than a PDF

def analyze_files(file_name):
    if file_name.endswith('.pdf') == False:
        print("Invalid file type! Returning!") # Skips over non-.pdf-ending files.
        return
    pdf = PdfReader(file_name)

    # Take the index of all pages in the selected pdf and use that to iterate through all pages
    
    for x, y in enumerate(pdf.pages):
        page = pdf.pages[x]        
        
        # Create extracted text from page after replacing invalid unicode blank character with space
        
        extracted_text = page.extract_text() # Replaces unicode character that causes errors when read, there may be more.
        
        # Save data of page if 'Rachmaninoff' is in the page's OCR, and name it appropriately.
        
        if 'Rachmaninoff' in extracted_text:
            print(f"!!! DIRECT MATCH !!! PAGE {x+1} of {file_name} HAS 'Rachmaninoff'!")
            direct_match_file = open(f"{file_name}_direct_match.txt", "a") # direct matches
            direct_match_file.write(f"Page {x+1} of {file_name} is a direct match! 'Rachmaninoff' is present!\n\n\n"
                                    f"EXTRACTED TEXT FROM PAGE {x+1} of {file_name}:"
                                    f"\n\n\n{extracted_text}\n\n\n")
            direct_match_file.close()

        potentially_similar_words = extracted_text.split()    # Split the page text into individual words for comparison 
 
        '''Compare every word in the page OCR to the word 'Rachmaninoff', if it is greater or 
        equal to 65% similar, save the page data, and say which word triggered the response, and then append it.
        Will be differentiated from files generated by direct matches with a different name when generated.'''

        for word in potentially_similar_words:
            if fuzz.ratio(word, 'rachmaninoff') >= 65 and 'Rachmaninoff' not in word:
                match_index = potentially_similar_words.index(word)
                fuzzword = potentially_similar_words[match_index].replace(" ", "")
                print(f"! Potential match !: Page {x+1} of {file_name} has a 67% or more similar word."
                      f" Term that triggered similar match is {fuzzword}.")
                maybe_match_file = open(f"{file_name}_maybe_match.txt", "a")
                maybe_match_file.write(f"! Potential match !: Page {x+1} of {file_name}, "
                                       f"triggered by term '{fuzzword}'"
                                        f" Extracted text from page {x+1} of "
                                        f"{file_name}: \n\n\n{extracted_text}\n\n\n")
                    
                maybe_match_file.close()

# For loop that automatically runs at the beginning of every time this file is ran.

for x in os.listdir():
    print(f"\n\n Scanning: {x}.")
    analyze_files(x)
    

