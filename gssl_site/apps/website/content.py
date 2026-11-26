"""
Project content, as data.

The design build shipped one project-detail page holding Phase 1's sample
content, and every project card pointed at it - so Phase 2, Phase 3 and the
rest all opened Phase 1. Each project now has its own entry here and its own
URL, and everything the page says about a project - heading, description,
badge, programme, Gold Standard status - comes from its row.

This is still static: no database, no migrations. It is deliberately shaped
like the Project model that the admin panel will introduce, so moving to the
CMS means swapping the source of these rows, not rewriting templates.

Every sentence below is copy that was already on the site (the programme
pages, the project cards, the Phase 1 page). Nothing here is new fact; replace
the descriptions with GSSL's own per-project copy when it arrives.
"""

from dataclasses import dataclass

# Shared paragraphs, reused verbatim from the existing pages.
COOKSTOVE_INTRO = (
    "One of our key initiatives is developing and distributing improved cookstoves in "
    "Bangladesh. Traditional cooking methods carry serious health and environmental risks. "
    "After listening to households’ concerns about the improved cookstoves already on the "
    "market, we designed the Green ICS around local knowledge and ease of use."
)
GOLD_STANDARD_MONITORING = (
    "The project is registered with Gold Standard. Our monitoring team visits households to "
    "check that stoves are in use and in good condition, and keeps a clear record for "
    "independent verification."
)

# programme key -> (URL name of the programme page, label)
PROGRAMMES = {
    "cookstove": ("programme_improved_cookstove", "Improved Cookstove Programme"),
    "rooftop": ("programme_rooftop_solar", "Rooftop Solar MRV"),
}

# First filter chip -> badge style on project cards.
BADGE_CLASSES = {
    "registered": "badge--registered",
    "development": "badge--development",
    "active": "badge--active",
    "certification": "badge--certification",
}


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    summary: str
    location: str
    stage: str
    photo: str                      # img/photos/<photo>-<size>.<ext>
    programme: str = ""             # key into PROGRAMMES; also the accent colour hook
    gs_id: str = ""                 # Gold Standard registry id, only when registered
    standard: str = ""              # what to show in the Standard row
    filters: tuple[str, ...] = ()   # chips on the projects grid
    proponent: str = "Green Spark Solutions Australia Pty Ltd"
    status_label: str = "Status"    # label of the last Key details row
    status_note: str = ""           # value of that row
    card_badge: str = ""            # badge on cards when there is no GS registration
    description: tuple[str, ...] = ()  # "About the project" paragraphs
    stove_detail: bool = False      # show the Green ICS attributes, how-it-works and field photos

    @property
    def programme_url_name(self) -> str:
        return "website:" + PROGRAMMES[self.programme][0]

    @property
    def programme_label(self) -> str:
        return PROGRAMMES[self.programme][1]

    @property
    def badge_class(self) -> str:
        return BADGE_CLASSES.get(self.filters[0] if self.filters else "", "badge--type")

    @property
    def is_registered(self) -> bool:
        return bool(self.gs_id)


PROJECTS: tuple[Project, ...] = (
    Project(
        slug="rooftop-solar-mrv",
        title="Rooftop Solar MRV",
        summary="Rooftop solar systems on homes and businesses brought together as one carbon "
                "programme, measured, reported and verified so more owners can take part.",
        location="Bangladesh",
        stage="In development",
        photo="rooftop-solar",
        programme="rooftop",
        standard="Gold Standard (in preparation)",
        filters=("development", "rooftop"),
        status_note="Aggregation in development",
        card_badge="In development",
        description=(
            "Bringing rooftop solar systems together into one carbon programme, so more owners "
            "can take part. Generation is measured, reported and verified, so every result can "
            "be checked.",
            "The programme is at an early stage. We are working with communities, local "
            "government and technical partners to shape it, and will publish more detail as it "
            "develops.",
        ),
    ),
    Project(
        slug="green-ics-phase-1",
        title="Green ICS — Phase 1",
        summary="The first phase of our improved cookstove programme: stoves installed with "
                "households who cook with firewood and biomass.",
        location="Manikganj and neighbouring districts, Bangladesh",
        stage="Installed · monitoring",
        photo="ics-phase-1",
        programme="cookstove",
        gs_id="GS13141",
        standard="Gold Standard (registered)",
        filters=("registered", "cookstove"),
        status_label="Stove installation",
        status_note="Ongoing — temporarily paused",
        description=(
            COOKSTOVE_INTRO,
            "Phase 1 brought the Green ICS to households in Manikganj and neighbouring "
            "districts. Each stove was installed by a trained field officer, who showed the "
            "family how to use and look after it.",
            GOLD_STANDARD_MONITORING,
        ),
        stove_detail=True,
    ),
    Project(
        slug="green-ics-phase-2",
        title="Green ICS — Phase 2",
        summary="Expanding the programme to more households, with the same design, training "
                "and monitoring as Phase 1.",
        location="Dhaka and Rajshahi divisions, Bangladesh",
        stage="Installation in progress",
        photo="ics-phase-2",
        programme="cookstove",
        gs_id="GS23304",
        standard="Gold Standard (registered)",
        filters=("registered", "cookstove"),
        status_label="Stove installation",
        status_note="Installation in progress",
        description=(
            COOKSTOVE_INTRO,
            "Phase 2 expands the programme to more households, with the same design, training "
            "and monitoring as Phase 1.",
            GOLD_STANDARD_MONITORING,
        ),
        stove_detail=True,
    ),
    Project(
        slug="green-ics-phase-3",
        title="Green ICS — Phase 3",
        summary="The next phase of the programme is in preparation. Details will be published "
                "once it is registered.",
        location="Bangladesh",
        stage="Pipeline",
        photo="ics-phase-3",
        programme="cookstove",
        standard="Gold Standard (to be submitted)",
        filters=("development", "cookstove"),
        status_label="Stove installation",
        status_note="In preparation",
        card_badge="In pipeline",
        description=(
            COOKSTOVE_INTRO,
            "The next phase of the programme is in preparation. Details will be published once "
            "it is registered.",
        ),
    ),
    Project(
        slug="community-monitoring",
        title="Community monitoring and maintenance",
        summary="Field officers visit households, check stoves, replace parts and record use "
                "for the monitoring report.",
        location="All programme districts",
        stage="Ongoing",
        photo="monitoring",
        programme="cookstove",
        standard="Supports the registered Green ICS phases",
        filters=("active", "cookstove"),
        status_note="Ongoing",
        card_badge="Active",
        description=(
            COOKSTOVE_INTRO,
            "Field officers visit households, check stoves, replace parts and record use for "
            "the monitoring report.",
        ),
        stove_detail=True,
    ),
    Project(
        slug="stove-design-and-manufacturing",
        title="Stove design and local manufacturing",
        summary="Improving the Green ICS with feedback from households and producing parts "
                "with local makers.",
        location="Manikganj, Bangladesh",
        stage="Ongoing",
        photo="stove-manufacturing",
        programme="cookstove",
        standard="Supports the registered Green ICS phases",
        filters=("active", "cookstove"),
        status_note="Ongoing",
        card_badge="Active",
        description=(
            COOKSTOVE_INTRO,
            "We keep improving the Green ICS with feedback from households, and produce parts "
            "with local makers.",
        ),
        stove_detail=True,
    ),
    Project(
        slug="clean-cooking-scoping-nepal",
        title="Clean cooking scoping — Nepal",
        summary="Early work to understand how the programme could serve households in Nepal.",
        location="Nepal",
        stage="Scoping",
        photo="nepal-scoping",
        programme="cookstove",
        standard="Standard to be confirmed",
        filters=("certification", "cookstove"),
        status_note="Scoping",
        card_badge="Scoping",
        description=(
            "Early work to understand how the programme could serve households in Nepal. "
            "Details will be published as the work develops.",
        ),
    ),
)

PROJECTS_BY_SLUG = {p.slug: p for p in PROJECTS}


def related_projects(project: Project, count: int = 3) -> list[Project]:
    """Other projects, same programme first, in site order."""
    others = [p for p in PROJECTS if p.slug != project.slug]
    others.sort(key=lambda p: p.programme != project.programme)  # stable sort keeps order
    return others[:count]
