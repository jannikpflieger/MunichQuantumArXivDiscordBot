import os
import xml.etree.ElementTree as ET
import list_of_proffessors as lp
import copy
from datetime import datetime, timedelta
import json

atom_folder = "./arxiv_entries/"
namespace = {"arxiv": "http://arxiv.org/schemas/atom", "atom": "http://www.w3.org/2005/Atom"}
output_file = "recent_papers.json"

# Change this value if you want a different cutoff for "recent"
seven_days_ago = datetime.now() - timedelta(days=20)

matching_papers = []
processed_ids = set()

for file_name in os.listdir(atom_folder):
    if file_name.endswith(".atom"):
        xml_file = os.path.join(atom_folder, file_name)
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for entry in root.findall("atom:entry", namespace):
            paper_id = entry.find("atom:id", namespace).text
            title = entry.find("atom:title", namespace).text
            published = entry.find("atom:published", namespace).text
            link = paper_id  # Use the ArXiv ID as the link (or extract a different link if needed)
            
            # Skip if we've already processed this paper
            if paper_id in processed_ids:
                continue

            # Parse the published date and compare with cutoff
            published_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
            if published_date < seven_days_ago:
                continue

            authors = entry.findall("atom:author/atom:name", namespace)
            author_names = [author.text for author in authors]

            # Check if any of the authors is in our list of professors
            for name in author_names:
                if name in lp.LIST_OF_PROFESSORS:
                    # Build the paper info and add it to matching_papers
                    matching_papers.append({
                        "id": paper_id,
                        "title": title,
                        "authors": author_names,
                        "publishing_date": published,
                        "link": link
                    })
                    processed_ids.add(paper_id)
                    break

# Save the results to a JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(matching_papers, file, indent=4, ensure_ascii=False)

print(f"Saved {len(matching_papers)} matching papers to {output_file}.")
