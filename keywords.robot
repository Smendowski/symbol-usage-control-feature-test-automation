*** Keywords ***
Wait until Base Station Status is Ready
    [Documentation]    Waiting Untill Base Station Status Is Ready
    sleep    10s
    # INTERNAL IMPLEMENTATION

Prepare Core Network Configuration File for multiple SA UEs
    [Documentation]    Prepare Core Network Configuration File for multiple SA UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Start Core Network Application and Load Configuration File
    [Documentation]    Start Core Network Application and Load Configuration File
    sleep    10s
    # INTERNAL IMPLEMENTATION

Wait until Cell Status is Online
    [Documentation]    Wait until Cell Status is Online
    sleep    10s
    # INTERNAL IMPLEMENTATION

Wait until NG Link Status is Ready
    [Documentation]    Wait until NG Link Status is Ready
    sleep    10s
    # INTERNAL IMPLEMENTATION

Verify Cell Setup and System Information Blocks
    [Documentation]    Verify Cell Setup and System Information Blocks
    sleep    10s
    # INTERNAL IMPLEMENTATION

Setup L1L2 Packets Capturing
    [Documentation]    Setup L1L2 Packets Capturing
    sleep    10s
    # INTERNAL IMPLEMENTATION

Close Core Network Connections
    [Documentation]    Close Core Network Connections
    sleep    10s
    # INTERNAL IMPLEMENTATION

Start L1L2 packets capturing
    [Documentation]    Start L1L2 packets capturing
    sleep    10s
    # INTERNAL IMPLEMENTATION

Register multiple UEs from UE-${ue_start_idx} to UE-${ue_stop_idx}
    [Documentation]    Register multiple UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Deregister multiple UEs from UE-${ue_start_idx} to UE-${ue_stop_idx}
    [Documentation]    Register multiple UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Allow usage of AL=${fitst_al} and AL=${second_al} for multiple UEs from UE-${ue_start_idx} to UE-${ue_stop_idx}
    [Documentation]    Allow usage of specified aggregation levels for multiple UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Force usage of AL=${al} for multiple UEs from UE-${ue_start_idx} to UE-${ue_stop_idx}
    [Documentation]    Force usage of specified aggregation levels for multiple UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Start ${traffic} ${unit} ${direction} traffic for multiple UEs from UE-${ue_start_idx} to UE-${ue_stop_idx}
    [Documentation]    Start DL or UL traffic for multiple UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Stop DL and UL traffic for multiple UEs from UE-${ue_start_idx} to UE-${ue_stop_idx}
    [Documentation]    Stop DL and UL traffic for multiple UEs
    sleep    10s
    # INTERNAL IMPLEMENTATION

Stop and Collect L1L2 packets
    [Documentation]    Stop and Collect L1L2 packets
    [Arguments]    ${dir}
    sleep    10s
    # INTERNAL IMPLEMENTATION

Convert L1L2 pcap to CSV format
    [Documentation]    Convert L1L2 pcap to CSV format
    [Arguments]    ${dir}
    sleep    10s
    # INTERNAL IMPLEMENTATION