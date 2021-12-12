from automation import Parser, Verifier


def preprocess_data(path_to_l1l2_csv: str) -> dict:
    l1l2_traces = Parser.convert_l1l2_csv_traces(path_to_l1l2_csv)
    send_request_messages = Parser.remove_non_dl_send_request_messages(l1l2_traces)
    filtered_messages = Parser.extract_dl_send_request_messages(
        send_request_messages)
    return filtered_messages


def verify_pdcch_size_without_common_channels(path_to_l1l2_csv, expected_size: int) -> bool:
    preprocessed_traces = preprocess_data(path_to_l1l2_csv)
    return Verifier.verify_pdcch_size_without_common_channels(
        preprocessed_traces, expected_size)

