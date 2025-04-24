# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from .readme import (
    ReadmeResource,
    AsyncReadmeResource,
    ReadmeResourceWithRawResponse,
    AsyncReadmeResourceWithRawResponse,
    ReadmeResourceWithStreamingResponse,
    AsyncReadmeResourceWithStreamingResponse,
)
from ...types import model_create_params, model_create_prediction_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import maybe_transform, strip_not_given, async_maybe_transform
from .examples import (
    ExamplesResource,
    AsyncExamplesResource,
    ExamplesResourceWithRawResponse,
    AsyncExamplesResourceWithRawResponse,
    ExamplesResourceWithStreamingResponse,
    AsyncExamplesResourceWithStreamingResponse,
)
from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorURLPage, AsyncCursorURLPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.prediction import Prediction
from ...types.model_list_response import ModelListResponse

__all__ = ["ModelsResource", "AsyncModelsResource"]


class ModelsResource(SyncAPIResource):
    @cached_property
    def examples(self) -> ExamplesResource:
        return ExamplesResource(self._client)

    @cached_property
    def readme(self) -> ReadmeResource:
        return ReadmeResource(self._client)

    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/replicate/replicate-python-stainless#accessing-raw-response-data-eg-headers
        """
        return ModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/replicate/replicate-python-stainless#with_streaming_response
        """
        return ModelsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        hardware: str,
        name: str,
        owner: str,
        visibility: Literal["public", "private"],
        cover_image_url: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        github_url: str | NotGiven = NOT_GIVEN,
        license_url: str | NotGiven = NOT_GIVEN,
        paper_url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a model.

        Example cURL request:

        ```console
        curl -s -X POST \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          -d '{"owner": "alice", "name": "my-model", "description": "An example model", "visibility": "public", "hardware": "cpu"}' \\
          https://api.replicate.com/v1/models
        ```

        The response will be a model object in the following format:

        ```json
        {
          "url": "https://replicate.com/alice/my-model",
          "owner": "alice",
          "name": "my-model",
          "description": "An example model",
          "visibility": "public",
          "github_url": null,
          "paper_url": null,
          "license_url": null,
          "run_count": 0,
          "cover_image_url": null,
          "default_example": null,
          "latest_version": null
        }
        ```

        Note that there is a limit of 1,000 models per account. For most purposes, we
        recommend using a single model and pushing new
        [versions](https://replicate.com/docs/how-does-replicate-work#versions) of the
        model as you make changes to it.

        Args:
          hardware: The SKU for the hardware used to run the model. Possible values can be retrieved
              from the `hardware.list` endpoint.

          name: The name of the model. This must be unique among all models owned by the user or
              organization.

          owner: The name of the user or organization that will own the model. This must be the
              same as the user or organization that is making the API request. In other words,
              the API token used in the request must belong to this user or organization.

          visibility: Whether the model should be public or private. A public model can be viewed and
              run by anyone, whereas a private model can be viewed and run only by the user or
              organization members that own the model.

          cover_image_url: A URL for the model's cover image. This should be an image file.

          description: A description of the model.

          github_url: A URL for the model's source code on GitHub.

          license_url: A URL for the model's license.

          paper_url: A URL for the model's paper.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/models",
            body=maybe_transform(
                {
                    "hardware": hardware,
                    "name": name,
                    "owner": owner,
                    "visibility": visibility,
                    "cover_image_url": cover_image_url,
                    "description": description,
                    "github_url": github_url,
                    "license_url": license_url,
                    "paper_url": paper_url,
                },
                model_create_params.ModelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorURLPage[ModelListResponse]:
        """
        Get a paginated list of public models.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models
        ```

        The response will be a pagination object containing a list of model objects.

        See the [`models.get`](#models.get) docs for more details about the model
        object.
        """
        return self._get_api_list(
            "/models",
            page=SyncCursorURLPage[ModelListResponse],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=ModelListResponse,
        )

    def delete(
        self,
        model_name: str,
        *,
        model_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a model

        Model deletion has some restrictions:

        - You can only delete models you own.
        - You can only delete private models.
        - You can only delete models that have no versions associated with them.
          Currently you'll need to
          [delete the model's versions](#models.versions.delete) before you can delete
          the model itself.

        Example cURL request:

        ```command
        curl -s -X DELETE \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world
        ```

        The response will be an empty 204, indicating the model has been deleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/models/{model_owner}/{model_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def create_prediction(
        self,
        model_name: str,
        *,
        model_owner: str,
        input: object,
        stream: bool | NotGiven = NOT_GIVEN,
        webhook: str | NotGiven = NOT_GIVEN,
        webhook_events_filter: List[Literal["start", "output", "logs", "completed"]] | NotGiven = NOT_GIVEN,
        prefer: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Prediction:
        """
        Create a prediction using an
        [official model](https://replicate.com/changelog/2025-01-29-official-models).

        If you're _not_ running an official model, use the
        [`predictions.create`](#predictions.create) operation instead.

        Example cURL request:

        ```console
        curl -s -X POST -H 'Prefer: wait' \\
          -d '{"input": {"prompt": "Write a short poem about the weather."}}' \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          https://api.replicate.com/v1/models/meta/meta-llama-3-70b-instruct/predictions
        ```

        The request will wait up to 60 seconds for the model to run. If this time is
        exceeded the prediction will be returned in a `"starting"` state and need to be
        retrieved using the `predictions.get` endpiont.

        For a complete overview of the `deployments.predictions.create` API check out
        our documentation on
        [creating a prediction](https://replicate.com/docs/topics/predictions/create-a-prediction)
        which covers a variety of use cases.

        Args:
          input: The model's input as a JSON object. The input schema depends on what model you
              are running. To see the available inputs, click the "API" tab on the model you
              are running or [get the model version](#models.versions.get) and look at its
              `openapi_schema` property. For example,
              [stability-ai/sdxl](https://replicate.com/stability-ai/sdxl) takes `prompt` as
              an input.

              Files should be passed as HTTP URLs or data URLs.

              Use an HTTP URL when:

              - you have a large file > 256kb
              - you want to be able to use the file multiple times
              - you want your prediction metadata to be associable with your input files

              Use a data URL when:

              - you have a small file <= 256kb
              - you don't want to upload and host the file somewhere
              - you don't need to use the file again (Replicate will not store it)

          stream: **This field is deprecated.**

              Request a URL to receive streaming output using
              [server-sent events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).

              This field is no longer needed as the returned prediction will always have a
              `stream` entry in its `url` property if the model supports streaming.

          webhook: An HTTPS URL for receiving a webhook when the prediction has new output. The
              webhook will be a POST request where the request body is the same as the
              response body of the [get prediction](#predictions.get) operation. If there are
              network problems, we will retry the webhook a few times, so make sure it can be
              safely called more than once. Replicate will not follow redirects when sending
              webhook requests to your service, so be sure to specify a URL that will resolve
              without redirecting.

          webhook_events_filter: By default, we will send requests to your webhook URL whenever there are new
              outputs or the prediction has finished. You can change which events trigger
              webhook requests by specifying `webhook_events_filter` in the prediction
              request:

              - `start`: immediately on prediction start
              - `output`: each time a prediction generates an output (note that predictions
                can generate multiple outputs)
              - `logs`: each time log output is generated by a prediction
              - `completed`: when the prediction reaches a terminal state
                (succeeded/canceled/failed)

              For example, if you only wanted requests to be sent at the start and end of the
              prediction, you would provide:

              ```json
              {
                "input": {
                  "text": "Alice"
                },
                "webhook": "https://example.com/my-webhook",
                "webhook_events_filter": ["start", "completed"]
              }
              ```

              Requests for event types `output` and `logs` will be sent at most once every
              500ms. If you request `start` and `completed` webhooks, then they'll always be
              sent regardless of throttling.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {**strip_not_given({"Prefer": prefer}), **(extra_headers or {})}
        return self._post(
            f"/models/{model_owner}/{model_name}/predictions",
            body=maybe_transform(
                {
                    "input": input,
                    "stream": stream,
                    "webhook": webhook,
                    "webhook_events_filter": webhook_events_filter,
                },
                model_create_prediction_params.ModelCreatePredictionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Prediction,
        )

    def get(
        self,
        model_name: str,
        *,
        model_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world
        ```

        The response will be a model object in the following format:

        ```json
        {
          "url": "https://replicate.com/replicate/hello-world",
          "owner": "replicate",
          "name": "hello-world",
          "description": "A tiny model that says hello",
          "visibility": "public",
          "github_url": "https://github.com/replicate/cog-examples",
          "paper_url": null,
          "license_url": null,
          "run_count": 5681081,
          "cover_image_url": "...",
          "default_example": {...},
          "latest_version": {...},
        }
        ```

        The model object includes the
        [input and output schema](https://replicate.com/docs/reference/openapi#model-schemas)
        for the latest version of the model.

        Here's an example showing how to fetch the model with cURL and display its input
        schema with [jq](https://stedolan.github.io/jq/):

        ```console
        curl -s \\
            -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
            https://api.replicate.com/v1/models/replicate/hello-world \\
            | jq ".latest_version.openapi_schema.components.schemas.Input"
        ```

        This will return the following JSON object:

        ```json
        {
          "type": "object",
          "title": "Input",
          "required": ["text"],
          "properties": {
            "text": {
              "type": "string",
              "title": "Text",
              "x-order": 0,
              "description": "Text to prefix with 'hello '"
            }
          }
        }
        ```

        The `cover_image_url` string is an HTTPS URL for an image file. This can be:

        - An image uploaded by the model author.
        - The output file of the example prediction, if the model author has not set a
          cover image.
        - The input file of the example prediction, if the model author has not set a
          cover image and the example prediction has no output file.
        - A generic fallback image.

        The `default_example` object is a [prediction](#predictions.get) created with
        this model.

        The `latest_version` object is the model's most recently pushed
        [version](#models.versions.get).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/models/{model_owner}/{model_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncModelsResource(AsyncAPIResource):
    @cached_property
    def examples(self) -> AsyncExamplesResource:
        return AsyncExamplesResource(self._client)

    @cached_property
    def readme(self) -> AsyncReadmeResource:
        return AsyncReadmeResource(self._client)

    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/replicate/replicate-python-stainless#accessing-raw-response-data-eg-headers
        """
        return AsyncModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/replicate/replicate-python-stainless#with_streaming_response
        """
        return AsyncModelsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        hardware: str,
        name: str,
        owner: str,
        visibility: Literal["public", "private"],
        cover_image_url: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        github_url: str | NotGiven = NOT_GIVEN,
        license_url: str | NotGiven = NOT_GIVEN,
        paper_url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create a model.

        Example cURL request:

        ```console
        curl -s -X POST \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          -d '{"owner": "alice", "name": "my-model", "description": "An example model", "visibility": "public", "hardware": "cpu"}' \\
          https://api.replicate.com/v1/models
        ```

        The response will be a model object in the following format:

        ```json
        {
          "url": "https://replicate.com/alice/my-model",
          "owner": "alice",
          "name": "my-model",
          "description": "An example model",
          "visibility": "public",
          "github_url": null,
          "paper_url": null,
          "license_url": null,
          "run_count": 0,
          "cover_image_url": null,
          "default_example": null,
          "latest_version": null
        }
        ```

        Note that there is a limit of 1,000 models per account. For most purposes, we
        recommend using a single model and pushing new
        [versions](https://replicate.com/docs/how-does-replicate-work#versions) of the
        model as you make changes to it.

        Args:
          hardware: The SKU for the hardware used to run the model. Possible values can be retrieved
              from the `hardware.list` endpoint.

          name: The name of the model. This must be unique among all models owned by the user or
              organization.

          owner: The name of the user or organization that will own the model. This must be the
              same as the user or organization that is making the API request. In other words,
              the API token used in the request must belong to this user or organization.

          visibility: Whether the model should be public or private. A public model can be viewed and
              run by anyone, whereas a private model can be viewed and run only by the user or
              organization members that own the model.

          cover_image_url: A URL for the model's cover image. This should be an image file.

          description: A description of the model.

          github_url: A URL for the model's source code on GitHub.

          license_url: A URL for the model's license.

          paper_url: A URL for the model's paper.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/models",
            body=await async_maybe_transform(
                {
                    "hardware": hardware,
                    "name": name,
                    "owner": owner,
                    "visibility": visibility,
                    "cover_image_url": cover_image_url,
                    "description": description,
                    "github_url": github_url,
                    "license_url": license_url,
                    "paper_url": paper_url,
                },
                model_create_params.ModelCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[ModelListResponse, AsyncCursorURLPage[ModelListResponse]]:
        """
        Get a paginated list of public models.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models
        ```

        The response will be a pagination object containing a list of model objects.

        See the [`models.get`](#models.get) docs for more details about the model
        object.
        """
        return self._get_api_list(
            "/models",
            page=AsyncCursorURLPage[ModelListResponse],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=ModelListResponse,
        )

    async def delete(
        self,
        model_name: str,
        *,
        model_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a model

        Model deletion has some restrictions:

        - You can only delete models you own.
        - You can only delete private models.
        - You can only delete models that have no versions associated with them.
          Currently you'll need to
          [delete the model's versions](#models.versions.delete) before you can delete
          the model itself.

        Example cURL request:

        ```command
        curl -s -X DELETE \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world
        ```

        The response will be an empty 204, indicating the model has been deleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/models/{model_owner}/{model_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def create_prediction(
        self,
        model_name: str,
        *,
        model_owner: str,
        input: object,
        stream: bool | NotGiven = NOT_GIVEN,
        webhook: str | NotGiven = NOT_GIVEN,
        webhook_events_filter: List[Literal["start", "output", "logs", "completed"]] | NotGiven = NOT_GIVEN,
        prefer: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Prediction:
        """
        Create a prediction using an
        [official model](https://replicate.com/changelog/2025-01-29-official-models).

        If you're _not_ running an official model, use the
        [`predictions.create`](#predictions.create) operation instead.

        Example cURL request:

        ```console
        curl -s -X POST -H 'Prefer: wait' \\
          -d '{"input": {"prompt": "Write a short poem about the weather."}}' \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          https://api.replicate.com/v1/models/meta/meta-llama-3-70b-instruct/predictions
        ```

        The request will wait up to 60 seconds for the model to run. If this time is
        exceeded the prediction will be returned in a `"starting"` state and need to be
        retrieved using the `predictions.get` endpiont.

        For a complete overview of the `deployments.predictions.create` API check out
        our documentation on
        [creating a prediction](https://replicate.com/docs/topics/predictions/create-a-prediction)
        which covers a variety of use cases.

        Args:
          input: The model's input as a JSON object. The input schema depends on what model you
              are running. To see the available inputs, click the "API" tab on the model you
              are running or [get the model version](#models.versions.get) and look at its
              `openapi_schema` property. For example,
              [stability-ai/sdxl](https://replicate.com/stability-ai/sdxl) takes `prompt` as
              an input.

              Files should be passed as HTTP URLs or data URLs.

              Use an HTTP URL when:

              - you have a large file > 256kb
              - you want to be able to use the file multiple times
              - you want your prediction metadata to be associable with your input files

              Use a data URL when:

              - you have a small file <= 256kb
              - you don't want to upload and host the file somewhere
              - you don't need to use the file again (Replicate will not store it)

          stream: **This field is deprecated.**

              Request a URL to receive streaming output using
              [server-sent events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).

              This field is no longer needed as the returned prediction will always have a
              `stream` entry in its `url` property if the model supports streaming.

          webhook: An HTTPS URL for receiving a webhook when the prediction has new output. The
              webhook will be a POST request where the request body is the same as the
              response body of the [get prediction](#predictions.get) operation. If there are
              network problems, we will retry the webhook a few times, so make sure it can be
              safely called more than once. Replicate will not follow redirects when sending
              webhook requests to your service, so be sure to specify a URL that will resolve
              without redirecting.

          webhook_events_filter: By default, we will send requests to your webhook URL whenever there are new
              outputs or the prediction has finished. You can change which events trigger
              webhook requests by specifying `webhook_events_filter` in the prediction
              request:

              - `start`: immediately on prediction start
              - `output`: each time a prediction generates an output (note that predictions
                can generate multiple outputs)
              - `logs`: each time log output is generated by a prediction
              - `completed`: when the prediction reaches a terminal state
                (succeeded/canceled/failed)

              For example, if you only wanted requests to be sent at the start and end of the
              prediction, you would provide:

              ```json
              {
                "input": {
                  "text": "Alice"
                },
                "webhook": "https://example.com/my-webhook",
                "webhook_events_filter": ["start", "completed"]
              }
              ```

              Requests for event types `output` and `logs` will be sent at most once every
              500ms. If you request `start` and `completed` webhooks, then they'll always be
              sent regardless of throttling.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {**strip_not_given({"Prefer": prefer}), **(extra_headers or {})}
        return await self._post(
            f"/models/{model_owner}/{model_name}/predictions",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "stream": stream,
                    "webhook": webhook,
                    "webhook_events_filter": webhook_events_filter,
                },
                model_create_prediction_params.ModelCreatePredictionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Prediction,
        )

    async def get(
        self,
        model_name: str,
        *,
        model_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world
        ```

        The response will be a model object in the following format:

        ```json
        {
          "url": "https://replicate.com/replicate/hello-world",
          "owner": "replicate",
          "name": "hello-world",
          "description": "A tiny model that says hello",
          "visibility": "public",
          "github_url": "https://github.com/replicate/cog-examples",
          "paper_url": null,
          "license_url": null,
          "run_count": 5681081,
          "cover_image_url": "...",
          "default_example": {...},
          "latest_version": {...},
        }
        ```

        The model object includes the
        [input and output schema](https://replicate.com/docs/reference/openapi#model-schemas)
        for the latest version of the model.

        Here's an example showing how to fetch the model with cURL and display its input
        schema with [jq](https://stedolan.github.io/jq/):

        ```console
        curl -s \\
            -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
            https://api.replicate.com/v1/models/replicate/hello-world \\
            | jq ".latest_version.openapi_schema.components.schemas.Input"
        ```

        This will return the following JSON object:

        ```json
        {
          "type": "object",
          "title": "Input",
          "required": ["text"],
          "properties": {
            "text": {
              "type": "string",
              "title": "Text",
              "x-order": 0,
              "description": "Text to prefix with 'hello '"
            }
          }
        }
        ```

        The `cover_image_url` string is an HTTPS URL for an image file. This can be:

        - An image uploaded by the model author.
        - The output file of the example prediction, if the model author has not set a
          cover image.
        - The input file of the example prediction, if the model author has not set a
          cover image and the example prediction has no output file.
        - A generic fallback image.

        The `default_example` object is a [prediction](#predictions.get) created with
        this model.

        The `latest_version` object is the model's most recently pushed
        [version](#models.versions.get).

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/models/{model_owner}/{model_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ModelsResourceWithRawResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.create = to_raw_response_wrapper(
            models.create,
        )
        self.list = to_raw_response_wrapper(
            models.list,
        )
        self.delete = to_raw_response_wrapper(
            models.delete,
        )
        self.create_prediction = to_raw_response_wrapper(
            models.create_prediction,
        )
        self.get = to_raw_response_wrapper(
            models.get,
        )

    @cached_property
    def examples(self) -> ExamplesResourceWithRawResponse:
        return ExamplesResourceWithRawResponse(self._models.examples)

    @cached_property
    def readme(self) -> ReadmeResourceWithRawResponse:
        return ReadmeResourceWithRawResponse(self._models.readme)

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._models.versions)


class AsyncModelsResourceWithRawResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.create = async_to_raw_response_wrapper(
            models.create,
        )
        self.list = async_to_raw_response_wrapper(
            models.list,
        )
        self.delete = async_to_raw_response_wrapper(
            models.delete,
        )
        self.create_prediction = async_to_raw_response_wrapper(
            models.create_prediction,
        )
        self.get = async_to_raw_response_wrapper(
            models.get,
        )

    @cached_property
    def examples(self) -> AsyncExamplesResourceWithRawResponse:
        return AsyncExamplesResourceWithRawResponse(self._models.examples)

    @cached_property
    def readme(self) -> AsyncReadmeResourceWithRawResponse:
        return AsyncReadmeResourceWithRawResponse(self._models.readme)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._models.versions)


class ModelsResourceWithStreamingResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.create = to_streamed_response_wrapper(
            models.create,
        )
        self.list = to_streamed_response_wrapper(
            models.list,
        )
        self.delete = to_streamed_response_wrapper(
            models.delete,
        )
        self.create_prediction = to_streamed_response_wrapper(
            models.create_prediction,
        )
        self.get = to_streamed_response_wrapper(
            models.get,
        )

    @cached_property
    def examples(self) -> ExamplesResourceWithStreamingResponse:
        return ExamplesResourceWithStreamingResponse(self._models.examples)

    @cached_property
    def readme(self) -> ReadmeResourceWithStreamingResponse:
        return ReadmeResourceWithStreamingResponse(self._models.readme)

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._models.versions)


class AsyncModelsResourceWithStreamingResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.create = async_to_streamed_response_wrapper(
            models.create,
        )
        self.list = async_to_streamed_response_wrapper(
            models.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            models.delete,
        )
        self.create_prediction = async_to_streamed_response_wrapper(
            models.create_prediction,
        )
        self.get = async_to_streamed_response_wrapper(
            models.get,
        )

    @cached_property
    def examples(self) -> AsyncExamplesResourceWithStreamingResponse:
        return AsyncExamplesResourceWithStreamingResponse(self._models.examples)

    @cached_property
    def readme(self) -> AsyncReadmeResourceWithStreamingResponse:
        return AsyncReadmeResourceWithStreamingResponse(self._models.readme)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._models.versions)
