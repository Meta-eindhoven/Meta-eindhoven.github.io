import bibtexparser
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
from pylatexenc import LatexNodes2Text

# Define the list of names to bold
names_to_bold = {"Wybo Houkes", "Andrea Kis", "Daniël Lakens", "Sajedeh Rasti", "Cristian Mesquida", "Vlasta Sikimić", "Krist Vaesen"}  # Add the names you want to bold here


# Load the .bib file
def load_bib_file(filename):
    with open(filename, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries

# Convert LaTeX to Unicode
def convert_latex_to_unicode(text):
    return LatexNodes2Text().latex_to_text(text)

# Bold specific names in the author field
def bold_authors(authors):
    author_list = [name.strip() for name in authors.split(" and ")]
    bolded_authors = []
    for author in author_list:
        if author in names_to_bold:
            bolded_authors.append(f"<b>{author}</b>")
        else:
            bolded_authors.append(author)
    return ", ".join(bolded_authors)

# Process a publication entry
def process_publication(pub):
    pub["author"] = convert_latex_to_unicode(pub.get("author", "Unknown Author"))
    pub["title"] = convert_latex_to_unicode(pub.get("title", "Untitled"))
    pub["author"] = bold_authors(pub["author"])
    return pub

# Organize publications by year
def sort_publications_by_year(publications):
    sorted_publications = defaultdict(list)
    for pub in publications:
        pub = process_publication(pub)
        year = pub.get("year")
        if year:
            sorted_publications[year].append(pub)
    return dict(sorted(sorted_publications.items(), reverse=True))

# Render HTML from template
def render_html(sorted_publications, template_file, output_file):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    rendered_html = template.render(sorted_publications=sorted_publications)
    manual_content = "\n --- \n layout: page\n title: 'Publications'\n --- \n\n"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(manual_content)
        f.write(rendered_html)

# Main function
if __name__ == "__main__":
    bib_file = "biblio.bib"  # Replace with your .bib file path
    template_file = "template.html"
    output_file = "publications.html"

    # Load and sort publications
    publications = load_bib_file(bib_file)
    sorted_publications = sort_publications_by_year(publications)

    # Generate the HTML file
    render_html(sorted_publications, template_file, output_file)
    print("HTML file generated as", output_file)
