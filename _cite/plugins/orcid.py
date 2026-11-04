import json
from urllib.request import Request, urlopen
from util import *
from retrieval import normalize_identifier, orcid_metadata


def main(entry):
    """Expand ORCID works while retaining identifiers and fallback metadata."""
    orcid = get_safe(entry, "orcid", "")
    if not orcid:
        raise Exception('No "orcid" key')

    @log_cache
    @cache.memoize(name=__file__, expire=1 * (60 * 60 * 24))
    def query(_id):
        request = Request(
            url=f"https://pub.orcid.org/v3.0/{_id}/works",
            headers={"Accept": "application/json"},
        )
        with urlopen(request, timeout=30) as response:
            return get_safe(json.load(response), "group", [])

    sources = []
    for work in query(orcid):
        summaries = get_safe(work, "work-summary", [])
        if not summaries:
            continue
        identifiers = []
        all_identifiers = []
        for summary in summaries:
            for external in get_safe(summary, "external-ids.external-id", []) or []:
                identifier = normalize_identifier(
                    get_safe(external, "external-id-type", ""),
                    get_safe(external, "external-id-value", ""),
                )
                if not identifier:
                    continue
                if identifier not in all_identifiers:
                    all_identifiers.append(identifier)
                # Containing journals/books and other versions aren't this work.
                if external.get("external-id-relationship") == "self" and identifier not in identifiers:
                    identifiers.append(identifier)

        # Stable work IDs prevent unrelated papers sharing an ISSN from merging.
        put_code = summaries[0].get("put-code")
        source_id = f"orcid:{orcid}/work/{put_code}"
        for prefix in ["doi:", "pubmed:", "pmc:"]:
            match = next((identifier for identifier in identifiers if identifier.startswith(prefix)), None)
            if match:
                source_id = match
                break
        metadata = {}
        # Fill missing fields from other summaries, preserving the preferred one.
        for summary in reversed(summaries):
            metadata.update(orcid_metadata(summary))
        source = {
            "id": source_id,
            "_orcid": [{
                "orcid": orcid, "put-code": put_code,
                "identifiers": identifiers, "all-identifiers": all_identifiers,
                "metadata": metadata,
            }],
        }
        source.update(entry)
        sources.append(source)
    return sources
