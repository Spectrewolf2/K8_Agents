import json
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_nodes_via_client(kubeconfig_path=None):
    try:
        if kubeconfig_path and kubeconfig_path != "None":
            config.load_kube_config(config_file=kubeconfig_path)
        else:
            try:
                config.load_incluster_config()
            except config.ConfigException:
                config.load_kube_config()
    except Exception as e:
        return {"success": False, "error": f"Config load error: {str(e)}"}

    v1 = client.CoreV1Api()
    try:
        nodes = [node.metadata.name for node in v1.list_node().items]
        return {"success": True, "nodes": nodes}
    except ApiException as e:
        return {"success": False, "error": f"K8s API error ({e.status}): {e.reason}"}

if __name__ == "__main__":
    kubeconfig_path = sys.argv[1] if len(sys.argv) > 1 else None
    result = get_nodes_via_client(kubeconfig_path)
    print(json.dumps(result))
