from bs4 import BeautifulSoup

def generate_html_from_string(html_string,out="log/log.html"):
    soup = BeautifulSoup(html_string, "html.parser")
    with open(out,"w",encoding="utf-8") as f:
        f.write(str(soup.prettify()))