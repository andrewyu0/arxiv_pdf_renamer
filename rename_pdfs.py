import os
import requests
import xml.etree.ElementTree as ET
import glob
import re
import traceback


root_url = "http://export.arxiv.org/api/query?"
namespaces = {"atom": "http://www.w3.org/2005/Atom"}

def rename_pdfs(file_paths):
    new_names = []
    success_counter = 0
    skip_counter = 0

    def sanitize_title(title):
        return re.sub("[\\/:*?\"<>|]", "_", title)

    for file in file_paths:
        try:
            expanded_file_path = os.path.expanduser(file)
            file_name_without_extension = os.path.basename(expanded_file_path).split(".pdf")[0]
            arxiv_id = file_name_without_extension.split("v")[0]
            if arxiv_id.isdigit() and len(arxiv_id) in [8, 9]:
                if len(arxiv_id) == 8:
                    arxiv_id = arxiv_id[:4] + "." + arxiv_id[4:]
                elif len(arxiv_id) == 9:
                    arxiv_id = arxiv_id[:4] + "." + arxiv_id[4:]
                response = requests.get(root_url + "id_list=" + arxiv_id)
                root = ET.fromstring(response.content)
                title_element = root.find("atom:entry/atom:title", namespaces)
                if title_element is not None and title_element.text.lower() != "error":
                    title = title_element.text
                    print(f"File: {expanded_file_path}, Title: {title}")
                    sanitized_title = sanitize_title(" ".join(title.split()))
                    new_file_name = os.path.join(os.path.dirname(expanded_file_path), sanitized_title + ".pdf")
                    try:
                        os.rename(expanded_file_path, new_file_name)
                        new_names.append(new_file_name)
                        print("Renaming successful")
                        success_counter += 1
                    except Exception as ex:
                        print(f"Error renaming : {ex}")
                else:
                    print(f"Skipped file (no valid title found): {expanded_file_path}")
                    skip_counter += 1
            else:
                print("Skipping non-ArXiv file: " + expanded_file_path)
        except Exception as e:
            print(f"Error occurred: {e}")
            print(traceback.format_exc())

    print(f"Successful renames: {success_counter}")
    print(f"Skipped files: {skip_counter}")
    return new_names

all_pdf_files = glob.glob(os.path.expanduser("~/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/*.pdf"))
rename_pdfs(all_pdf_files)
