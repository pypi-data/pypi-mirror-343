# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

class AuthErrors:
    @staticmethod
    def spn_auth_missing_tenant_id() -> str:
        return "Tenant ID is required for Service Principal authentication"

    @staticmethod
    def spn_auth_missing_client_id() -> str:
        return "Client ID is required for Service Principal authentication"
    
    @staticmethod
    def spn_auth_missing_client_secret() -> str:
        return "Client secret is required for Service Principal authentication with secret"
    
    @staticmethod
    def spn_auth_missing_cert_path() -> str:
        return "Certificate path is required for Service Principal authentication with certificate"
    
    @staticmethod
    def spn_auth_missing_federated_token() -> str:
        return "Federated token is required for Service Principal authentication with federated credential"


