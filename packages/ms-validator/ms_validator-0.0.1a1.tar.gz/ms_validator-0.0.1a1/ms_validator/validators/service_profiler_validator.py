from .base_validator import BaseValidator
from ..utils import msg_wrapper


class ServiceProfilerValidator(BaseValidator):
    def get_func_name(self):
        return "service_profiler_validator"

    def generate_func_body(self):
        check_mapping = {
            "libmindieservice_endpoint.so": ("/usr/local/Ascend/mindie/latest/mindie-service/lib/libmindieservice_endpoint.so", ["httpReq", "httpRes"]),
            "libmindie_llm_ibis.so": ("/usr/local/Ascend/mindie/latest/mindie-service/lib/libmindie_llm_ibis.so", ["batchFrameworkProcessing"]),
            "libmindie_llm_backend_model.so": ("/usr/local/Ascend/mindie/latest/mindie-service/lib/libmindie_llm_backend_model.so", ["setInferBuffer", "grpcWriteToSlave", "receiveInfer", "deserializeExecuteResponse"]),
            "mindie_llm_backend_connector": ("/usr/local/Ascend/mindie/latest/mindie-service/bin/mindie_llm_backend_connector", ["convertTensorBatchToBackend", "processPythonExecResult", "deserializeExecuteRequestsForInfer"]),
            "standard_model.py": ("/usr/local/lib/python3.11/site-packages/model_wrapper/standard_model.py", ["getInputMetadata", "generateOutput"]),
            "flash_causal_deepseekv2.py": ("/usr/local/Ascend/atb-models/atb_llm/models/deepseekv2/flash_causal_deepseekv2.py", ["operatorExecute", "prepareInputs"])
        }

        def generate_check_block(checkee, check_path, check_items):
            sub_cmd = f"""
            if [ ! -f {check_path} ]; then
                echo "ERROR - {check_path} not found" >&2
            else
                echo {msg_wrapper(checkee)}
            """
            sub_cmd += "\n".join(
                f"""
                if ! grep -i {check_item} > /dev/null 2>&1; then
                    echo "WARNING - {check_item} missing"
                fi
                """ for check_item in check_items
            )
            sub_cmd += "fi\n"
            return sub_cmd

        cmd = "function service_profiler_validator() {\n"
        for checkee, (check_path, check_items) in check_mapping.items():
            cmd += generate_check_block(checkee, check_path, check_items)
        cmd += "}\n"

        return cmd
