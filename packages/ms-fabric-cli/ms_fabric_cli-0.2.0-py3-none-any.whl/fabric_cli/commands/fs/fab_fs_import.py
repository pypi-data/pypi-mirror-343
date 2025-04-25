# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

from argparse import Namespace

from fabric_cli.commands.fs.impor import fab_fs_import_item as import_item
from fabric_cli.core.fab_context import Context
from fabric_cli.core.fab_hiearchy import Item
from fabric_cli.utils import fab_util as utils


def exec_command(args: Namespace, context: Context) -> None:
    args.input = utils.process_nargs(args.input)

    if isinstance(context, Item):
        import_item.import_single_item(context, args)
