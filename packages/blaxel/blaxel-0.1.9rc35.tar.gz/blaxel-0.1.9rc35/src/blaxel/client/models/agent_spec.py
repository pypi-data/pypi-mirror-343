from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_chain import AgentChain
    from ..models.core_spec_configurations import CoreSpecConfigurations
    from ..models.flavor import Flavor
    from ..models.model_private_cluster import ModelPrivateCluster
    from ..models.pod_template_spec import PodTemplateSpec
    from ..models.repository import Repository
    from ..models.revision_configuration import RevisionConfiguration
    from ..models.runtime import Runtime
    from ..models.serverless_config import ServerlessConfig


T = TypeVar("T", bound="AgentSpec")


@_attrs_define
class AgentSpec:
    """Agent specification

    Attributes:
        configurations (Union[Unset, CoreSpecConfigurations]): Optional configurations for the object
        enabled (Union[Unset, bool]): Enable or disable the agent
        flavors (Union[Unset, list['Flavor']]): Types of hardware available for deployments
        integration_connections (Union[Unset, list[str]]):
        pod_template (Union[Unset, PodTemplateSpec]): Pod template specification
        policies (Union[Unset, list[str]]):
        private_clusters (Union[Unset, ModelPrivateCluster]): Private cluster where the model deployment is deployed
        revision (Union[Unset, RevisionConfiguration]): Revision configuration
        runtime (Union[Unset, Runtime]): Set of configurations for a deployment
        sandbox (Union[Unset, bool]): Sandbox mode
        serverless_config (Union[Unset, ServerlessConfig]): Configuration for a serverless deployment
        agent_chain (Union[Unset, list['AgentChain']]): Agent chain
        description (Union[Unset, str]): Description, small description computed from the prompt
        functions (Union[Unset, list[str]]):
        knowledgebase (Union[Unset, str]): Knowledgebase Name
        model (Union[Unset, str]): Model name
        prompt (Union[Unset, str]): Prompt, describe what your agent does
        repository (Union[Unset, Repository]): Repository
        store_id (Union[Unset, str]): Store id
    """

    configurations: Union[Unset, "CoreSpecConfigurations"] = UNSET
    enabled: Union[Unset, bool] = UNSET
    flavors: Union[Unset, list["Flavor"]] = UNSET
    integration_connections: Union[Unset, list[str]] = UNSET
    pod_template: Union[Unset, "PodTemplateSpec"] = UNSET
    policies: Union[Unset, list[str]] = UNSET
    private_clusters: Union[Unset, "ModelPrivateCluster"] = UNSET
    revision: Union[Unset, "RevisionConfiguration"] = UNSET
    runtime: Union[Unset, "Runtime"] = UNSET
    sandbox: Union[Unset, bool] = UNSET
    serverless_config: Union[Unset, "ServerlessConfig"] = UNSET
    agent_chain: Union[Unset, list["AgentChain"]] = UNSET
    description: Union[Unset, str] = UNSET
    functions: Union[Unset, list[str]] = UNSET
    knowledgebase: Union[Unset, str] = UNSET
    model: Union[Unset, str] = UNSET
    prompt: Union[Unset, str] = UNSET
    repository: Union[Unset, "Repository"] = UNSET
    store_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configurations: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.configurations
            and not isinstance(self.configurations, Unset)
            and not isinstance(self.configurations, dict)
        ):
            configurations = self.configurations.to_dict()
        elif self.configurations and isinstance(self.configurations, dict):
            configurations = self.configurations

        enabled = self.enabled

        flavors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = []
            for componentsschemas_flavors_item_data in self.flavors:
                if type(componentsschemas_flavors_item_data) == dict:
                    componentsschemas_flavors_item = componentsschemas_flavors_item_data
                else:
                    componentsschemas_flavors_item = componentsschemas_flavors_item_data.to_dict()
                flavors.append(componentsschemas_flavors_item)

        integration_connections: Union[Unset, list[str]] = UNSET
        if not isinstance(self.integration_connections, Unset):
            integration_connections = self.integration_connections

        pod_template: Union[Unset, dict[str, Any]] = UNSET
        if self.pod_template and not isinstance(self.pod_template, Unset) and not isinstance(self.pod_template, dict):
            pod_template = self.pod_template.to_dict()
        elif self.pod_template and isinstance(self.pod_template, dict):
            pod_template = self.pod_template

        policies: Union[Unset, list[str]] = UNSET
        if not isinstance(self.policies, Unset):
            policies = self.policies

        private_clusters: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.private_clusters
            and not isinstance(self.private_clusters, Unset)
            and not isinstance(self.private_clusters, dict)
        ):
            private_clusters = self.private_clusters.to_dict()
        elif self.private_clusters and isinstance(self.private_clusters, dict):
            private_clusters = self.private_clusters

        revision: Union[Unset, dict[str, Any]] = UNSET
        if self.revision and not isinstance(self.revision, Unset) and not isinstance(self.revision, dict):
            revision = self.revision.to_dict()
        elif self.revision and isinstance(self.revision, dict):
            revision = self.revision

        runtime: Union[Unset, dict[str, Any]] = UNSET
        if self.runtime and not isinstance(self.runtime, Unset) and not isinstance(self.runtime, dict):
            runtime = self.runtime.to_dict()
        elif self.runtime and isinstance(self.runtime, dict):
            runtime = self.runtime

        sandbox = self.sandbox

        serverless_config: Union[Unset, dict[str, Any]] = UNSET
        if (
            self.serverless_config
            and not isinstance(self.serverless_config, Unset)
            and not isinstance(self.serverless_config, dict)
        ):
            serverless_config = self.serverless_config.to_dict()
        elif self.serverless_config and isinstance(self.serverless_config, dict):
            serverless_config = self.serverless_config

        agent_chain: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.agent_chain, Unset):
            agent_chain = []
            for componentsschemas_agent_chains_item_data in self.agent_chain:
                if type(componentsschemas_agent_chains_item_data) == dict:
                    componentsschemas_agent_chains_item = componentsschemas_agent_chains_item_data
                else:
                    componentsschemas_agent_chains_item = componentsschemas_agent_chains_item_data.to_dict()
                agent_chain.append(componentsschemas_agent_chains_item)

        description = self.description

        functions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.functions, Unset):
            functions = self.functions

        knowledgebase = self.knowledgebase

        model = self.model

        prompt = self.prompt

        repository: Union[Unset, dict[str, Any]] = UNSET
        if self.repository and not isinstance(self.repository, Unset) and not isinstance(self.repository, dict):
            repository = self.repository.to_dict()
        elif self.repository and isinstance(self.repository, dict):
            repository = self.repository

        store_id = self.store_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if configurations is not UNSET:
            field_dict["configurations"] = configurations
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if integration_connections is not UNSET:
            field_dict["integrationConnections"] = integration_connections
        if pod_template is not UNSET:
            field_dict["podTemplate"] = pod_template
        if policies is not UNSET:
            field_dict["policies"] = policies
        if private_clusters is not UNSET:
            field_dict["privateClusters"] = private_clusters
        if revision is not UNSET:
            field_dict["revision"] = revision
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if sandbox is not UNSET:
            field_dict["sandbox"] = sandbox
        if serverless_config is not UNSET:
            field_dict["serverlessConfig"] = serverless_config
        if agent_chain is not UNSET:
            field_dict["agentChain"] = agent_chain
        if description is not UNSET:
            field_dict["description"] = description
        if functions is not UNSET:
            field_dict["functions"] = functions
        if knowledgebase is not UNSET:
            field_dict["knowledgebase"] = knowledgebase
        if model is not UNSET:
            field_dict["model"] = model
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if repository is not UNSET:
            field_dict["repository"] = repository
        if store_id is not UNSET:
            field_dict["storeId"] = store_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.agent_chain import AgentChain
        from ..models.core_spec_configurations import CoreSpecConfigurations
        from ..models.flavor import Flavor
        from ..models.model_private_cluster import ModelPrivateCluster
        from ..models.pod_template_spec import PodTemplateSpec
        from ..models.repository import Repository
        from ..models.revision_configuration import RevisionConfiguration
        from ..models.runtime import Runtime
        from ..models.serverless_config import ServerlessConfig

        if not src_dict:
            return None
        d = src_dict.copy()
        _configurations = d.pop("configurations", UNSET)
        configurations: Union[Unset, CoreSpecConfigurations]
        if isinstance(_configurations, Unset):
            configurations = UNSET
        else:
            configurations = CoreSpecConfigurations.from_dict(_configurations)

        enabled = d.pop("enabled", UNSET)

        flavors = []
        _flavors = d.pop("flavors", UNSET)
        for componentsschemas_flavors_item_data in _flavors or []:
            componentsschemas_flavors_item = Flavor.from_dict(componentsschemas_flavors_item_data)

            flavors.append(componentsschemas_flavors_item)

        integration_connections = cast(list[str], d.pop("integrationConnections", UNSET))

        _pod_template = d.pop("podTemplate", UNSET)
        pod_template: Union[Unset, PodTemplateSpec]
        if isinstance(_pod_template, Unset):
            pod_template = UNSET
        else:
            pod_template = PodTemplateSpec.from_dict(_pod_template)

        policies = cast(list[str], d.pop("policies", UNSET))

        _private_clusters = d.pop("privateClusters", UNSET)
        private_clusters: Union[Unset, ModelPrivateCluster]
        if isinstance(_private_clusters, Unset):
            private_clusters = UNSET
        else:
            private_clusters = ModelPrivateCluster.from_dict(_private_clusters)

        _revision = d.pop("revision", UNSET)
        revision: Union[Unset, RevisionConfiguration]
        if isinstance(_revision, Unset):
            revision = UNSET
        else:
            revision = RevisionConfiguration.from_dict(_revision)

        _runtime = d.pop("runtime", UNSET)
        runtime: Union[Unset, Runtime]
        if isinstance(_runtime, Unset):
            runtime = UNSET
        else:
            runtime = Runtime.from_dict(_runtime)

        sandbox = d.pop("sandbox", UNSET)

        _serverless_config = d.pop("serverlessConfig", UNSET)
        serverless_config: Union[Unset, ServerlessConfig]
        if isinstance(_serverless_config, Unset):
            serverless_config = UNSET
        else:
            serverless_config = ServerlessConfig.from_dict(_serverless_config)

        agent_chain = []
        _agent_chain = d.pop("agentChain", UNSET)
        for componentsschemas_agent_chains_item_data in _agent_chain or []:
            componentsschemas_agent_chains_item = AgentChain.from_dict(componentsschemas_agent_chains_item_data)

            agent_chain.append(componentsschemas_agent_chains_item)

        description = d.pop("description", UNSET)

        functions = cast(list[str], d.pop("functions", UNSET))

        knowledgebase = d.pop("knowledgebase", UNSET)

        model = d.pop("model", UNSET)

        prompt = d.pop("prompt", UNSET)

        _repository = d.pop("repository", UNSET)
        repository: Union[Unset, Repository]
        if isinstance(_repository, Unset):
            repository = UNSET
        else:
            repository = Repository.from_dict(_repository)

        store_id = d.pop("storeId", UNSET)

        agent_spec = cls(
            configurations=configurations,
            enabled=enabled,
            flavors=flavors,
            integration_connections=integration_connections,
            pod_template=pod_template,
            policies=policies,
            private_clusters=private_clusters,
            revision=revision,
            runtime=runtime,
            sandbox=sandbox,
            serverless_config=serverless_config,
            agent_chain=agent_chain,
            description=description,
            functions=functions,
            knowledgebase=knowledgebase,
            model=model,
            prompt=prompt,
            repository=repository,
            store_id=store_id,
        )

        agent_spec.additional_properties = d
        return agent_spec

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
