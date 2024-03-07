# ArXiv PDF Renamer

<img width="827" alt="image" src="https://github.com/andrewyu0/arxiv_pdf_renamer/assets/5696002/9ac04e28-cbab-4803-ac34-90a73df300b8">



## Goal
Our goal was to rename PDF files stored in the `~/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/` directory. Each file was named with its unique arXiv ID, but we aimed to rename each file using its corresponding arXiv paper title for straightforward identification.

## Approach
1. We developed a Python function `rename_pdfs()`, which:
    - Parses a list of file paths.
    - Retrieves the arXiv IDs from the names of the files.
    - Sends a HTTP request to the arXiv API to get the title of the paper associated with each arXiv ID.
    - Renames each file with its paper title within the same directory.
2. We introduced checks and error-handling to ensure smooth execution even when a file doesnt exist, the arXiv title is unavailable, or renaming fails. 

## ArXiv Title Retrieval
We accomplished this by sending an HTTP GET request to `root_url + id_list= + arxiv_id`. The `root_url` was the arXiv API URL, and our arXiv ID was appended to it. The request response held the metadata for the respective paper, which included the paper title. We extracted this title for renaming our PDF files. 

## Outcome
We passed all our PDF files within the `~/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/` directory to `rename_pdfs()`. Among these files, we successfully renamed those with a valid arXiv ID, and ignored those with no valid arXiv ID or whose arXiv ID didnt have an associated title. 

Our approach enables automatic and consistent naming of files, making it highly adaptable for similar future tasks.
