# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

class CommonErrors:
    @staticmethod
    def file_or_directory_not_exists() -> str:
        return "No such file or directory"

    @staticmethod
    def invalid_json_format() -> str:
        return "Invalid JSON format"
