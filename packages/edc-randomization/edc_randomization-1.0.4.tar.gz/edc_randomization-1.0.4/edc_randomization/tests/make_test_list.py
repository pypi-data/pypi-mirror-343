import csv
import random
from pathlib import Path
from tempfile import mkdtemp

from ..constants import ACTIVE, PLACEBO

default_assignments = [ACTIVE, PLACEBO]


def make_test_list(
    full_path: Path | str = None,
    assignments=None,
    site_names=None,
    count=None,
    first_sid=None,
    per_site=None,
) -> Path:
    first_sid = first_sid or 0
    if per_site:
        site_names = site_names * per_site
        count = len(site_names)
        gen_site_name = (x for x in site_names)
    else:
        count = count or 50
        gen_site_name = (random.choice(site_names) for i in range(0, 50))  # nosec B311

    if not full_path:
        full_path = Path(mkdtemp()) / "randomizationlist.csv"
    else:
        full_path = Path(full_path).expanduser()
    assignments = assignments or default_assignments
    with full_path.open(mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=["sid", "assignment", "site_name"])
        writer.writeheader()
        n = 0
        for i in range(first_sid, count + first_sid):
            n += 1
            assignment = random.choice(assignments)  # nosec B311
            writer.writerow(dict(sid=i, assignment=assignment, site_name=next(gen_site_name)))
    return full_path
