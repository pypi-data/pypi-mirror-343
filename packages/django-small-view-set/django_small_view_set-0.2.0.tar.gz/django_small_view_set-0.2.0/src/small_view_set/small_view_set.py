import inspect
import json
import logging
from django.http import JsonResponse
from urllib.request import Request

from .exceptions import BadRequest, MethodNotAllowed

logger = logging.getLogger('app')

class SmallViewSet:
    def parse_json_body(self, request: Request):
        if request.content_type != 'application/json':
            raise BadRequest('Invalid content type')
        return json.loads(request.body)

    def protect_create(self, request: Request):
        """
        Stub for adding any custom business logic to protect the create method.
        For example:
        - Check if the user is authenticated
        - Check if the user has validated their email
        - Throttle requests

        Recommended to call super().protect_create(request) in the subclass in case
        this library adds logic in the future.
        """
        pass

    def protect_list(self, request: Request):
        """
        Stub for adding any custom business logic to protect the list method.
        For example:
        - Check if the user is authenticated
        - Check if the user has validated their email
        - Throttle requests

        Recommended to call super().protect_create(request) in the subclass in case
        this library adds logic in the future.
        """
        pass

    def protect_retrieve(self, request: Request):
        """
        Stub for adding any custom business logic to protect the retrieve method.
        For example:
        - Check if the user is authenticated
        - Check if the user has validated their email
        - Throttle requests

        Recommended to call super().protect_create(request) in the subclass in case
        this library adds logic in the future.
        """
        pass

    def protect_update(self, request: Request):
        """
        Stub for adding any custom business logic to protect the update method.
        For example:
        - Check if the user is authenticated
        - Check if the user has validated their email
        - Throttle requests

        Recommended to call super().protect_create(request) in the subclass in case
        this library adds logic in the future.
        """
        pass

    def protect_delete(self, request: Request):
        """
        Stub for adding any custom business logic to protect the delete method.
        For example:
        - Check if the user is authenticated
        - Check if the user has validated their email
        - Throttle requests

        Recommended to call super().protect_create(request) in the subclass in case
        this library adds logic in the future.
        """
        pass

    async def default_router(self, request: Request, pk=None, *args, **kwargs):
        """
        This method routes requests to the appropriate method based on the HTTP method and presence of a primary key (pk).
        
        It also handles errors and returns appropriate JSON responses by using the decorator @default_handle_endpoint_exceptions.
        
        GET/POST for collection endpoints and GET/PUT/PATCH/DELETE for detail endpoints.

        Example:
        ```
        # Note: AppViewSet is a subclass of SmallViewSet with overridden protect methods with more specific logic.

        class CommentViewSet(AppViewSet):
            def urlpatterns(self):
                return [
                    path('api/comments/',                     self.default_router, name='comments_collection'),
                    path('api/comments/<int:pk>/',            self.default_router, name='comments_detail'),
                    path('api/comments/<int:pk>/custom_put/', self.custom_put,     name='comments_custom_put_detail'),
                ]

            @default_handle_endpoint_exceptions
            def create(self, request: Request):
                self.protect_create(request)
                . . .

            @default_handle_endpoint_exceptions
            def update(self, request: Request, pk: int):
                self.protect_update(request)
                . . .

            @default_handle_endpoint_exceptions
            def custom_put(self, request: Request, pk: int):
                self.protect_update(request)
                . . .

            @disable_endpoint
            @default_handle_endpoint_exceptions
            def some_disabled_endpoint(self, request: Request):
                self.protect_retrieve(request)
                . . .
        ```
        """
        func = None
        if pk is None:
            if request.method == 'GET':
                if hasattr(self, 'list'):
                    func = self.list

            elif request.method == 'POST':
                if hasattr(self, 'create'):
                    func = self.create
        else:
            if request.method == 'GET':
                if hasattr(self, 'retrieve'):
                    func = self.retrieve

            elif request.method == 'PUT':
                if hasattr(self, 'put'):
                    func = self.put

            elif request.method == 'PATCH':
                if hasattr(self, 'patch'):
                    func = self.patch

            elif request.method == 'DELETE':
                if hasattr(self, 'delete'):
                    func = self.delete

        if func is None:
            raise MethodNotAllowed(request.method)

        if pk is not None:
            kwargs['pk'] = pk

        if inspect.iscoroutinefunction(func):
            return await func(request, *args, **kwargs)
        else:
            return func(request, *args, **kwargs)
