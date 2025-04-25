# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

class StartStopErrors:
    @staticmethod
    def invalid_state_stop_capacity(capacityName: str, state: str) -> str:
        return f"'{capacityName}' is not in a valid state to stop. State: {state}"

    @staticmethod
    def invalid_state_start_capacity(capacityName: str, state: str) -> str:
        return f"'{capacityName}' is not in a valid state to start. State: {state}"
