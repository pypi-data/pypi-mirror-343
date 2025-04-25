from sigma.pipelines.common import logsource_windows, windows_logsource_mapping
from sigma.pipelines.base import Pipeline
from sigma.processing.transformations import ChangeLogsourceTransformation, RuleFailureTransformation, DetectionItemFailureTransformation, FieldMappingTransformation
from sigma.processing.postprocessing import EmbedQueryTransformation
from sigma.processing.conditions import LogsourceCondition, IncludeFieldCondition, ExcludeFieldCondition, RuleProcessingItemAppliedCondition, RuleProcessingCondition
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline, QueryPostprocessingItem
from sigma.rule import SigmaRule

# --- Logsource helpers ----------------------------

def ls_win_proc():  
    return LogsourceCondition(category="process_creation", product="windows")

def ls_win_sec_logon():  
    return LogsourceCondition(category="authentication", product="windows", service="security")

def ls_linux_proc(): 
    return LogsourceCondition(category="process_creation", product="linux", service="rsyslog")

def ls_nginx_proxy():
    return LogsourceCondition(category="proxy", product="nginx")

def ls_generic_syslog():
    return LogsourceCondition(category="syslog")  

        
@Pipeline
# Processing pipelines should be defined as functions that return a ProcessingPipeline object.
def predictiq_pipeline() -> ProcessingPipeline:       
    """Pipeline básico con tres pasos:
    1. Cambio de propiedades de logsource
    2. Error genérico para logsources no soportados
    3. Manejo de reglas con funciones agregadas
    """
    return ProcessingPipeline(
        name="Basic SIEM Backend Pipeline",
        priority=10,
        items=[
            # 1. Windows Process Creation
            ProcessingItem(
                identifier="predict_iq_proc_fieldmap",
                transformation=FieldMappingTransformation({
                    "Image":       "process_name",
                    "ProcessId":   "process_id",
                    "CommandLine": "command_line",
                    "ParentImage": "parent_process",
                    "User":        "user",
                    "Hostname":    "hostname",
                }),
                rule_conditions=[ ls_win_proc() ],
            ),
            ProcessingItem(
                identifier="predict_iq_proc_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="process", product="windows"
                ),
                rule_conditions=[ ls_win_proc() ],
            ),
            ProcessingItem(
                identifier="predict_iq_proc_unsupported",
                transformation=DetectionItemFailureTransformation(
                    "Campo no soportado para eventos de proceso (IntegrityLevel, imphash, LogonId)"
                ),
                rule_conditions=[ ls_win_proc() ],
                field_name_conditions=[
                    IncludeFieldCondition(fields=["IntegrityLevel", "imphash", "LogonId"])
                ],
            ),

            # 2. Windows Security Logon
            ProcessingItem(
                identifier="predict_iq_logon_fieldmap",
                transformation=FieldMappingTransformation({
                    "event_id":    "event_id",
                    "user":        "user",
                    "hostname":    "hostname",
                    "ip_address":  "source_ip",
                    "log_level":   "log_level",
                }),
                rule_conditions=[ ls_win_sec_logon() ],
            ),
            ProcessingItem(
                identifier="predict_iq_logon_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="authentication", product="windows", service="security"
                ),
                rule_conditions=[ ls_win_sec_logon() ],
            ),

            # 3. Linux Process via Syslog
            ProcessingItem(
                identifier="predict_iq_linux_proc_fieldmap",
                transformation=FieldMappingTransformation({
                    "program":     "process_name",
                    "message":     "message",
                    "timestamp":   "timestamp",
                    "hostname":    "hostname",
                }),
                rule_conditions=[ ls_linux_proc() ],
            ),
            ProcessingItem(
                identifier="predict_iq_linux_proc_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="process_creation", product="linux", service="rsyslog"
                ),
                rule_conditions=[ ls_linux_proc() ],
            ),

            # 4. Nginx Proxy
            ProcessingItem(
                identifier="predict_iq_nginx_proxy_fieldmap",
                transformation=FieldMappingTransformation({
                    "cs-host":    "url_host",
                    "cs-method":  "http_method",
                    "cs-uri":     "url_path",
                    "sc-status":  "status_code",
                    "src_ip":     "source_ip",
                    "dst_ip":     "destination_ip",
                }),
                rule_conditions=[ ls_nginx_proxy() ],
            ),
            ProcessingItem(
                identifier="predict_iq_nginx_proxy_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="proxy", product="nginx"
                ),
                rule_conditions=[ ls_nginx_proxy() ],
            ),

            # 5. Generic Syslog 
            ProcessingItem(
                identifier="predict_iq_syslog_fieldmap",
                transformation=FieldMappingTransformation({
                    "timestamp": "timestamp",
                    "hostname":  "host",
                    "program":   "process_name",
                    "pri":       "severity",
                    "msg":       "message",
                    "raw":       "raw_log",
                }),
                rule_conditions=[ ls_generic_syslog() ],
            ),
            ProcessingItem(
                identifier="predict_iq_syslog_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="syslog"
                ),
                rule_conditions=[ ls_generic_syslog() ],
            ),

            # 6. Catch-all to unsupported log sources
            ProcessingItem(
                identifier="predict_iq_unsupported_rule",
                transformation=RuleFailureTransformation(
                    "Tipo de log aún no soportado por PredicIQ SIEM"
                ),
                rule_condition_negation=True,
                rule_conditions=[
                    RuleProcessingItemAppliedCondition("predict_iq_proc_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_logon_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_linux_proc_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_nginx_proxy_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_syslog_logsource"),
                ],
            ),
        ],
    )