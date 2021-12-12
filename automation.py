import csv
import json
import copy
import re
from collections import defaultdict

allocation_expressions = {
    "SI": r'(grant[\s\w]+).+(coreSet=\d+).+(startSymb=\d+).+(nbSymb=\d).+'
          r'(searchSpace=[\w\s\d-]+).+(rnti=.+)',

    "DL_UL": r'(.+grant\s[01-]{3}).+(nbPrb=\d+).+(startCce=\d+).+(AL=\d+).+'
             r'(coreSet=\d+).+(startPDCCHSymbol=\d+).+(nbPDCCHSymbol=\d+).+'
             r'(searchSpace=[\w\s\d-]+).+(rnti=.+)',

    "MSG3": r'(grant\srach\sMsg3).+(coreSet=\d+).+(startSymb=\d+).+'
            r'(nbSymb=\d+).+(searchSpace=[\w\s\d-]+)',

    "PDSCH": r'.+(startPrb=\d+).+(startPDSCHSymbol=\d+).+(nbPDSCHSymbols=\d+).+'
}


class Parser(object):
    @staticmethod
    def convert_l1l2_csv_traces(path_to_l1l2_csv: str) -> dict:
        with open(path_to_l1l2_csv, "r") as csv_traces:
            csv_reader = csv.reader(csv_traces, delimiter=';')
            next(csv_reader, None)
            traces = defaultdict(list)

            for row in csv_reader:
                tti = row[0]
                message_id = row[9]
                message_content = ",rnti=".join([row[11], row[8]])

                if tti in traces:
                    if message_id in traces[tti].keys():
                        traces[tti][message_id].append(message_content)
                    else:
                        traces[tti][message_id] = [message_content]
                else:
                    traces.update({tti: {message_id: [message_content]}})
        return dict(traces)

    @staticmethod
    def remove_non_dl_send_request_messages(l1l2_traces: dict) -> dict:
        send_request_traces = copy.deepcopy(l1l2_traces)

        for tti, data in l1l2_traces.items():
            for message_id, component_messages in data.items():
                if message_id not in ['Dl PdcchSendReq(29)', 'Dl PdschSendReq(30)', 'Dl PdcchSendReq(31)']:
                    try:
                        del send_request_traces[tti][message_id]
                        if not send_request_traces[tti]:
                            del send_request_traces[tti]
                    except KeyError:
                        print(f"[!] Cannot remove {message_id} associated with {tti} tti.")
        return send_request_traces

    @staticmethod
    def extract_dl_send_request_messages(l1l2_traces: dict) -> dict:
        filtered_traces = copy.deepcopy(l1l2_traces)

        for tti, data in l1l2_traces.items():
            for message_id, component_messages in data.items():
                filtered_traces[tti][message_id] = Parser.filter_dl_send_request_messages(component_messages)

        return filtered_traces

    @staticmethod
    def filter_dl_send_request_messages(component_messages: list) -> list:
        filtered_messages = []

        for message in component_messages:
            content_indicator = message.split(',')[0]
            if content_indicator == "grant for SI rnti":
                filtered_messages.append(
                    Parser.filter_allocation_content(
                        message, allocation_expressions["SI"]
                    )
                )
            elif content_indicator in ["DL grant 1-1", "UL grant 0-1"]:
                filtered_messages.append(
                    Parser.filter_allocation_content(
                        message, allocation_expressions["DL_UL"]
                    )
                )
            elif "codeBooki" in content_indicator:
                filtered_messages.append(
                    Parser.filter_allocation_content(g
                        message, allocation_expressions["PDSCH"]
                    )
                )
            elif "grant rach Msg3" in content_indicator:
                filtered_messages.append(
                    Parser.filter_allocation_content(
                        message, allocation_expressions["MSG3"]
                    )
                )
        return filtered_messages

    @staticmethod
    def filter_allocation_content(message: str, expression: str) -> str:
        pattern = re.compile(expression)
        return ",".join(pattern.findall(message)[0])

    @staticmethod
    def convert_traces_to_json(traces: dict) -> str:
        return json.dumps(traces)


class Verifier(object):
    @staticmethod
    def get_traces_with_specific_content(traces: dict, to_keep: str) -> dict:
        traces_with_content = {}
        for tti, data in traces.items():
            for _, message_content in data.items():
                if any([x for x in message_content if to_keep in x]):
                    traces_with_content.update({tti: traces[tti]})
        return traces_with_content

    @staticmethod
    def get_traces_without_specific_content(traces: dict, to_skip: str):
        traces_without_content = copy.deepcopy(traces)
        for tti, data in traces.items():
            for _, message_content in data.items():
                if any([x for x in message_content if to_skip in x]):
                    del traces_without_content[tti]
        return traces_without_content

    @staticmethod
    def get_traces_with_dl_grant_and_without_common_channel(traces: dict):
        return Verifier.get_traces_with_specific_content(
            Verifier.get_traces_without_specific_content(
                traces, to_skip="grant for SI rnti"
            ),
            to_keep="DL grant 1-1"
        )

    @staticmethod
    def get_traces_with_dl_grant_and_with_common_channel(traces: dict):
        return Verifier.get_traces_with_specific_content(
            Verifier.get_traces_with_specific_content(
                traces, to_keep="grant for SI rnti"
            ),
            to_keep="DL grant 1-1"
        )

    @staticmethod
    def get_matched_pattern_content(content: str, reg_exp: str):
        pattern = re.compile(reg_exp)
        return pattern.findall(content)

    @staticmethod
    def verify_pdcch_size_without_common_channels(traces, expected_pdcch_size):
        traces_to_verify = Verifier.get_traces_with_dl_grant_and_without_common_channel(traces)
        traces_with_expected_pdcch_size = []

        for tti, data in traces_to_verify.items():
            start_pdcch_symbols = []
            nb_pdcch_symbols = []
            start_pdsch_symbols = []

            for message_id, message_content in data.items():
                message_content_merged = ",".join(message_content)

                if message_id in ["Dl PdcchSendReq(29)", "Dl PdcchSendReq(31)"]:
                    for match in Verifier.get_matched_pattern_content(message_content_merged, r'startPDCCHSymbol=(\d)'):
                        start_pdcch_symbols.append(match)
                    for match in Verifier.get_matched_pattern_content(message_content_merged, r'nbPDCCHSymbol=(\d)'):
                        nb_pdcch_symbols.append(match)
                elif message_id == "Dl PdschSendReq(30)":
                    for match in Verifier.get_matched_pattern_content(message_content_merged, r'startPDSCHSymbol=(\d)'):
                        start_pdsch_symbols.append(match)

            if not start_pdsch_symbols:
                continue

            symbol_usage = []
            pdcch_allocation_pairs = list(set(["".join([start_pdcch_symbols[i], nb_pdcch_symbols[i]])
                                               for i in range(len(start_pdcch_symbols))]))
            for pair in pdcch_allocation_pairs:
                start_pdcch_symbol, allocated_symbols = pair
                symbol_usage.append(int(start_pdcch_symbol))
                symbol_usage.append(int(start_pdcch_symbol) + int(allocated_symbols))

            final_pdcch_size = list(set(symbol_usage))[-1]
            if final_pdcch_size == int(sorted(start_pdsch_symbols)[0]) and final_pdcch_size == expected_pdcch_size:
                traces_with_expected_pdcch_size.append(tti)

        return len(traces_with_expected_pdcch_size) > 0
