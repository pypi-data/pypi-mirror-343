import logging
from collections import defaultdict

from cyclonedx.factory.license import LicenseFactory
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.model.license import LicenseExpression
from cyclonedx.model.tool import Tool
from packageurl import PackageURL

from labels.model.package import Package
from labels.model.relationship import Relationship
from labels.output.cyclonedx.complete_file import (
    add_authors,
    add_component_properties,
    add_integrity,
    add_vulnerabilities,
)

LOGGER = logging.getLogger(__name__)


def pkg_to_component(package: Package) -> Component:
    lc_factory = LicenseFactory()
    licenses = [
        lc_factory.make_from_string(lic)
        for lic in package.licenses
        if not isinstance(lc_factory.make_from_string(lic), LicenseExpression)
    ]
    health_metadata = package.health_metadata
    return Component(
        type=ComponentType.LIBRARY,
        name=package.name,
        version=package.version,
        licenses=licenses,
        authors=add_authors(health_metadata) if health_metadata else [],
        bom_ref=f"{package.name}@{package.version}",
        purl=PackageURL.from_string(package.p_url),
        properties=add_component_properties(package),
        hashes=add_integrity(health_metadata) if health_metadata else [],
    )


def create_bom(namespace: str, version: str | None) -> Bom:
    bom = Bom()
    bom.metadata.component = Component(
        name=namespace,
        type=ComponentType.APPLICATION,
        licenses=[],
        bom_ref="",
        version=version,
    )
    bom.metadata.tools.tools.add(Tool(vendor="Fluid Attacks", name="Fluid-Labels"))
    return bom


def add_components_to_bom(
    bom: Bom,
    packages: list[Package],
    component_cache: dict[Package, Component],
) -> None:
    for component in component_cache.values():
        bom.components.add(component)
        if bom.metadata.component:
            bom.register_dependency(bom.metadata.component, [component])
        package = next(
            pkg
            for pkg in packages
            if pkg.name == component.name and pkg.version == component.version
        )
        if package.advisories:
            vulnerabilities = add_vulnerabilities(package)
            for vulnerability in vulnerabilities:
                bom.vulnerabilities.add(vulnerability)


def add_relationships_to_bom(
    bom: Bom,
    relationships: list[Relationship],
    component_cache: dict[Package, Component],
) -> None:
    dependency_map: dict[Component, list[Component]] = defaultdict(list)
    for relationship in relationships:
        to_pkg = component_cache.get(relationship.to_, pkg_to_component(relationship.to_))
        from_pkg = component_cache.get(relationship.from_, pkg_to_component(relationship.from_))
        dependency_map[to_pkg].append(from_pkg)

    for ref, depends_on_list in dependency_map.items():
        bom.register_dependency(ref, depends_on_list)
