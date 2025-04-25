from lino.api import rt, _

home_children = [
    (_("Mission"), None, []),
    (_("Maxim"), None, []),
    (_("Propaganda"), None, []),
    (_("About us"), None, [
        (_("Team"), None, []),
        (_("History"), None, []),
        (_("Contact"), None, []),
        (_("Terms & conditions"), None, []),
    ]),
]


def objects():
    return rt.models.publisher.make_demo_pages(home_children)
