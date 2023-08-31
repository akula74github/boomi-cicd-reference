import boomi_cicd

from boomi_cicd import logger


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Packaged_Component_object.html


def create_packaged_component(component_id, package_version, notes):
    """
    Create a packaged component.

    :param component_id: The ID of the component.
    :type component_id: str
    :param package_version: The version of the package.
    :type package_version: str
    :param notes: Additional notes for the package.
    :type notes: str
    :return: The ID of the created package.
    :rtype: str
    """
    resource_path = "/PackagedComponent"
    logger.info(resource_path)
    packaged_component_query = "boomi_cicd/util/json/createPackagedComponent.json"

    payload = boomi_cicd.parse_json(packaged_component_query)
    payload["componentId"] = component_id
    payload["packageVersion"] = package_version
    payload["notes"] = notes

    response = boomi_cicd.requests_post(resource_path, payload)

    package_id = response["packageId"]
    return package_id


def query_packaged_component(component_id, package_version):
    """
    Query the packaged component to check if it has already been created.

    :param component_id: The ID of the component.
    :type component_id: str
    :param package_version: The version of the package.
    :type package_version: str
    :return: The ID of the existing package, or an empty string if not found.
    :rtype: str
    """
    resource_path = "/PackagedComponent/query"
    logger.info(resource_path)
    logger.info(f"ComponentId: {component_id}")
    logger.info(f"PackagedVersion: {package_version}")
    packaged_component_query = "boomi_cicd/util/json/packagedComponentQuery.json"

    payload = boomi_cicd.parse_json(packaged_component_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][
        0
    ] = component_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][
        0
    ] = package_version

    response = boomi_cicd.requests_post(resource_path, payload)

    package_id = ""
    if response["numberOfResults"] > 0:
        logger.info(
            f"Packaged component has already been created. ComponentId: {component_id}, PackageId: {package_version}"
        )
        package_id = response["result"][0]["packageId"]

    return package_id
