import logging
import os

from functools import lru_cache

import flywheel
from fw_file.dicom import DICOM

log = logging.getLogger(__name__)


# Note: "get_protocol_from_name": taken as-is from the
# form-and-annotations-exporter gear
@lru_cache(maxsize=512)
def get_protocol_from_name(client, protocol_name, project_id=None):
    """Get Protocol object from api by name.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol_name (str): The name of the protocol. Protocol Names are unique within
                             a project.
        project_id (str, optional): The ID of the project. Defaults to None.

    Returns:
        dict or None: The protocol object or None if not found.
    """
    filter_string = f"label={protocol_name}"
    if project_id:
        filter_string += f",project={project_id}"

    protocols = client.get("/api/read_task_protocols", params={"filter": filter_string})
    if protocols["count"] == 1:
        protocol = protocols["results"][0]
    elif protocols["count"] > 1:
        log.warning(
            "Found %s protocols with name %s.", protocols["count"], protocol_name
        )
        log.warning("Using last protocol found.")
        protocol = protocols["results"][-1]
    else:
        if project_id:
            log.error(
                "No protocol found with name %s for project %s.",
                protocol_name,
                project_id,
            )
            log.error(
                "Ensure you have the protocol define for the project you are "
                "running the gear under."
            )
        else:
            log.warning("No protocol found with name %s.", protocol_name)
        protocol = None
    return protocol


def redact_and_save_dicom(
    dcm: DICOM, start_x: int, end_x: int, start_y: int, end_y: int
) -> None:
    """Takes input pydicom object and redact it based on rectangle co-ordinates

    Args:
        dcm: input Flywheel Dicom file for a single dicom image
        start_x: start x co-ordinate of rectangle (upper left hand corner)
        end_x: end x co-ordinate of rectangle (lower right hand corner)
        start_y: start y co-ordinate of rectangle (upper left hand corner)
        end_y: end y co-ordinate of rectangle (lower right hand corner)

    Returns:
        Save the redacted raw data in the same Flywheel Dicom file.
    """
    ds = dcm.dataset.raw
    pix_array = ds.pixel_array
    pix_array[int(start_y) : int(end_y), int(start_x) : int(end_x)] = 0

    ds.PixelData = pix_array.tobytes()
    dcm.dataset.raw = ds
    dcm.save()


def set_output_filename(file_path, output_file_prefix) -> str:
    """Set the output filename based on the input filename and
    output_file_prefix.

    Args:
        file_path (str): The input file path.
        output_file_prefix (str): The prefix for the output file name.

    Returns:
        output_file_name (str): The output filename.
    """

    input_file_name = os.path.basename(file_path)
    if output_file_prefix:
        # If output_file_prefix is set, use it to create the output file name
        output_file_name = f"{output_file_prefix}_{input_file_name}"
        log.info(
            "Prefix provided. Output file name is set to '%s' based on the input file name '%s'.",
            output_file_name,
            input_file_name,
        )
    else:
        # If output_file_prefix is not set, use the input file name as the output file name
        output_file_name = input_file_name
        log.info(
            "No prefix provided. Output file name is set to '%s' based on the input file name '%s'.",
            output_file_name,
            input_file_name,
        )

    return output_file_name


def set_output_file_metadata(context, output_file_name):
    """Set the output file metadata based on input file metadata.

    Args:
        context (GearToolkitContext): The gear context.
        output_file_name (str): The output file name.

    Returns:
        None
    """

    # Get the input-file
    input_file_ = context.get_input_file_object("input-file")

    # Set metadata for output file, getting the modality, classification and custom
    # metadata from the input file
    metadata_dict = {
        "modality": input_file_.get("modality"),
        "classification": input_file_.get("classification").copy(),
        "info": input_file_.get("info").copy(),
    }

    # Get tags:
    tags = input_file_.get("tags", []).copy()
    # Remove "PHI-Found" tag if it exists
    if "PHI-Found" in tags:
        tags.remove("PHI-Found")
    # Add "redacted-image" tag if it doesn't exist
    if "redacted-image" not in tags:
        tags.append("redacted-image")
    metadata_dict["tags"] = tags

    # Update the output file's metadata
    context.update_file_metadata(file_=output_file_name, **metadata_dict)
    log.info(
        "Copied input file's metadata (modality, classification, info and tags) to output file."
    )

    return


def delete_flywheel_file(client: flywheel.Client, file_id: str):
    """Deletes a file from flywheel

    Args:
        client: the flywheel sdk client
        file_id: the flywheel file ID to delete

    Returns:
        None

    """
    client.delete_file(file_id=file_id)
    log.info("Deleted input file '%s'.", file_id)
