#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
# jinjia2

# 虚拟机告警策略类型：
# CPU使用率    正常：VmCpuUsageNormal，警告：VmCpuUsageWaring，危险：VmCpuUsageDanger，严重：VmCpuUsageCritical
# 内存可用量    正常：VmMemUsageNormal，警告：VmMemUsageWarning，危险：VmMemUsageDanger，严重：VmMemUsageCritical
# 网络下行速率    正常：VmNetResvSpeedNormal，警告：VmNetResvSpeedWaring，危险：VmNetResvSpeedDanger，严重：VmNetResvSpeedCritical
# 网络上行速率    正常：VmNetSEendSpeedNormal，警告：VmNetSEendSpeedWaring，危险：VmNetSEendSpeedDDanger，严重：VmNetSEendSpeedCritical
# 磁盘读速率    正常：VmDiskReadSpeedNormal，警告：VmDiskReadSpeedWaring，危险：VmDiskReadSpeedDanger，严重：VmDiskReadSpeedCritical
# 磁盘写速率    正常：VmDiskWriteSpeedNormal，警告：VmDiskWriteSpeedWaring，危险：VmDiskWriteSpeedDanger，严重：VmDiskWriteSpeedCritical
# 磁盘读IOPS    正常：VmDiskReadIopsNormal，警告：VmDiskReadIopsWaring，危险：VmDiskReadIopsDanger，严重：VmDiskReadIopsCritical
# 磁盘写IOPS    正常：VmDiskWriteIopsNormal，警告：VmDiskWriteIopsWaring，危险：VmDiskWriteIopsDanger，严重：VmDiskWriteIopsCritical

# 宿主机告警策略类型：
# CPU使用率           正常：HostCpuUsageNormal,警告：HostCpuUsageWaring,危险：HostCpuUsageDanger，严重：HostCpuUsageCritical
# 内存可用量          正常：HostMemUsageNormal,警告：HostMemUsageWarning,危险：HostMemUsageDanger，严重：HostMemUsageCritical
# 网络下行速率        正常：HostNetResvSpeedNormal,警告：HostNetResvSpeedWaring,危险：HostNetResvSpeedDanger，严重：HostNetResvSpeedCritical
# 网络上行速率        正常：HostNetSendSpeedNormal,警告：HostNetSendSpeedWaring,危险：HostNetSendSpeedDanger，严重：HostNetSendSpeedCritical
# 磁盘使用率          正常：HostDiskUsageNormal,警告：HostDiskUsageWaring,危险：HostDiskUsageDanger，严重：HostDiskUsageCritical
# 磁盘读速率          正常：HostDiskReadSpeedNormal,警告：HostDiskReadSpeedWaring,危险：HostDiskReadSpeedDanger，严重：HostDiskReadSpeedCritical
# 磁盘写速率          正常：HostDiskWriteSpeedNormal,警告：HostDiskWriteSpeedWaring,危险：HostDiskWriteSpeedDanger，严重：HostDiskWriteSpeedCritical

# example = '''
# ALERT VmCpuUsageWaring
#   IF rate(libvirt_vm_cpu_time{vm_uuid='1798870d-0525-4e7d-ac0d-6b19197ff5b9', job="telegraf"}[1m])*60 > 1
#   AND  rate(libvirt_vm_cpu_time{vm_uuid='1798870d-0525-4e7d-ac0d-6b19197ff5b9', job="telegraf"}[1m])*60 > 0
#   FOR 1m
#   LABELS { severity="warning", meterId="23", group="user" }
#   ANNOTATIONS {
#     summary = "虚拟机1798870d-0525-4e7d-ac0d-6b19197ff5b9 CPU使用率大于1%",
#     description = "23@warning告警，在最近的1m内，监控到虚拟机1798870d-0525-4e7d-ac0d-6b19197ff5b9 CPU使用率大于1%.",
#   }
# '''
templates = {
# 虚拟机CPU使用率
'VmCpuUsage': '''
ALERT {type}
  IF rate(libvirt_vm_cpu_time{{vm_uuid='{vmUuid}', job="telegraf"}}[1m])*60 {operator} {metervalue}
  AND  rate(libvirt_vm_cpu_time{{vm_uuid='{vmUuid}', job="telegraf"}}[1m])*60 > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机CPU使用率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到虚拟机{vmUuid} CPU使用率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群CPU使用率
'ClusterCpuUsage': '''
ALERT {type}
  IF avg(rate(libvirt_vm_cpu_time{{vm_cluster='{vmClusterUuid}', job="telegraf"}}[1m])*60)by(vm_cluster) {operator} {metervalue}
  AND  avg(rate(libvirt_vm_cpu_time{{vm_cluster='{vmClusterUuid}', job="telegraf"}}[1m])*60)by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群CPU使用率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到集群{vmClusterUuid} CPU使用率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机内存可用量
'VmMemUsage': '''
ALERT {type}   
  IF libvirt_vm_unused{{vm_uuid='{vmUuid}', job="telegraf"}}*1024 {operator} {metervalue}*1024*1024
  AND  libvirt_vm_unused{{vm_uuid='{vmUuid}', job="telegraf"}}*1024 > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机内存可用量{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到虚拟机{vmUuid} 内存可用量{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群内存可用量
'ClusterMemUsage': '''
ALERT {type}   
  IF avg(libvirt_vm_unused{{vm_cluster='{vmClusterUuid}', job="telegraf"}}*1024)by(vm_cluster) {operator} {metervalue}*1024*1024
  AND  avg(libvirt_vm_unused{{vm_cluster='{vmClusterUuid}', job="telegraf"}}*1024)by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群内存可用量{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到集群{vmClusterUuid} 内存可用量{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机网络下行速率
'VmNetResvSpeed': '''
ALERT {type}
  IF rate(libvirt_vm_rx_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[45s]) {operator} {metervalue}*1024*1024
  AND rate(libvirt_vm_rx_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[45s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机网络接收速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}内，监控到虚拟机{vmUuid} 网卡下行速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群网络下行速率
'ClusterNetResvSpeed': '''
ALERT {type}
  IF avg(rate(libvirt_vm_rx_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[45s]))by(vm_cluster) {operator} {metervalue}*1024*1024
  AND avg(rate(libvirt_vm_rx_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[45s]))by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群网络接收速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}内，监控到集群{vmClusterUuid} 网卡下行速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机网络上行速率
'VmNetSEendSpeed': '''
ALERT {type}
  IF rate(libvirt_vm_tx_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[45s]) {operator} {metervalue}*1024*1024
  AND rate(libvirt_vm_tx_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[45s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机网络发送速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}内，监控到虚拟机{vmUuid} 网卡上行速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群网络上行速率
'ClusterNetSEendSpeed': '''
ALERT {type}
  IF avg(rate(libvirt_vm_tx_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[45s]))by(vm_cluster) {operator} {metervalue}*1024*1024
  AND avg(rate(libvirt_vm_tx_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[45s]))by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群网络发送速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}内，监控到集群{vmClusterUuid} 网卡上行速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机磁盘读速率
'VmDiskReadSpeed': '''
ALERT {type}
  IF rate(libvirt_vm_rd_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[30s]) {operator} {metervalue}*1024*1024
  AND rate(libvirt_vm_rd_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[30s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机硬盘读速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到虚拟机{vmUuid} 本地硬盘读速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群磁盘读速率
'ClusterDiskReadSpeed': '''
ALERT {type}
  IF avg(rate(libvirt_vm_rd_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s]))by(vm_cluster) {operator} {metervalue}*1024*1024
  AND avg(rate(libvirt_vm_rd_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s]))by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群硬盘读速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到集群{vmClusterUuid} 本地硬盘读速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机磁盘写速率
'VmDiskWriteSpeed': '''
ALERT {type}
  IF rate(libvirt_vm_wr_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[30s]) {operator} {metervalue}*1024*1024
  AND rate(libvirt_vm_wr_bytes{{vm_uuid='{vmUuid}',job="telegraf"}}[30s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机硬盘写速率超过{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到虚拟机{vmUuid} 本地硬盘写速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群磁盘写速率
'ClusterDiskWriteSpeed': '''
ALERT {type}
  IF avg(rate(libvirt_vm_wr_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s]))by(vm_cluster) {operator} {metervalue}*1024*1024
  AND avg(rate(libvirt_vm_wr_bytes{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s]))by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群硬盘写速率超过{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到集群{vmClusterUuid} 本地硬盘写速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机磁盘读IOPS
'VmDiskReadIops': '''
ALERT {type}
  IF stddev_over_time(libvirt_vm_rd_req{{vm_uuid='{vmUuid}',job="telegraf"}}[30s])/(2.7*30) {operator} {metervalue}
  AND stddev_over_time(libvirt_vm_rd_req{{vm_uuid='{vmUuid}',job="telegraf"}}[30s])/(2.7*30) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机硬盘读IOPS{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到虚拟机{vmUuid} 本地硬盘读IOPS{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群磁盘读IOPS
'ClusterDiskReadIops': '''
ALERT {type}
  IF avg(stddev_over_time(libvirt_vm_rd_req{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s])/(2.7*30))by(vm_cluster) {operator} {metervalue}
  AND avg(stddev_over_time(libvirt_vm_rd_req{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s])/(2.7*30))by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群硬盘读IOPS{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到集群{vmClusterUuid} 本地硬盘读IOPS{operator_zh}{metervalue}{unit}.",
  }}
''',

# 虚拟机磁盘写IOPS
'VmDiskWriteIops': '''
ALERT {type}
  IF stddev_over_time(libvirt_vm_wr_req{{vm_uuid='{vmUuid}',job="telegraf"}}[30s])/(2.7*30) {operator} {metervalue}
  AND stddev_over_time(libvirt_vm_wr_req{{vm_uuid='{vmUuid}',job="telegraf"}}[30s])/(2.7*30) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "虚拟机硬盘写IOPS{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到虚拟机{vmUuid} 本地硬盘写IOPS{operator_zh}{metervalue}{unit}.",
  }}
''',

# 集群磁盘写IOPS
'ClusterDiskWriteIops': '''
ALERT {type}
  IF avg(stddev_over_time(libvirt_vm_wr_req{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s])/(2.7*30))by(vm_cluster) {operator} {metervalue}
  AND avg(stddev_over_time(libvirt_vm_wr_req{{vm_cluster='{vmClusterUuid}',job="telegraf"}}[30s])/(2.7*30))by(vm_cluster) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "集群硬盘写IOPS{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}分钟内，监控到集群{vmClusterUuid} 本地硬盘写IOPS{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机CPU使用率：
'HostCpuUsage': '''
ALERT {type}
  IF 100 - cpu_usage_idle{{host='{hostname}', job="telegraf"}} {operator} {metervalue}
  AND 100 - cpu_usage_idle{{host='{hostname}', job="telegraf"}} > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机CPU使用比例{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到主机{hostname} CPU使用率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机内存可用量(只支持GB):
'HostMemUsage': '''
ALERT {type}
  IF mem_available{{host='{hostname}', job="telegraf"}} {operator} {metervalue}*1024*1024*1024
  AND  mem_available{{host='{hostname}', job="telegraf"}} > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机内存可用量{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到主机节点{hostname} 内存可用量{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机磁盘使用率
'HostDiskUsage': '''
ALERT {type}
  IF disk_used_percent{{host='{hostname}', job="telegraf"}} {operator} {metervalue}
  AND disk_used_percent{{host='{hostname}', job="telegraf"}} > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机磁盘使用率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}内，监控到主机{hostname} 磁盘使用率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机网络下行速率：
'HostNetResvSpeed': '''
ALERT {type}
  IF rate(net_bytes_recv{{host='{hostname}', job="telegraf"}}[45s]) {operator} {metervalue} * 1024 * 1024
  AND rate(net_bytes_recv{{host='{hostname}', job="telegraf"}}[45s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机网络接收速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警，在最近的{period}{clock}分钟内，监控到主机{hostname} 网卡下行速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机网络上行速率：
'HostNetSendSpeed': '''
ALERT {type}
  IF rate(libvirt_vm_tx_bytes{{host='{hostname}', job="telegraf"}}[45s]) {operator} {metervalue}*1024*1024
  AND rate(libvirt_vm_tx_bytes{{host='{hostname}', job="telegraf"}}[45s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机网络发送速率{operator_zh}{metervalue}{unit}",
    description = "{severity}告警,在最近的{period}{clock}内，监控到主机{hostname} 网卡上行速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机磁盘读速率
'HostDiskReadSpeed': '''
ALERT {type}
  IF rate(diskio_read_bytes{{host='{hostname}', job="telegraf"}}[30s]) {operator} {metervalue}*1024*1024
  AND rate(diskio_read_bytes{{host='{hostname}', job="telegraf"}}[30s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机本地硬盘读速率{operator_zh}{metervalue}{unit}",
    description = "{severity}警告，在最近的{period}{clock}分钟内，监控到主机{hostname} 本地硬盘读速率{operator_zh}{metervalue}{unit}.",
  }}
''',

# 主机磁盘写速率
'HostDiskWriteSpeed': '''
ALERT {type}
  IF rate(diskio_write_bytes{{host='{hostname}', job="telegraf"}}[30s]) {operator} {metervalue}*1024*1024
  AND rate(diskio_write_bytes{{host='{hostname}', job="telegraf"}}[30s]) > 0
  FOR {period}{clock}
  LABELS {{ severity="{severity}", meterId="{meterId}", group="{group}" }}
  ANNOTATIONS {{
    summary = "主机本地硬盘写速率{operator_zh}{metervalue}{unit}",
    description = "{severity}警告，在最近的{period}{clock}分钟内，监控到主机{hostname} 本地硬盘写速率{operator_zh}{metervalue}{unit}.",
  }}
''',
}

def generate_rule(kwargs):
    expected_keys = {'clock', 'severity', 'vmUuid', 'operator', 'period',
        'metervalue', 'unit',  'meterId', 'group', 'hostname', 'type'}  # set
    if set(kwargs.keys()) != expected_keys:
        return
    rule_type = kwargs['type']
    key = ''
    for k in templates.keys():
        if rule_type.startswith(k):
            key = k
    template = templates.get(key)
    if template is None:
        return
    else:
        if kwargs['operator'] == '<':
            operator_zh = '小于'
        elif kwargs['operator'] == '>':
            if 'Usage' in kwargs['type']:
                operator_zh = '大于'
            else:
                operator_zh = '超过'
        else:
            operator_zh = kwargs['operator']
        rule = template.format(operator_zh=operator_zh, **kwargs).lstrip()
        return rule


if __name__ == '__main__':

    request = {
        "clock": "m",
        "severity": "warning",
        "vmUuid": "1798870d-0525-4e7d-ac0d-6b19197ff5b9",
        "operator": ">",
        "period": 1,
        "metervalue": 1,
        "unit": "%",
        "meterId": "23",
        "group": "user",
        "hostname": "sugon.local",
        "type": "VmCpuUsageWaring"
    }

    print generate_rule(request)
