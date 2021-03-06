"""test_level3_dithers: Test of dither rules."""
from __future__ import absolute_import
import pytest

from .helpers import (
    level3_rule_path,
    mkstemp_pool_file,
    t_path,
)

from ..main import Main

@pytest.mark.parametrize(
    "partial_args, n_asns",
    [
        # Invalid ACID
        (
            ['-i', 'nosuchid'],
            0
        ),
        # Basic observation ACIDs
        (
            ['-i', 'o001'],
            2
        ),
        (
            ['-i', 'o002'],
            2
        ),
        # Specifying multiple ACIDs
        (
            ['-i', 'o001', 'o002'],
            4
        ),
        # Candidate ID's
        (
            ['-i', 'c1000'],
            2
        ),
        (
            ['-i', 'c1000', 'c1001'],
            4
        ),
        # Whole program
        (
            [],
            20
        ),
        # Discovered only
        (
            ['--discover'],
            0
        ),
    ]
)
def test_candidate_observation(partial_args, n_asns):
    with mkstemp_pool_file(t_path('data/pool_001_candidates.csv')) as pool_path:
        cmd_args = [
            pool_path,
            '--dry-run',
            '-r', level3_rule_path(),
            '--ignore-default',
        ]
        cmd_args.extend(partial_args)
        generated = Main(cmd_args)
        assert len(generated.associations) == n_asns
