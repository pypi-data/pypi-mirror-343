#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from itertools import chain
from os import linesep
from typing import Any

from torch.nn import Module

from lightly_train._models.custom.custom_package import CUSTOM_PACKAGE
from lightly_train._models.feature_extractor import FeatureExtractor
from lightly_train._models.package import Package
from lightly_train._models.rfdetr.rfdetr_package import RFDETR_PACKAGE
from lightly_train._models.super_gradients.super_gradients_package import (
    SUPER_GRADIENTS_PACKAGE,
)
from lightly_train._models.timm.timm_package import TIMM_PACKAGE
from lightly_train._models.torchvision.torchvision_package import TORCHVISION_PACKAGE
from lightly_train._models.ultralytics.ultralytics_package import ULTRALYTICS_PACKAGE
from lightly_train.errors import UnknownModelError


def list_packages() -> list[Package]:
    """Lists all supported packages."""
    return [
        RFDETR_PACKAGE,
        SUPER_GRADIENTS_PACKAGE,
        TIMM_PACKAGE,
        TORCHVISION_PACKAGE,
        ULTRALYTICS_PACKAGE,
        # Custom package must be at end of list because we first want to check if a
        # model is part of one of the other packages. Custom is the last resort.
        CUSTOM_PACKAGE,
    ]


def get_package(package_name: str) -> Package:
    """Get a package by name."""
    # Don't include custom package. It should never be fetched by name.
    packages = {p.name: p for p in list_packages()}
    try:
        return packages[package_name]
    except KeyError:
        raise ValueError(
            f"Unknown package name: '{package_name}'. Supported packages are "
            f"{list(packages)}."
        )


def list_model_names() -> list[str]:
    """Lists all models in ``<package_name>/<model_name>`` format.

    See the documentation for more information: https://docs.lightly.ai/train/stable/models/
    """
    return sorted(chain.from_iterable(p.list_model_names() for p in list_packages()))


def get_model(model: str | Module, model_args: dict[str, Any] | None = None) -> Module:
    """Returns a model instance given a model name or instance."""
    if isinstance(model, Module):
        return model

    package_name, model_name = _parse_model_name(model=model)
    package = get_package(package_name=package_name)
    return package.get_model(model_name, model_args)


def get_feature_extractor(model: Module) -> FeatureExtractor:
    """Returns a feature extractor class for the given model."""
    for package in list_packages():
        if package.is_supported_model(model):
            return package.get_feature_extractor(model)

    raise UnknownModelError(f"Unknown model: '{model.__class__.__name__}'")


def get_package_from_model(model: Module) -> Package:
    """Returns the package of the model. If the model is not part of any package,
    the custom package is returned."""
    for package in list_packages():
        if package.is_supported_model(model):
            return package

    raise UnknownModelError(f"Unknown model: '{model.__class__.__name__}'")


def _parse_model_name(model: str) -> tuple[str, str]:
    parts = model.split("/")
    if len(parts) != 2:
        raise ValueError(
            "Model name has incorrect format. Should be 'package/model' but is "
            f"'{model}'"
        )
    package_name = parts[0]
    model_name = parts[1]
    return package_name, model_name


def format_log_msg_model_usage_example(log_message_code_block: list[str]) -> str:
    log_message_header = (
        f"Example: How to use the exported model{linesep}{'-' * 88}{linesep}"
    )

    log_message_footer = f"{'-' * 88}{linesep}"

    def format_code_lines(lines: list[str]) -> str:
        str_out = ""
        for line in lines:
            str_out += f"{line}{linesep}"
        return str_out

    log_message = (
        log_message_header
        + format_code_lines(log_message_code_block)
        + log_message_footer
    )

    return log_message
