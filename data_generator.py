from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds


class EEGGenerator:
    def __init__(self):
        params = BrainFlowInputParams()
        self.board_id = BoardIds.SYNTHETIC_BOARD.value
        self.board = BoardShim(self.board_id, params)
        self.eeg_channels = BoardShim.get_eeg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.board.prepare_session()

    def start_stream(self) -> None:
        self.board.start_stream()

    def get_data(self, num_samples: int):
        return self.board.get_current_board_data(num_samples)

    def stop_stream(self) -> None:
        self.board.stop_stream()
        self.board.release_session()


