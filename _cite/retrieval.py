"""Retrieve ORCID works with validated identifier fallbacks."""

import json
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from util import (
    cache, citation_from_csl, cite_with_manubot, format_date, get_safe,
    log, log_cache, validate_citation,
)


def normalize_identifier(kind, value):
    """Normalize supported identifiers without changing unrelated identifiers."""
    kind = kind.lower().strip()
    kind = {"pmid": "pubmed", "pmcid": "pmc"}.get(kind, kind)
    value = str(value or "").strip()
    if kind == "doi":
        value = "".join(value.split()).lower()
        for prefix in ["https://doi.org/", "http://doi.org/", "doi:"]:
            if value.startswith(prefix):
                value = value[len(prefix):]
                break
    elif kind in ["pubmed", "pmc"]:
        value = "".join(value.split())
        if kind == "pmc":
            value = value.upper()
            if not value.startswith("PMC"):
                value = "PMC" + value
    return f"{kind}:{value}" if value else ""


def read_json(url):
    request = Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "picsl-website-citations (https://picsl.upenn.edu)",
    })
    with urlopen(request, timeout=30) as response:
        return json.load(response)


@log_cache
@cache.memoize(name="crossref-v1", expire=90 * (60 * 60 * 24))
def cite_with_crossref(doi):
    """Use Crossref's structured DOI record, bypassing publisher scraping."""
    response = read_json("https://api.crossref.org/works/" + quote(doi, safe=""))
    work = response["message"]
    if normalize_identifier("doi", work.get("DOI")) != f"doi:{doi}":
        raise ValueError("Crossref returned a different DOI")

    def first_text(value):
        return (value[0] if value else "") if isinstance(value, list) else value or ""

    csl = dict(work)
    csl["title"] = first_text(work.get("title"))
    csl["container-title"] = first_text(work.get("container-title"))
    csl["issued"] = work.get("published") or work.get("issued") or {}
    csl["URL"] = f"https://doi.org/{doi}"
    citation = citation_from_csl(f"doi:{doi}", csl)
    validate_citation(citation)
    return citation


@log_cache
@cache.memoize(name="pmcid-doi-v1", expire=90 * (60 * 60 * 24))
def doi_from_pmcid(pmcid):
    """Crossref accepts DOIs, so resolve a PMCID through NCBI first."""
    params = urlencode({
        "ids": pmcid, "idtype": "pmcid", "format": "json",
        "tool": "picsl-website-citations",
    })
    response = read_json("https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?" + params)
    for record in response.get("records", []):
        if record.get("pmcid", "").upper() == pmcid.upper() and record.get("doi"):
            return normalize_identifier("doi", record["doi"]).split(":", 1)[1]
    raise ValueError(f"No DOI found for {pmcid}")


def orcid_metadata(work):
    """Keep ORCID metadata, using publication dates rather than edit timestamps."""
    citation = {}
    for field, path in [
        ("title", "title.title.value"), ("publisher", "journal-title.value"),
        ("link", "url.value"),
    ]:
        value = get_safe(work, path)
        if value:
            citation[field] = value
    year = get_safe(work, "publication-date.year.value")
    if year:
        month = get_safe(work, "publication-date.month.value") or "1"
        day = get_safe(work, "publication-date.day.value") or "1"
        try:
            citation["date"] = format_date(f"{int(year):04d}-{int(month):02d}-{int(day):02d}")
        except (TypeError, ValueError):
            pass
    authors = [
        get_safe(contributor, "credit-name.value", "")
        for contributor in get_safe(work, "contributors.contributor", []) or []
    ]
    if any(authors):
        citation["authors"] = [author for author in authors if author]
    return citation


@log_cache
@cache.memoize(name="orcid-work-v1", expire=1 * (60 * 60 * 24))
def read_orcid_work(orcid, put_code):
    return read_json(f"https://pub.orcid.org/v3.0/{quote(orcid, safe='')}/work/{quote(str(put_code), safe='')}")


def cite_orcid(contexts):
    """Return (metadata, needs_review) using the requested five-stage sequence."""
    identifiers = list(dict.fromkeys(
        identifier for context in contexts for identifier in context["identifiers"]
    ))
    dois = [value.split(":", 1)[1] for value in identifiers if value.startswith("doi:")]
    pmids = [value for value in identifiers if value.startswith("pubmed:")]
    pmcids = [value.split(":", 1)[1] for value in identifiers if value.startswith("pmc:")]

    def attempt(description, retrieve):
        log(description, indent=1)
        try:
            citation = retrieve()
            validate_citation(citation)
            return citation
        except Exception as error:
            log(f"{description} failed: {error}", indent=2, level="WARNING")
            return None

    for identifier in [f"doi:{doi}" for doi in dois] + pmids:
        citation = attempt(f"Manubot {identifier}", lambda: cite_with_manubot(identifier))
        if citation is not None:
            return citation, False
    for doi in dois:
        citation = attempt(f"Crossref doi:{doi}", lambda: cite_with_crossref(doi))
        if citation is not None:
            return citation, False
    for pmcid in pmcids:
        citation = attempt(
            f"Crossref via pmc:{pmcid}", lambda: cite_with_crossref(doi_from_pmcid(pmcid))
        )
        if citation is not None:
            return citation, False

    # Prefer the latest context, matching existing source override precedence.
    context = contexts[-1]
    citation = context["metadata"].copy()
    if context.get("put-code") is not None:
        try:
            details = read_orcid_work(context["orcid"], context["put-code"])
            citation.update(orcid_metadata(details))
        except Exception as error:
            log(f"Could not retrieve full ORCID work: {error}", indent=2, level="WARNING")
    return citation, True
