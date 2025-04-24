import pytest
import os
from rara_tools.parsers.marc_parsers.ems_parser import EMSMARCParser
from rara_tools.parsers.marc_parsers.person_parser import PersonsMARCParser
from rara_tools.parsers.marc_parsers.organization_parser import OrganizationsMARCParser
from rara_tools.parsers.marc_parsers.location_parser import LocationMARCParser


MARC_ROOT_DIR = os.path.join("tests", "test_data", "marc_records")
EMS_TEST_FILE = os.path.join(MARC_ROOT_DIR, "ems_test_subset.mrc")
PER_TEST_FILE = os.path.join(MARC_ROOT_DIR, "per_test_subset.mrc")
ORG_TEST_FILE = os.path.join(MARC_ROOT_DIR, "org_test_subset.mrc")

def test_ems_parser_without_variations():
    ems_marc_parser = EMSMARCParser(EMS_TEST_FILE, add_variations=False)
    for record in ems_marc_parser.record_generator():
        assert "keyword" in record
        assert "link_variations" not in record

def test_ems_parser_with_variations():
    ems_marc_parser = EMSMARCParser(EMS_TEST_FILE, add_variations=True)
    record_count = 0
    for record in ems_marc_parser.record_generator():
        assert "keyword" in record
        assert "link_variations" in record
        record_count+=1
    assert record_count == 10

def test_loc_parser_with_variations():
    loc_marc_parser = LocationMARCParser(EMS_TEST_FILE, add_variations=True)
    record_count = 0
    for record in loc_marc_parser.record_generator():
        assert "keyword" in record
        assert "link_variations" in record
        record_count+=1
    assert record_count == 5

def test_persons_parser_without_variations():
    per_marc_parser = PersonsMARCParser(PER_TEST_FILE, add_variations=False)
    for record in per_marc_parser.record_generator():
        assert "name" in record
        assert "link_variations" not in record


def test_organizations_parser_without_variations():
    org_marc_parser = OrganizationsMARCParser(ORG_TEST_FILE, add_variations=False)
    for record in org_marc_parser.record_generator():
        assert "name" in record
        assert "link_variations" not in record
