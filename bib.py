import bibtexparser
from collections import defaultdict
import re


# Define the list of names to bold
BOLD_AUTHORS = ["Wybo Houkes", "Andrea Kis", "Daniël Lakens", "Sajedeh Rasti", "Cristian Mesquida", "Vlasta Sikimić", "Krist Vaesen"]  # Add the names you want to bold here




def fix_latex_encoding(text):
    """Manually replace common LaTeX accents."""
    replacements = {
        r"{\\c{c}}": "ç",
        r"{\\'e}": "é",
        r"{\\`e}": "è",
        r"{\\o}": "ø",
        r"{\\\"u}": "ü",
        r"{\\~n}": "ñ",
        r"{\\'a}": "á",
        r"{\\'i}": "í",
        r"{\\'o}": "ó",
        r"{\\'u}": "ú"
    }
    for latex, utf in replacements.items():
        text = text.replace(latex, utf)
    return text

def format_authors(author_string):
    """Fix LaTeX encoded names and bold certain authors."""
    authors = author_string.split(" and ")
    formatted_authors = [
        f"<strong>{fix_latex_encoding(author)}</strong>" if author in BOLD_AUTHORS 
        else fix_latex_encoding(author)
        for author in authors
    ]
    return ", ".join(formatted_authors)


def parse_bib_file(bib_file):
    """Parse the .bib file and return a dictionary grouped by year."""
    with open(bib_file, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    publications = defaultdict(list)

    for entry in bib_database.entries:
        year = entry.get("year", "Unknown")
        title = entry.get("title", "No Title")
        author = entry.get("author", "Unknown Author")
        journal = entry.get("journal", "Unknown Journal")
        url = entry.get("url", "#")

        formatted_authors = format_authors(author)
        clickable_url = f'<a href="{url}" target="_blank">{url}</a>'

        publications[year].append({
            "title": title,
            "author": formatted_authors,
            "journal": journal,
            "year": year,
            "URL": clickable_url,
        })

    return dict(sorted(publications.items(), reverse=True))

def generate_html(publications):
    """Generate an HTML page for publications."""
    if not publications:
        return "<html><body><h1>No Publications Found</h1></body></html>"

    html_template = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Publications</title>
        <style>
            body { font-family: Calibri, sans-serif; }
            .year-section { margin-bottom: 2em; }
            .publication { margin-bottom: 0.5em; }
            h2 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Publications</h1>
        {content}
    </body>
    </html>"""

    content = ""
    for year, pubs in publications.items():
        content += f'<div class="year-section">\n<h2>{year}</h2>\n<ul>\n'
        for pub in pubs:
            content += (f'<li class="publication"><strong>{pub["title"]}</strong> '
                        f'by {pub["author"]}. <em>{pub["journal"]}</em> '
                        f'({pub["year"]}). {pub["URL"]}.</li>\n')
        content += "</ul>\n</div>\n"

    return html_template.replace("{content}", content)


def save_html_file(html_content, output_filename="publications.html"):
    """Save the generated HTML content to a file."""
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    bib_file = "biblio.bib"  # Update this with your .bib file path
    publications = parse_bib_file(bib_file)
    if not publications:
      print("Error: No publications were parsed from the .bib file.")
      exit()
    html_content = generate_html(publications)
    save_html_file(html_content)
    print("HTML file generated: publications.html")
