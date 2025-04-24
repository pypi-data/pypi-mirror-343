from collections.abc import Callable

from labels.model.core import OutputFormat, SbomConfig
from labels.model.package import Package
from labels.model.relationship import Relationship
from labels.model.resolver import Resolver
from labels.output.cyclonedx.output_handler import format_cyclonedx_sbom
from labels.output.fluid.output_handler import format_fluid_sbom
from labels.output.spdx.output_handler import format_spdx_sbom

_FORMAT_HANDLERS: dict[OutputFormat, Callable] = {
    OutputFormat.FLUID_JSON: format_fluid_sbom,
    OutputFormat.CYCLONEDX_JSON: format_cyclonedx_sbom,
    OutputFormat.CYCLONEDX_XML: format_cyclonedx_sbom,
    OutputFormat.SPDX_JSON: format_spdx_sbom,
    OutputFormat.SPDX_XML: format_spdx_sbom,
}


def merge_packages(packages: list[Package]) -> list[Package]:
    merged_packages: dict[str | Package, Package] = {}

    for package in packages:
        if package.id_:
            if package.id_ in merged_packages:
                merged_packages[package.id_].locations.extend(
                    x for x in package.locations if x not in merged_packages[package.id_].locations
                )
            else:
                merged_packages[package.id_] = package
        else:
            merged_packages[package] = package

    return list(merged_packages.values())


def dispatch_sbom_output(
    *,
    packages: list[Package],
    relationships: list[Relationship],
    config: SbomConfig,
    resolver: Resolver,
) -> None:
    processed_packages = merge_packages(packages)

    handler = _FORMAT_HANDLERS[config.output_format]
    handler(
        packages=processed_packages,
        relationships=relationships,
        config=config,
        resolver=resolver,
    )
