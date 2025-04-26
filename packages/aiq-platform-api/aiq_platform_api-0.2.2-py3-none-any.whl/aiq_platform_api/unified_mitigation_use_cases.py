# Example use cases for Unified Mitigation endpoints
from typing import Optional, Dict, Any

from aiq_platform_api.common_utils import (
    AttackIQRestClient,
    AttackIQLogger,
    UnifiedMitigationUtils,
    UnifiedMitigationProjectUtils,
    UnifiedMitigationWithRelationsUtils,
    UnifiedMitigationReportingUtils,
)
from aiq_platform_api.env import ATTACKIQ_API_TOKEN, ATTACKIQ_PLATFORM_URL

logger = AttackIQLogger.get_logger(__name__)


def list_mitigation_rules(client: AttackIQRestClient, limit: Optional[int] = 10) -> int:
    """Lists unified mitigation rules."""
    logger.info(f"Listing up to {limit} unified mitigations...")
    count = 0
    try:
        for rule in UnifiedMitigationUtils.list_mitigations(client, limit=limit):
            count += 1
            logger.info(
                f"Mitigation Rule {count}: ID={rule.get('id')}, Name={rule.get('name')}"
            )
        logger.info(f"Total mitigation rules listed: {count}")
    except Exception as e:
        logger.error(f"Failed to list mitigation rules: {e}")
    return count


def create_and_delete_mitigation_rule(
    client: AttackIQRestClient, rule_data: Dict[str, Any]
) -> None:
    """Creates a mitigation rule and then deletes it."""
    mitigation_id = None
    try:
        logger.info("Attempting to create a new mitigation rule...")
        created_rule = UnifiedMitigationUtils.create_mitigation(client, rule_data)
        if created_rule and created_rule.get("id"):
            mitigation_id = created_rule["id"]
            logger.info(
                f"Successfully created mitigation rule with ID: {mitigation_id}"
            )

            # Example: Get the created rule
            retrieved_rule = UnifiedMitigationUtils.get_mitigation(
                client, mitigation_id
            )
            if retrieved_rule:
                logger.info(f"Retrieved rule: {retrieved_rule.get('name')}")
            else:
                logger.warning("Could not retrieve the newly created rule.")

        else:
            logger.error(
                "Failed to create mitigation rule or ID not found in response."
            )
            return

    except Exception as e:
        logger.error(f"Error during mitigation rule creation/retrieval: {e}")
    finally:
        if mitigation_id:
            logger.info(f"Attempting to delete mitigation rule: {mitigation_id}")
            deleted = UnifiedMitigationUtils.delete_mitigation(client, mitigation_id)
            if deleted:
                logger.info(f"Successfully deleted mitigation rule: {mitigation_id}")
            else:
                logger.error(f"Failed to delete mitigation rule: {mitigation_id}")


def list_project_associations(
    client: AttackIQRestClient, limit: Optional[int] = 10
) -> int:
    """Lists unified mitigation project associations."""
    logger.info(f"Listing up to {limit} unified mitigation project associations...")
    count = 0
    try:
        for assoc in UnifiedMitigationProjectUtils.list_associations(
            client, limit=limit
        ):
            count += 1
            logger.info(
                f"Association {count}: ID={assoc.get('id')}, RuleID={assoc.get('unified_mitigation')}, ProjectID={assoc.get('project')}"
            )
        logger.info(f"Total associations listed: {count}")
    except Exception as e:
        logger.error(f"Failed to list project associations: {e}")
    return count


def list_mitigations_with_relations(
    client: AttackIQRestClient, limit: Optional[int] = 10
) -> int:
    """Lists unified mitigations including related project and detection data."""
    logger.info(f"Listing up to {limit} unified mitigations with relations...")
    count = 0
    try:
        for rule in UnifiedMitigationWithRelationsUtils.list_mitigations_with_relations(
            client, limit=limit
        ):
            count += 1
            logger.info(
                f"Mitigation+Relations {count}: ID={rule.get('id')}, Name={rule.get('name')}"
            )
            # Add more details as needed, e.g., project info
            if rule.get("project"):
                logger.info(f"  Associated Project: {rule.get('project').get('name')}")
        logger.info(f"Total mitigations with relations listed: {count}")
    except Exception as e:
        logger.error(f"Failed to list mitigations with relations: {e}")
    return count


def get_detection_timeline(
    client: AttackIQRestClient, params: Optional[Dict[str, Any]] = None
):
    """Gets the detection performance timeline data."""
    logger.info(f"Getting detection performance timeline with params: {params}")
    try:
        timeline_data = (
            UnifiedMitigationReportingUtils.get_detection_performance_timeline(
                client, params
            )
        )
        if timeline_data:
            logger.info(
                "Successfully retrieved detection timeline data."
            )  # Process or display data as needed  # logger.info(f"Timeline Data: {timeline_data}") # Potentially large output
        else:
            logger.warning("No detection timeline data returned.")
    except Exception as e:
        logger.error(f"Failed to get detection timeline: {e}")


def main():
    client = AttackIQRestClient(ATTACKIQ_PLATFORM_URL, ATTACKIQ_API_TOKEN)

    logger.info("--- Testing Unified Mitigation Rules ---")
    list_mitigation_rules(client, limit=5)
    # Example data - replace with actual valid data for your platform
    # Ensure 'mitigation_type' UUID exists in your environment
    test_rule_data = {
        "name": "SDK Test Rule - Delete Me",
        "description": "Test rule created via SDK examples",
        "mitigation_type": 1,  # 1 = Sigma (integer ID, not UUID)
        "rule_content": "test content",
        "severity": "medium",
        "rule_source": "custom",
        "source_type": "custom",
        # Required field
        "stage": "dev",  # Required field
        "is_active": True,  # Boolean value, not string 'active'
        "metadata": {},
    }
    # Uncomment to run create/delete test (ensure data is valid)
    create_and_delete_mitigation_rule(client, test_rule_data)

    logger.info("--- Testing Unified Mitigation Project Associations ---")
    list_project_associations(client, limit=5)
    # Add examples for create/delete association if needed, requires valid rule/project IDs

    logger.info("--- Testing Unified Mitigations With Relations ---")
    list_mitigations_with_relations(client, limit=5)

    logger.info("--- Testing Detection Performance Timeline ---")
    # Example params - adjust as needed
    timeline_params = {"time_interval": "monthly"}
    get_detection_timeline(client, timeline_params)


if __name__ == "__main__":
    main()
