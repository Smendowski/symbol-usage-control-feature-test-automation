*** Settings ***
Resource    keywords.robot

Suite Setup    Run Keywords
...            Wait untill Base Station Status is Ready
...            Prepare Core Network Configuration File for multiple SA UEs
...            Start Core Network Application and Load Configuration File
...            Wait untill Cell Status is Online
...            Wait untill NG Link Status is Ready
...            Verify Cell Setup and System Information Blocks
...            Setup L1L2 Packets Capturing

Suite Teardown    Run Keyword and Ignore Error
...               Close Core Network Connections

*** Test Cases ***
[Standalone][20MHz][FR1][TDD]Symbol_usage_control_feature
    Start L1L2 packets capturing

    Register multiple UEs from UE-1 to UE-4
    Allow usage of AL=2 and AL=4 for multiple UEs from UE-1 to UE-4
    Start 600 Mbps DL traffic for multiple UEs from UE-1 to UE-2
    Start 60 Mbps UL traffic for multiple UEs from UE-1 to UE-2
    Start 64 Kbps DL traffic for multiple UEs from UE-3 to UE-4
    Start 30 Kbps UL traffic for multiple UEs from UE-3 to UE-4
    sleep    20s

    Force usage of AL=8 for multiple UEs from UE-3 to UE-4
    sleep    20s

    Stop DL and UL traffic for multiple UEs from UE-1 to UE-4
    Deregister multiple UEs from UE-1 to UE-4

    Stop and Collect L1L2 packets    dir=${OUTPUT_DIR}/[1]AL2_AL4_AL8
    Convert L1L2 pcap to CSV format    dir=${OUTPUT_DIR}/[1]AL2_AL4_AL8