# Django Small View Set

A lightweight Django ViewSet alternative with minimal abstraction. This library provides a simple and transparent way to define API endpoints without relying on complex abstractions.

## Getting Started with Django Small View Set

This guide provides a simple example to get started with the library.

### Example Usage

Here’s how to define a basic view set:

In settings.py
```python
# Register SmallViewSetConfig in settings
from small_view_set SmallViewSetConfig

SMALL_VIEW_SET_CONFIG = SmallViewSetConfig()
```


```python
import asyncio
from django.http import JsonResponse
from django.urls import path
from small_view_set import SmallViewSet, endpoint, endpoint_disabled

class BarViewSet(SmallViewSet):

    def urlpatterns(self):
        return [
            path('api/bars/',          self.default_router, name='bars_collection'),
            path('api/bars/items/',    self.items,          name='bars_items'),
            path('api/bars/<int:pk>/', self.default_router, name='bars_detail'),
        ]

    @endpoint(allowed_methods=['GET'])
    def list(self, request):
        self.protect_list(request)
        return JsonResponse({"message": "Hello, world!"}, status=200)

    @endpoint(allowed_methods=['GET'])
    @endpoint_disabled
    async def items(self, request):
        self.protect_list(request)
        await asyncio.sleep(1)
        return JsonResponse({"message": "List of items"}, status=200)

    @endpoint(allowed_methods=['PATCH'])
    def patch(self, request, pk):
        self.protect_update(request)
        return JsonResponse({"message": f"Updated {pk}"}, status=200)

    @endpoint(allowed_methods=['GET'])
    async def retrieve(self, request, pk):
        self.protect_retrieve(request)
        return JsonResponse({"message": f"Detail for ID {pk}"}, status=200)
```


## Registering in `urls.py`

To register the viewset in your `urls.py`:

```python
from api.views.bar import BarViewSet

urlpatterns = [
    # Other URLs like admin, static, etc.

    *BarViewSet().urlpatterns(),
]
```


## Documentation

- [Custom Endpoints](./README_CUSTOM_ENDPOINT.md): Learn how to define custom endpoints alongside the default router.
- [Handling Endpoint Exceptions](./README_HANDLE_ENDPOINT_EXCEPTIONS.md): Understand how to write your own decorators for exception handling.
- [Custom Protections](./README_CUSTOM_PROTECTIONS.md): Learn how to subclass `SmallViewSet` to add custom protections like logged-in checks.
- [DRF Compatibility](./README_DRF_COMPATIBILITY.md): Learn how to use some of Django Rest Framework's tools, like Serializers.
- [Disabling an endpoint](./README_DISABLE_ENDPOINT.md): Learn how to disable an endpoint without needing to delete it or comment it out.
- [Reason](./README_REASON.md): Reasoning behind this package.
