"""Parser module to parse gear config.json."""

import logging
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext

log = logging.getLogger(__name__)


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str, str, str, str, bool, str, int]:
    """Parse the gear config.

    Return the requisite inputs and options for the gear.

    Returns:
        Tuple: api_key, protocol_name, file_path, file_id, output_file_prefix, delete_input, project_id, read_timeout
    """
    api_key = gear_context.get_input("api-key").get("key")
    protocol_name = gear_context.config.get("protocol_name")
    file_path = gear_context.get_input_path("input-file")
    file_id = gear_context.get_input_file_object("input-file").get("file_id")
    output_file_prefix = gear_context.config.get("output_file_prefix")
    delete_input = gear_context.config.get("delete_input")

    container = gear_context.client.get(gear_context.destination["id"])
    project_id = container.parents["project"]

    # If read_timeout is less than 60, then set it to 60.
    if (read_timeout := gear_context.config.get("read_timeout", 60)) < 60:
        read_timeout = 60
        log.warning("read_timeout is set to less than 60. Setting it to 60.")

    return (
        api_key,
        protocol_name,
        file_path,
        file_id,
        output_file_prefix,
        delete_input,
        project_id,
        read_timeout,
    )
