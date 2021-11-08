*** Settings ***
Library    utils.py

*** Variables ***
&{RRH}    Username=********    Hostname=192.168.200.1    Password=********

*** Test Cases ***
Compare_radio_head_gscn_with_base_station_configuration

    ${rrh_gscn}=    get_gscn_from_rrh_config
    ...    username=${RRH['Username']}
    ...    hostname=${RRH['Hostname']}
    ...    password=${RRH['Password']}

    ${gnb_gscn}=    get_gscn_from_bs_config
    ...    configuration_file_path=/gNB_config.xml

    Should be equal    ${rrh_gscn}    ${gnb_gscn}

*** Keywords ***
# No custom keywords implemented.