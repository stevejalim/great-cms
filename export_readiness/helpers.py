from urllib.parse import urljoin


def get_page_full_url(domain, full_path):
    """Urljoin quirkiness

    urljoin('http://great.gov.uk/international/', 'test/')
    http://great.gov.uk/international/test/

    urljoin('http://great.gov.uk/international', 'test/')
    http://great.gov.uk/test/

    urljoin('http://great.gov.uk/international/', '/test/')
    http://great.gov.uk/test/

    urljoin('http://great.gov.uk/international', '/test/')
    http://great.gov.uk/test/

    The first one is right!
    """

    if not domain.endswith('/'):
        domain = f'{domain}/'
    if full_path.startswith('/'):
        full_path = full_path[1:]
    url = urljoin(domain, full_path)
    return url
