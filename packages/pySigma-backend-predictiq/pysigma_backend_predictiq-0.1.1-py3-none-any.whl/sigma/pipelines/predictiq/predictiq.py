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

def ls_win_file_access():
    return LogsourceCondition(category="file_access", product="windows")

def ls_win_file_event() -> LogsourceCondition:
    return LogsourceCondition(category="file_event", product="windows")

def ls_win_netconn():
    return LogsourceCondition(category="network_connection", product="windows")

def ls_win_image_load():
    return LogsourceCondition(category="image_load", product="windows")

def ls_win_ps_module():
    return LogsourceCondition(category="ps_module", product="windows")

def ls_win_firewall_as():
    return LogsourceCondition(service="firewall-as", product="windows")

def ls_win_security():
    return LogsourceCondition(service="security", product="windows")

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

            # 6-BIS.  Windows file_event  (.evtx created in uncommon location)
            ProcessingItem(
                identifier="predict_iq_file_access_fieldmap",
                transformation=FieldMappingTransformation({
                    "FileName":   "file_name",
                    "Image":      "process_name",
                    "ProcessId":  "process_id",
                    "User":       "user",
                    "Hostname":   "hostname",
                }),
                rule_conditions=[ ls_win_file_access() ],
            ),

            ProcessingItem(
                identifier="predict_iq_file_access_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="file_access", product="windows"
                ),
                rule_conditions=[ ls_win_file_access() ],
            ),

            ProcessingItem(
                identifier="predict_iq_file_event_fieldmap",
                transformation=FieldMappingTransformation({
                    # map Sysmon-style field names to your unified schema
                    "TargetFilename": "file_path",
                    "Image":          "process_name",
                    "ProcessId":      "process_id",
                    "User":           "user",
                    "Hostname":       "hostname",
                }),
                rule_conditions=[ ls_win_file_event() ],
            ),
            ProcessingItem(
                identifier="predict_iq_file_event_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="file_event", product="windows"
                ),
                rule_conditions=[ ls_win_file_event() ],
            ),

            # 7. Windows Network Connection
            ProcessingItem(
                identifier="predict_iq_netconn_fieldmap",
                transformation=FieldMappingTransformation({
                    "Initiated":           "initiated",           # true/false
                    "Image":               "process_name",
                    "DestinationHostname": "destination_host",
                    "DestinationIp":       "destination_ip",
                    "SourceIp":            "source_ip",
                    "SourcePort":          "source_port",
                    "DestinationPort":     "destination_port",
                    # añade aquí otros campos que quieras exponer…
                }),
                rule_conditions=[ ls_win_netconn() ],
            ),

            ProcessingItem(
                identifier="predict_iq_netconn_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="network_connection", product="windows"
                ),
                rule_conditions=[ ls_win_netconn() ],
            ),

            # 8. Windows Image Load (DLLs)
            ProcessingItem(
                identifier="predict_iq_image_load_fieldmap",
                transformation=FieldMappingTransformation({
                    "Image":       "process_name",   # proceso que carga la DLL
                    "ImageLoaded": "dll_path",       # ruta del módulo DLL cargado
                    "ProcessId":   "process_id",
                    "User":        "user",
                    "Hostname":    "hostname",
                }),
                rule_conditions=[ ls_win_image_load() ],
            ),
            ProcessingItem(
                identifier="predict_iq_image_load_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="image_load", product="windows"
                ),
                rule_conditions=[ ls_win_image_load() ],
            ),

            # 9. Windows PS Module
            ProcessingItem(
                identifier="predict_iq_ps_module_fieldmap",
                transformation=FieldMappingTransformation({
                    "Payload":     "script_content",  # o el nombre de campo que uses para el contenido del módulo
                }),
                rule_conditions=[ ls_win_ps_module() ],
            ),
            ProcessingItem(
                identifier="predict_iq_ps_module_logsource",
                transformation=ChangeLogsourceTransformation(
                    category="ps_module", product="windows"
                ),
                rule_conditions=[ ls_win_ps_module() ],
            ),

            # 10. Windows Firewall (Advanced Security)
            ProcessingItem(
                identifier="predict_iq_firewall_fieldmap",
                transformation=FieldMappingTransformation({
                    "EventID":             "event_id",
                    "ModifyingApplication": "mod_app_path",
                    "User":                "user",
                    "Hostname":            "hostname",
                }),
                rule_conditions=[ ls_win_firewall_as() ],
            ),
            ProcessingItem(
                identifier="predict_iq_firewall_logsource",
                transformation=ChangeLogsourceTransformation(
                    product="windows", service="firewall-as"
                ),
                rule_conditions=[ ls_win_firewall_as() ],
            ),

            # 11. Kerberos Authentication (Windows Security)
            ProcessingItem(
                identifier="predict_iq_security_fieldmap",
                transformation=FieldMappingTransformation({
                    "EventID":               "event_id",
                    "TicketOptions":         "ticket_options",
                    "TicketEncryptionType":  "ticket_encryption",
                    "ServiceName":           "service_name",
                    "User":                  "user",
                    "Hostname":              "hostname",
                }),
                rule_conditions=[ ls_win_security() ],
            ),
            ProcessingItem(
                identifier="predict_iq_security_logsource",
                transformation=ChangeLogsourceTransformation(
                    product="windows", service="security"
                ),
                rule_conditions=[ ls_win_security() ],
            ),

            # Catch-all to unsupported log sources
            ProcessingItem(
                identifier="predict_iq_unsupported_rule",
                transformation=RuleFailureTransformation(
                    "Tipo de log aún no soportado por PredicIQ SIEM"
                ),
                rule_condition_negation=True,
                rule_condition_linking=any,
                rule_conditions=[
                    RuleProcessingItemAppliedCondition("predict_iq_proc_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_logon_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_linux_proc_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_nginx_proxy_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_syslog_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_file_access_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_file_event_logsource"),  
                    RuleProcessingItemAppliedCondition("predict_iq_netconn_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_image_load_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_ps_module_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_firewall_logsource"),
                    RuleProcessingItemAppliedCondition("predict_iq_security_logsource"),
                ],
            ),
        ],
    )