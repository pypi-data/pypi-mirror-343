# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:52:27 2023

@author: pkiefer
"""

from src.tadamz import processing_steps as ps
from src.tadamz import in_out
import pytest
import os

here = os.path.abspath(os.path.dirname(__file__))
data_folder = os.path.join(here, "data")


@pytest.fixture
def result_post():
    path = os.path.join(data_folder, "test_processing_steps_changed_rows.table")
    return in_out.load_twf_table(path)


@pytest.fixture
def config_srm():
    path = os.path.join(data_folder, "test_mrm_config.txt")
    return in_out.load_config(path)


@pytest.fixture
def kwargs():
    return {"ms_data_type": "MS_Chromatogram"}


@pytest.fixture
def kwargs1():
    return {"ms_data_type": "Spectra"}


def test_extract_track_changes_0(result_post, config_srm):
    t, _ = ps.extract_track_changes(result_post, config_srm, True)
    is_ = set(t.row_id)
    expected = {35, 36, 37, 38, 4159, 4160, 4161, 4162, 4163}
    assert is_ - expected == expected - is_


def test_extract_track_changes_1(result_post, config_srm):
    _, is_ = ps.extract_track_changes(result_post, config_srm, False)
    assert is_ is None


def test_postprocess_0(result_post, config_srm):
    pr_all = ps.PostProcessResult(result_post, config_srm)
    pr_sub = ps.PostProcessResult(
        result_post, config_srm, process_only_tracked_changes=True
    )
    pr_all.normalize_peaks()
    pr_sub.normalize_peaks()
    pr_sub.merge_reprocessed()
    # print(pr_sub.result)
    # print(pr_all.result)
    is_ = dict(zip(pr_sub.result.row_id, pr_sub.result.normalized_area_chromatogram))
    exp = dict(zip(pr_all.result.row_id, pr_all.result.normalized_area_chromatogram))
    print(is_)
    print(exp)
    exp = dict(zip(pr_all.result.row_id, pr_all.result.normalized_area_chromatogram))

    def _comp(v1, v2):
        if v1 is None and v2 is None:
            return True
        return abs(v1 - v2) / v2 < 1e-16

    assert all([_comp(is_[key], exp[key]) for key in exp.keys()])


def test_postprocess_1(result_post, config_srm):
    exp = dict(zip(result_post.row_id, result_post.normalized_area_chromatogram))
    result_post.meta_data["tracked_change"] = {}
    result_post.meta_data["changed_rows"] = set()
    pr_sub = ps.PostProcessResult(
        result_post, config_srm, process_only_tracked_changes=True
    )
    pr_sub.normalize_peaks()
    pr_sub.merge_reprocessed()
    # print(pr_sub.result)
    # print(pr_all.result)
    is_ = dict(zip(pr_sub.result.row_id, pr_sub.result.normalized_area_chromatogram))
    print(is_)
    print(exp)

    def _comp(v1, v2):
        if v1 is None and v2 is None:
            return True
        return abs(v1 - v2) / v2 < 1e-16

    assert all([_comp(is_[key], exp[key]) for key in exp.keys()])
