import itertools
from typing import Any, Dict, List

import pytest

import great_expectations.expectations as gxe
from great_expectations.compatibility import pydantic
from great_expectations.exceptions import InvalidExpectationConfigurationError
from great_expectations.expectations import expectation
from great_expectations.expectations.expectation_configuration import (
    ExpectationConfiguration,
)
from great_expectations.validator.metric_configuration import MetricConfiguration


class FakeMulticolumnExpectation(expectation.MulticolumnMapExpectation):
    map_metric = "fake_multicol_metric"


class FakeColumnMapExpectation(expectation.ColumnMapExpectation):
    map_metric = "fake_col_metric"


class FakeColumnPairMapExpectation(expectation.ColumnPairMapExpectation):
    map_metric = "fake_pair_metric"


@pytest.fixture
def metrics_dict():
    """
    Fixture for metrics dict, which represents Metrics already calculated for given Batch
    """
    return {
        (
            "column_values.nonnull.unexpected_count",
            "e197e9d84e4f8aa077b8dd5f9042b382",
            (),
        ): "i_exist"
    }


def fake_metrics_config_list(
    metric_name: str, metric_domain_kwargs: Dict[str, Any]
) -> List[MetricConfiguration]:
    """
    Helper method to generate list of MetricConfiguration objects for tests.
    """
    return [
        MetricConfiguration(
            metric_name=metric_name,
            metric_domain_kwargs=metric_domain_kwargs,
            metric_value_kwargs={},
        )
    ]


def fake_expectation_config(
    expectation_type: str, config_kwargs: Dict[str, Any]
) -> ExpectationConfiguration:
    """
    Helper method to generate of ExpectationConfiguration objects for tests.
    """
    return ExpectationConfiguration(
        expectation_type=expectation_type,
        kwargs=config_kwargs,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "fake_expectation_cls, config",
    [
        (
            FakeMulticolumnExpectation,
            fake_expectation_config(
                "fake_multicolumn_expectation", {"column_list": []}
            ),
        ),
        (
            FakeColumnMapExpectation,
            fake_expectation_config("fake_column_map_expectation", {"column": "col"}),
        ),
        (
            FakeColumnPairMapExpectation,
            fake_expectation_config(
                "fake_column_pair_map_expectation",
                {"column_A": "colA", "column_B": "colB"},
            ),
        ),
    ],
)
def test_multicolumn_expectation_has_default_mostly(fake_expectation_cls, config):
    try:
        fake_expectation = fake_expectation_cls(**config.kwargs)
    except Exception:
        assert (
            False
        ), "Validate configuration threw an error when testing default mostly value"
    assert (
        fake_expectation._get_success_kwargs().get("mostly") == 1
    ), "Default mostly success ratio is not 1"


@pytest.mark.unit
@pytest.mark.parametrize(
    "fake_expectation_cls, config",
    itertools.chain(
        *[
            [
                (
                    FakeMulticolumnExpectation,
                    fake_expectation_config(
                        "fake_multicolumn_expectation", {"column_list": [], "mostly": x}
                    ),
                )
                for x in [0, 0.5, 1]
            ],
            [
                (
                    FakeColumnMapExpectation,
                    fake_expectation_config(
                        "fake_column_map_expectation", {"column": "col", "mostly": x}
                    ),
                )
                for x in [0, 0.5, 1]
            ],
            [
                (
                    FakeColumnPairMapExpectation,
                    fake_expectation_config(
                        "fake_column_pair_map_expectation",
                        {"column_A": "colA", "column_B": "colB", "mostly": x},
                    ),
                )
                for x in [0, 0.5, 1]
            ],
        ]
    ),
)
def test_expectation_succeeds_with_valid_mostly(fake_expectation_cls, config):
    fake_expectation = fake_expectation_cls(**config.kwargs)
    assert (
        fake_expectation._get_success_kwargs().get("mostly") == config.kwargs["mostly"]
    ), "Default mostly success ratio is not 1"


@pytest.mark.unit
@pytest.mark.parametrize(
    "fake_expectation_cls, config",
    [
        (
            FakeMulticolumnExpectation,
            fake_expectation_config(
                "fake_multicolumn_expectation", {"column_list": [], "mostly": -0.5}
            ),
        ),
        (
            FakeColumnMapExpectation,
            fake_expectation_config(
                "fake_column_map_expectation", {"column": "col", "mostly": 1.5}
            ),
        ),
        (
            FakeColumnPairMapExpectation,
            fake_expectation_config(
                "fake_column_pair_map_expectation",
                {"column_A": "colA", "column_B": "colB", "mostly": -1},
            ),
        ),
    ],
)
def test_multicolumn_expectation_validation_errors_with_bad_mostly(
    fake_expectation_cls, config
):
    with pytest.raises(pydantic.ValidationError):
        fake_expectation_cls(**config)


@pytest.mark.unit
def test_validate_dependencies_against_available_metrics_success(metrics_dict):
    metric_config_list: List[MetricConfiguration] = fake_metrics_config_list(
        metric_name="column_values.nonnull.unexpected_count",
        metric_domain_kwargs={
            "batch_id": "projects-projects",
            "column": "i_exist",
        },
    )
    expectation._validate_dependencies_against_available_metrics(
        validation_dependencies=metric_config_list,
        metrics=metrics_dict,
    )


@pytest.mark.unit
def test_validate_dependencies_against_available_metrics_failure(metrics_dict):
    metric_config_list: List[MetricConfiguration] = fake_metrics_config_list(
        metric_name="column_values.nonnull.unexpected_count",
        metric_domain_kwargs={
            "batch_id": "projects-projects",
            "column": "i_dont_exist",
        },
    )
    with pytest.raises(InvalidExpectationConfigurationError):
        expectation._validate_dependencies_against_available_metrics(
            validation_dependencies=metric_config_list,
            metrics=metrics_dict,
        )


@pytest.mark.unit
def test_expectation_configuration_property():
    expectation = gxe.ExpectColumnMaxToBeBetween(
        column="foo", min_value=0, max_value=10
    )

    assert expectation.configuration == ExpectationConfiguration(
        expectation_type="expect_column_max_to_be_between",
        kwargs={
            "column": "foo",
            "min_value": 0,
            "max_value": 10,
        },
    )


@pytest.mark.unit
def test_expectation_configuration_property_recognizes_state_changes():
    expectation = gxe.ExpectColumnMaxToBeBetween(
        column="foo", min_value=0, max_value=10
    )

    expectation.column = "bar"
    expectation.min_value = 5
    expectation.max_value = 15
    expectation.mostly = 0.95

    assert expectation.configuration == ExpectationConfiguration(
        expectation_type="expect_column_max_to_be_between",
        kwargs={
            "column": "bar",
            "mostly": 0.95,
            "min_value": 5,
            "max_value": 15,
        },
    )


@pytest.mark.unit
def test_unrecognized_expectation_arg_raises_error():
    with pytest.raises(pydantic.ValidationError, match="extra fields not permitted"):
        gxe.ExpectColumnMaxToBeBetween(
            column="foo", min_value=0, max_value=10, mostyl=0.95  # 'mostly' typo
        )
