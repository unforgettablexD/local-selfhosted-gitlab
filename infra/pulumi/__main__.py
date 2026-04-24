import pulumi
import pulumi_kubernetes as k8s

config = pulumi.Config()
namespace_name = config.get("namespace") or "pulumi-managed-lab"
context = config.get("context") or "kind-devsecops-lab"

provider = k8s.Provider(
    "kind-provider",
    context=context,
)

namespace = k8s.core.v1.Namespace(
    "platform-namespace",
    metadata={"name": namespace_name, "labels": {"managed-by": "pulumi"}},
    opts=pulumi.ResourceOptions(provider=provider),
)

configmap = k8s.core.v1.ConfigMap(
    "platform-configmap",
    metadata={"name": "platform-config", "namespace": namespace.metadata["name"]},
    data={"app_env": "pulumi-local", "owner": "devsecops-lab"},
    opts=pulumi.ResourceOptions(provider=provider),
)

pulumi.export("namespace", namespace.metadata["name"])
pulumi.export("configmap", configmap.metadata["name"])
