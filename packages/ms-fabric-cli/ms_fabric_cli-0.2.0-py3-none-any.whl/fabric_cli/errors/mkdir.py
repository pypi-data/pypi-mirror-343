# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

class MkdirErrors:
    @staticmethod
    def workspace_name_exists() -> str:
        return "A workspace with the same name exists"

    @staticmethod
    def workspace_capacity_not_found() -> str:
        return (f"Capacity not found or invalid. "
            f"Use 'config set default_capacity <capacity_name>' or '-P capacityName=<capacity_name>'")
