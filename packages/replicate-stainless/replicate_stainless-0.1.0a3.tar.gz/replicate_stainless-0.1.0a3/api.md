# Collections

Methods:

- <code title="get /collections">client.collections.<a href="./src/replicate/resources/collections.py">list</a>() -> None</code>

# Deployments

Types:

```python
from replicate.types import (
    DeploymentCreateResponse,
    DeploymentUpdateResponse,
    DeploymentListResponse,
    DeploymentGetResponse,
)
```

Methods:

- <code title="post /deployments">client.deployments.<a href="./src/replicate/resources/deployments/deployments.py">create</a>(\*\*<a href="src/replicate/types/deployment_create_params.py">params</a>) -> <a href="./src/replicate/types/deployment_create_response.py">DeploymentCreateResponse</a></code>
- <code title="patch /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/replicate/resources/deployments/deployments.py">update</a>(deployment_name, \*, deployment_owner, \*\*<a href="src/replicate/types/deployment_update_params.py">params</a>) -> <a href="./src/replicate/types/deployment_update_response.py">DeploymentUpdateResponse</a></code>
- <code title="get /deployments">client.deployments.<a href="./src/replicate/resources/deployments/deployments.py">list</a>() -> <a href="./src/replicate/types/deployment_list_response.py">SyncCursorURLPage[DeploymentListResponse]</a></code>
- <code title="delete /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/replicate/resources/deployments/deployments.py">delete</a>(deployment_name, \*, deployment_owner) -> None</code>
- <code title="get /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/replicate/resources/deployments/deployments.py">get</a>(deployment_name, \*, deployment_owner) -> <a href="./src/replicate/types/deployment_get_response.py">DeploymentGetResponse</a></code>
- <code title="get /collections">client.deployments.<a href="./src/replicate/resources/deployments/deployments.py">list_em_all</a>() -> None</code>

## Predictions

Methods:

- <code title="post /deployments/{deployment_owner}/{deployment_name}/predictions">client.deployments.predictions.<a href="./src/replicate/resources/deployments/predictions.py">create</a>(deployment_name, \*, deployment_owner, \*\*<a href="src/replicate/types/deployments/prediction_create_params.py">params</a>) -> <a href="./src/replicate/types/prediction.py">Prediction</a></code>

# Hardware

Types:

```python
from replicate.types import HardwareListResponse
```

Methods:

- <code title="get /hardware">client.hardware.<a href="./src/replicate/resources/hardware.py">list</a>() -> <a href="./src/replicate/types/hardware_list_response.py">HardwareListResponse</a></code>
- <code title="get /collections/{collection_slug}">client.hardware.<a href="./src/replicate/resources/hardware.py">retrieve_collections</a>(collection_slug) -> None</code>

# Accounts

Types:

```python
from replicate.types import AccountListResponse
```

Methods:

- <code title="get /account">client.accounts.<a href="./src/replicate/resources/accounts.py">list</a>() -> <a href="./src/replicate/types/account_list_response.py">AccountListResponse</a></code>

# Models

Types:

```python
from replicate.types import ModelListResponse
```

Methods:

- <code title="post /models">client.models.<a href="./src/replicate/resources/models/models.py">create</a>(\*\*<a href="src/replicate/types/model_create_params.py">params</a>) -> None</code>
- <code title="get /models">client.models.<a href="./src/replicate/resources/models/models.py">list</a>() -> <a href="./src/replicate/types/model_list_response.py">SyncCursorURLPage[ModelListResponse]</a></code>
- <code title="delete /models/{model_owner}/{model_name}">client.models.<a href="./src/replicate/resources/models/models.py">delete</a>(model_name, \*, model_owner) -> None</code>
- <code title="post /models/{model_owner}/{model_name}/predictions">client.models.<a href="./src/replicate/resources/models/models.py">create_prediction</a>(model_name, \*, model_owner, \*\*<a href="src/replicate/types/model_create_prediction_params.py">params</a>) -> <a href="./src/replicate/types/prediction.py">Prediction</a></code>
- <code title="get /models/{model_owner}/{model_name}">client.models.<a href="./src/replicate/resources/models/models.py">get</a>(model_name, \*, model_owner) -> None</code>

## Versions

Types:

```python
from replicate.types.models import VersionCreateTrainingResponse
```

Methods:

- <code title="get /models/{model_owner}/{model_name}/versions">client.models.versions.<a href="./src/replicate/resources/models/versions.py">list</a>(model_name, \*, model_owner) -> None</code>
- <code title="delete /models/{model_owner}/{model_name}/versions/{version_id}">client.models.versions.<a href="./src/replicate/resources/models/versions.py">delete</a>(version_id, \*, model_owner, model_name) -> None</code>
- <code title="post /models/{model_owner}/{model_name}/versions/{version_id}/trainings">client.models.versions.<a href="./src/replicate/resources/models/versions.py">create_training</a>(version_id, \*, model_owner, model_name, \*\*<a href="src/replicate/types/models/version_create_training_params.py">params</a>) -> <a href="./src/replicate/types/models/version_create_training_response.py">VersionCreateTrainingResponse</a></code>
- <code title="get /models/{model_owner}/{model_name}/versions/{version_id}">client.models.versions.<a href="./src/replicate/resources/models/versions.py">get</a>(version_id, \*, model_owner, model_name) -> None</code>

# Predictions

Types:

```python
from replicate.types import Prediction, PredictionOutput, PredictionRequest
```

Methods:

- <code title="post /predictions">client.predictions.<a href="./src/replicate/resources/predictions.py">create</a>(\*\*<a href="src/replicate/types/prediction_create_params.py">params</a>) -> <a href="./src/replicate/types/prediction.py">Prediction</a></code>
- <code title="get /predictions">client.predictions.<a href="./src/replicate/resources/predictions.py">list</a>(\*\*<a href="src/replicate/types/prediction_list_params.py">params</a>) -> <a href="./src/replicate/types/prediction.py">SyncCursorURLPageWithCreatedFilters[Prediction]</a></code>
- <code title="post /predictions/{prediction_id}/cancel">client.predictions.<a href="./src/replicate/resources/predictions.py">cancel</a>(prediction_id) -> None</code>
- <code title="get /predictions/{prediction_id}">client.predictions.<a href="./src/replicate/resources/predictions.py">get</a>(prediction_id) -> <a href="./src/replicate/types/prediction.py">Prediction</a></code>

# Trainings

Types:

```python
from replicate.types import TrainingListResponse, TrainingCancelResponse, TrainingGetResponse
```

Methods:

- <code title="get /trainings">client.trainings.<a href="./src/replicate/resources/trainings.py">list</a>() -> <a href="./src/replicate/types/training_list_response.py">SyncCursorURLPage[TrainingListResponse]</a></code>
- <code title="post /trainings/{training_id}/cancel">client.trainings.<a href="./src/replicate/resources/trainings.py">cancel</a>(training_id) -> <a href="./src/replicate/types/training_cancel_response.py">TrainingCancelResponse</a></code>
- <code title="get /trainings/{training_id}">client.trainings.<a href="./src/replicate/resources/trainings.py">get</a>(training_id) -> <a href="./src/replicate/types/training_get_response.py">TrainingGetResponse</a></code>

# Webhooks

## Default

Types:

```python
from replicate.types.webhooks import DefaultRetrieveSecretResponse
```

Methods:

- <code title="get /webhooks/default/secret">client.webhooks.default.<a href="./src/replicate/resources/webhooks/default.py">retrieve_secret</a>() -> <a href="./src/replicate/types/webhooks/default_retrieve_secret_response.py">DefaultRetrieveSecretResponse</a></code>
