import bibtexparser
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict

# Load the .bib file
def load_bib_file(filename):
    with open(filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database.entries

# Organize publications by year
def sort_publications_by_year(publications):
    sorted_publications = defaultdict(list)
    for pub in publications:
        year = pub.get("year")
        if year:
            sorted_publications[year].append(pub)
    return dict(sorted(sorted_publications.items(), reverse=True))

# Render HTML from template
def render_html(sorted_publications, template_file, output_file):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    rendered_html = template.render(sorted_publications=sorted_publications)
    with open(output_file, "w") as f:
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
