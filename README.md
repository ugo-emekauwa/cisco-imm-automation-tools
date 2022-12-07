<h1 align="center">Cisco IMM Automation Tools</h1>

<br>
<p align="center">
  <img alt="Cisco IMM Automation Tools Title Graphic" title="Cisco IMM Automation Tools Title Graphic" src="./src/assets/Cisco_IMM_Automation_Tools_Title_Graphic.png">
</p>  
<br>
<p align="center">
  Cisco IMM Automation Tools automates the build and deployment of Cisco UCS devices, policies, pools and profiles on Cisco Intersight Infrastructure Services for UCS X-Series hardware and previous generation UCS systems such as B-Series and C-Series. The automation of UCS under Intersight Managed Mode is simplified and requires minimal programming knowledge, enabling users to setup and run quickly.
</p>
<br>

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/ugo-emekauwa/cisco-imm-automation-tools)

## Build and Deployment Tools
- [UCS Chassis Deployment Tool](./src/deployment_tools/ucs_chassis_deployment_tool) - Build, assign and deploy many UCS chassis profiles with all policies and pools in seconds.
- [UCS Default Policy Deployment Tool](./src/deployment_tools/ucs_default_policy_deployment_tool) - Quickly deploy your own set of 27 default UCS policies.
- [UCS Domain Deployment Tool](./src/deployment_tools/ucs_domain_deployment_tool) - Build, assign and deploy a UCS domain profile with all policies in minutes.
- [UCS FI Claim Handler](./src/deployment_tools/ucs_fi_claim_handler) - Claim many UCS IMM fabric interconnect clusters to an Intersight account.
- [UCS Server Deployment Tool](./src/deployment_tools/ucs_server_deployment_tool) - Build, assign and deploy many UCS server profiles, along with a template and all policies and pools in minutes.

## Policy Makers

###### For UCS Chassis
- [IMC Access Policy Maker](./src/policy_makers/imc_access_policy_maker)
- [Power Policy Maker](./src/policy_makers/power_policy_maker)
- [SNMP Policy Maker](./src/policy_makers/snmp_policy_maker)
- [Thermal Policy Maker](./src/policy_makers/thermal_policy_maker)

###### For UCS Domains
- [Ethernet Network Control Policy Maker](./src/policy_makers/ethernet_network_control_policy_maker)
- [Ethernet Network Group Policy Maker](./src/policy_makers/ethernet_network_group_policy_maker)
- [Flow Control Policy Maker](./src/policy_makers/flow_control_policy_maker)
- [Link Aggregation Policy Maker](./src/policy_makers/link_aggregation_policy_maker)
- [Link Control Policy Maker](./src/policy_makers/link_control_policy_maker)
- [Multicast Policy Maker](./src/policy_makers/multicast_policy_maker)
- [Network Connectivity Policy Maker](./src/policy_makers/network_connectivity_policy_maker)
- [NTP Policy Maker](./src/policy_makers/ntp_policy_maker)
- [Port Policy Maker](./src/policy_makers/port_policy_maker)
- [SNMP Policy Maker](./src/policy_makers/snmp_policy_maker)
- [Switch Control Policy Maker](./src/policy_makers/switch_control_policy_maker)
- [Syslog Policy Maker](./src/policy_makers/syslog_policy_maker)
- [System QoS Policy Maker](./src/policy_makers/system_qos_policy_maker)
- [VLAN Policy Maker](./src/policy_makers/vlan_policy_maker)
- [VSAN Policy Maker](./src/policy_makers/vsan_policy_maker)

###### For UCS Servers
- [BIOS Policy Maker](./src/policy_makers/bios_policy_maker)
- [Boot Order Policy Maker](./src/policy_makers/boot_order_policy_maker)
- [Certificate Management Policy Maker](./src/policy_makers/cert_mgmt_policy_maker)
- [Ethernet Adapter Policy Maker](./src/policy_makers/ethernet_adapter_policy_maker)
- [Ethernet Network Control Policy Maker](./src/policy_makers/ethernet_network_control_policy_maker)
- [Ethernet Network Group Policy Maker](./src/policy_makers/ethernet_network_group_policy_maker)
- [Ethernet QoS Policy Maker](./src/policy_makers/ethernet_qos_policy_maker)
- [FC Zone Policy Maker](./src/policy_makers/fc_zone_policy_maker)
- [Fibre Channel Adapter Policy Maker](./src/policy_makers/fibre_channel_adapter_policy_maker)
- [Fibre Channel Network Policy Maker](./src/policy_makers/fibre_channel_network_policy_maker)
- [Fibre Channel QoS Policy Maker](./src/policy_makers/fibre_channel_qos_policy_maker)
- [IMC Access Policy Maker](./src/policy_makers/imc_access_policy_maker)
- [IPMI Over LAN Policy Maker](./src/policy_makers/ipmi_over_lan_policy_maker)
- [iSCSI Adapter Policy Maker](./src/policy_makers/iscsi_adapter_policy_maker)
- [iSCSI Boot Policy Maker](./src/policy_makers/iscsi_boot_policy_maker)
- [iSCSI Static Target Policy Maker](./src/policy_makers/iscsi_static_target_policy_maker)
- [LAN Connectivity Policy Maker](./src/policy_makers/lan_connectivity_policy_maker)
- [Local User Policy Maker](./src/policy_makers/local_user_policy_maker)
- [Power Policy Maker](./src/policy_makers/power_policy_maker)
- [SAN Connectivity Policy Maker](./src/policy_makers/san_connectivity_policy_maker)
- [SD Card Policy Maker](./src/policy_makers/sd_card_policy_maker)
- [Serial Over LAN Policy Maker](./src/policy_makers/serial_over_lan_policy_maker)
- [SNMP Policy Maker](./src/policy_makers/snmp_policy_maker)
- [Storage Policy Maker](./src/policy_makers/storage_policy_maker)
- [Syslog Policy Maker](./src/policy_makers/syslog_policy_maker)
- [Virtual KVM Policy Maker](./src/policy_makers/virtual_kvm_policy_maker)
- [Virtual Media Policy Maker](./src/policy_makers/virtual_media_policy_maker)

## Pool Makers
- [IP Pool Maker](./src/pool_makers/ip_pool_maker)
- [IQN Pool Maker](./src/pool_makers/iqn_pool_maker)
- [MAC Pool Maker](./src/pool_makers/mac_pool_maker)
- [Resource Pool Maker](./src/pool_makers/resource_pool_maker)
- [UUID Pool Maker](./src/pool_makers/uuid_pool_maker)
- [WWNN Pool Maker](./src/pool_makers/wwnn_pool_maker)
- [WWPN Pool Maker](./src/pool_makers/wwpn_pool_maker)

## Base Profile and Template Makers
- [Base UCS Chassis Profile Maker](./src/profile_makers/ucs_chassis_profile_maker)
- [Base UCS Domain Profile Maker](./src/profile_makers/ucs_domain_profile_maker)
- [Base UCS Server Profile Maker](./src/profile_makers/ucs_server_profile_maker)
- [Base UCS Server Profile Template Maker](./src/profile_makers/ucs_server_profile_template_maker)

## Demonstrations and Learning Labs
Cisco IMM Automation Tools can be demoed on Cisco dCloud in the following content:

1. [Cisco Intersight with UCS X-Series Demo](https://dcloud2-rtp.cisco.com/content/instantdemo/cisco-intersight-mode-with-ucs-x-series-v1-instant-demo-2)
![Cisco UCS X-Series Demo Topology](./src/assets/Cisco_UCS_X-Series_Demo_Topology.png "Cisco UCS X-Series Demo Topology")

2. [Cisco Intersight with UCS X-Series Lab](https://dcloud2.cisco.com/demo/cisco-intersight-management-with-x-series-lab-v1)
![Cisco UCS X-Series Lab Topology](./src/assets/Cisco_UCS_X-Series_Lab_Topology.png "Cisco UCS X-Series Lab Topology")

3. Cisco Intersight with UCS B-Series Lab - Coming soon!

dCloud is available at [https://dcloud.cisco.com](https://dcloud.cisco.com), where Cisco product demonstrations and labs can be found in the Catalog.

## Author
Ugo Emekauwa

## Contact Information
uemekauw@cisco.com or uemekauwa@gmail.com
