# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.commands.fs.export import fab_fs_export_item as export_item
from fabric_cli.core.fab_hiearchy import FabricElement, Item, Workspace
from fabric_cli.utils import fab_util as utils


def exec_command(args: Namespace, context: FabricElement) -> None:
    args.output = utils.process_nargs(args.output)

    if isinstance(context, Workspace):
        export_item.export_bulk_items(context, args)
    elif isinstance(context, Item):
        export_item.export_single_item(context, args)
