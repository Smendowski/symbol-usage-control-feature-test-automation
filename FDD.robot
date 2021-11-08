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
[Standalone][10MHz][FR1][FDD]Symbol_usage_control_feature
    Start L1L2 packets capturing

    Register multiple UEs from UE-1 to UE-8
    Force usage of AL=2 for multiple UEs from UE-1 to UE-8
    Start 30 Mbps DL traffic for multiple UEs from UE-1 to UE-8
    Start 30 Mbps UL traffic for multiple UEs from UE-1 to UE-8
    sleep    20s

    Stop DL and UL traffic for multiple UEs from UE-1 to UE-8
    Deregister multiple UEs from UE-1 to UE-8

    Stop and Collect L1L2 packets    dir=${OUTPUT_DIR}/[2]AL2
    Convert L1L2 pcap to CSV format    dir=${OUTPUT_DIR}/[2]AL2