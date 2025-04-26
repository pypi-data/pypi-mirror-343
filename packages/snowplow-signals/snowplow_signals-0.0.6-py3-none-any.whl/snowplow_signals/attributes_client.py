from .api_client import ApiClient
from .models import (
    Service,
    View,
    ViewOutput,
    GetOnlineAttributesRequest,
    OnlineAttributesResponse,
)


class AttributesClient:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_view_attributes(
        self,
        view: View | ViewOutput,
        identifiers: list[str] | str,
    ) -> OnlineAttributesResponse:
        attributes = [
            f"{view.name}_v{view.version}:{attribute.name}"
            for attribute in (view.attributes or []) + (view.fields or [])
        ]

        request = GetOnlineAttributesRequest(
            attributes=attributes,
            entities={
                view.entity.name: (
                    identifiers if isinstance(identifiers, list) else [identifiers]
                )
            },
        )
        return self._make_request(request)

    def get_service_attributes(
        self,
        service: Service,
        identifiers: list[str] | str,
    ) -> None:
        if not service.views:
            raise ValueError("No views to fetch.")

        entity_names = {view.entity.name for view in service.views}
        if len(entity_names) > 1:
            raise ValueError(
                "The service contains views with different entities which is not supported."
            )
        entity_name = entity_names.pop()

        request = GetOnlineAttributesRequest(
            service=service.name,
            entities={
                entity_name: (
                    identifiers if isinstance(identifiers, list) else [identifiers]
                )
            },
        )
        return self._make_request(request)

    def _make_request(
        self, request: GetOnlineAttributesRequest
    ) -> OnlineAttributesResponse | None:
        response = self.api_client.make_request(
            method="POST",
            endpoint="get-online-attributes",
            data=request.model_dump(mode="json"),
        )
        return OnlineAttributesResponse(data=response) if response else None
