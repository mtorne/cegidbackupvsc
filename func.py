#
# oci-list-instances-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import datetime

from fdk import response

import oci

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    bvgbid = btype = bname = ""
    cfg = ctx.Config()
    bvgbid = cfg["bvgbid"]
    btype = cfg["btype"]
    bname = cfg["bname"]
    #bvid = "ocid1.volume.oc1.eu-frankfurt-1.abtheljryoeofjvfgp3jstz2au5iigr6h642appq2gf556zzo2fc3w34seea"
    #resp = list_instances(signer)
    resp2 = create_backup(signer,bvgbid,btype,bname)
    return response.Response(
        ctx,
        response_data=json.dumps(resp2),
        headers={"Content-Type": "application/json"}
    )

# List instances ---------------------------------------------------------------
def list_instances(signer):
    client = oci.core.ComputeClient(config={}, signer=signer)
    # OCI API to manage Compute resources such as compute instances, block storage volumes, etc.
    try:
        # Returns a list of all instances in the current compartment
        inst = client.list_instances(signer.compartment_id)
        # Create a list that holds a list of the instances id and name next to each other
        inst = [[i.id, i.display_name] for i in inst.data]
    except Exception as ex:
        print("ERROR: accessing Compute instances failed", ex, flush=True)
        raise
    resp = { "instances": inst }
    return resp

# List instances ---------------------------------------------------------------
def create_backup(signer,bvgbid,btype,bname):
    client = oci.core.BlockstorageClient(config={}, signer=signer)
    ct = datetime.datetime.now()
    # OCI API to manage Compute resources such as compute instances, block storage volumes, etc.
    try:
        create_volume_group_backup_response = client.create_volume_group_backup(
          create_volume_group_backup_details=oci.core.models.CreateVolumeGroupBackupDetails(
            volume_group_id=bvgbid,
            display_name=bname + str(ct),
            type=btype),
          )
        print(create_volume_group_backup_response.data, flush=True)   
    except Exception as ex:
        print("ERROR: Creating Block Volume Group backup", ex, flush=True)
        raise
    resp = { "Block Volume Group backup": "OK" }
    return resp