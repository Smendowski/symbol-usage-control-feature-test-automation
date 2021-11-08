*** Settings ***
Library    automation_interface.py

*** Variables ***
${tdd_traces_path}    L1L2_TDD.csv
${fdd_traces_path}    L1L2_FDD.csv
@{expected_tdd_sizes}=    1    2
@{expected_fdd_sizes}=    1    2    3

*** Test Cases ***
FDD_symbol_usage_control_feature
    FOR    ${expected_size}    IN    @{expected_fdd_sizes}
        Verify_Physical_Downlink_Control_Channel_Size
        ...    path_to_l1l2_csv=${fdd_traces_path}
        ...    expected_size=${expected_size}
    END

TDD_symbol_usage_control_feature
    FOR    ${expected_size}    IN    @{expected_tdd_sizes}
        Verify_Physical_Downlink_Control_Channel_Size
        ...    path_to_l1l2_csv=${tdd_traces_path}
        ...    expected_size=${expected_size}
    END

*** Keywords ***
Verify_Physical_Downlink_Control_Channel_Size
    [Arguments]    ${path_to_l1l2_csv}    ${expected_size}
    ${expected_size}=    Convert To Integer    ${expected_size}
    ${result}=    verify_pdcch_size_without_common_channels
    ...    path_to_l1l2_csv=${path_to_l1l2_csv}
    ...    expected_size=${expected_size}
    Should Be True    ${result}
