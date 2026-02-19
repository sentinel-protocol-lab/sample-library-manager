"""Tests for license key validation and Pro tool gating."""

import pytest

from sample_library_manager.tools._shared import (
    is_pro_licensed,
    require_pro,
    set_license_key,
)


class TestKeyValidation:
    """Test that key validation accepts/rejects correctly."""

    def test_none_key_not_licensed(self):
        set_license_key(None)
        assert not is_pro_licensed()

    def test_empty_string_not_licensed(self):
        set_license_key("")
        assert not is_pro_licensed()

    def test_wrong_prefix_rejected(self):
        set_license_key("WRONG-PRO-abcd1234-test")
        assert not is_pro_licensed()

    def test_too_few_parts_rejected(self):
        set_license_key("SLM-PRO")
        assert not is_pro_licensed()

    def test_three_parts_rejected(self):
        set_license_key("SLM-PRO-onlythree")
        assert not is_pro_licensed()

    def test_valid_four_parts_accepted(self):
        set_license_key("SLM-PRO-abcd1234-payload")
        assert is_pro_licensed()

    def test_valid_many_parts_accepted(self):
        set_license_key("SLM-PRO-segment1-segment2-segment3")
        assert is_pro_licensed()


class TestRequireProGating:
    """Test that require_pro returns correct messages or None."""

    def test_blocks_without_license(self):
        set_license_key(None)
        result = require_pro("analyze_sample")
        assert result is not None
        assert "Pro feature" in result

    def test_message_contains_tool_name(self):
        set_license_key(None)
        result = require_pro("analyze_sample")
        assert "analyze_sample" in result

    def test_message_contains_setup_instructions(self):
        set_license_key(None)
        result = require_pro("read_midi")
        assert "license.key" in result
        assert "SLM_LICENSE_KEY" in result

    def test_message_lists_free_tools(self):
        set_license_key(None)
        result = require_pro("sort_samples")
        assert "search_samples" in result
        assert "collect_search_results" in result

    def test_passes_with_valid_license(self):
        set_license_key("SLM-PRO-abcd1234-test")
        result = require_pro("analyze_sample")
        assert result is None

    def test_passes_for_all_pro_tools(self):
        set_license_key("SLM-PRO-abcd1234-test")
        for tool in ["analyze_sample", "read_midi", "search_samples_by_bpm",
                      "sort_samples", "rename_with_metadata"]:
            assert require_pro(tool) is None
