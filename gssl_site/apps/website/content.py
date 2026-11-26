"""
Project content, as data.

The design build shipped one project-detail page holding Phase 1's sample
content, and every project card pointed at it - so Phase 2, Phase 3 and the
rest all opened Phase 1. Each project now has its own entry here and its own
URL.

This is still static: no database, no migrations. It is deliberately shaped
like the Project model that the admin panel will introduce, so moving to the
CMS means swapping the source of these rows, not rewriting templates.

Fields marked "to confirm" carry what the project cards already stated. The
longer narrative on each page is shared until GSSL supplies per-project copy.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    summary: str
    location: str
    stage: str
    photo: str                      # img/photos/<photo>-<size>.<ext>
    programme: str = ""             # data-programme hook for the accent colour
    gs_id: str = ""                 # Gold Standard registry id, when registered
    standard: str = ""              # what to show in the Standard row
    filters: tuple[str, ...] = ()   # chips on the projects grid
    proponent: str = "Green Spark Solutions Australia Pty Ltd"
    status_note: str = ""           # replaces a headline figure where there is none


PROJECTS: tuple[Project, ...] = (
    Project(
        slug="rooftop-solar-mrv",
        title="Rooftop Solar MRV",
        summary="Rooftop solar systems on homes and businesses brought together as one "
                "carbon programme, measured, reported and verified so more owners can take part.",
        location="Bangladesh",
        stage="In development",
        photo="rooftop-solar",
        programme="rooftop",
        standard="Gold Standard (in preparation)",
        filters=("development", "rooftop"),
        status_note="Aggregation in development",
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
        status_note="Ongoing — temporarily paused",
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
        status_note="Installation in progress",
    ),
    Project(
        slug="green-ics-phase-3",
        title="Green ICS — Phase 3",
        summary="The next phase of the programme is in preparation. Details will be published "
                "once it is registered.",
        location="Bangladesh (districts to confirm)",
        stage="Pipeline",
        photo="ics-phase-3",
        programme="cookstove",
        standard="Gold Standard (to be submitted)",
        filters=("development", "cookstove"),
        status_note="In preparation",
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
    ),
)

PROJECTS_BY_SLUG = {p.slug: p for p in PROJECTS}
