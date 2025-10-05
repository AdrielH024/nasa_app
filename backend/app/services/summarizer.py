from typing import List, Dict


async def get_article_summaries(tag: str) -> List[Dict[str, str]]:
    """Return summarized NASA article data for a given tag.

    Replace the body with your real service call. Keep the same return shape.
    """
    return [
        {
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity, osteocytic osteolysis, and osteoblastic cell cycle inhibition by CDKN1a/p21",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3630201/",
            "summary_for_dummies": (
                "Imagine your bones are like a brick wall constantly remodeled. In microgravity, "
                "osteoclasts (demolition) overwork while osteoblasts (construction) slow down, and "
                "osteocytes carve spaces, causing rapid pelvic bone loss."
            ),
        },
        {
            "title": "Dose- and Ion-Dependent Effects in the Oxidative Stress Response to Space-Like Radiation Exposure in the Skeletal System",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5666799/",
            "summary_for_dummies": (
                "Space radiation varies by particle and dose. High doses, especially heavy ions like iron, "
                "damage bone and impair marrow's ability to produce bone-forming cells; lighter doses have lesser effects."
            ),
        },
    ]
