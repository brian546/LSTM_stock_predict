from torch import nn

# ================== MODEL ==================
class LSTMModel(nn.Module):
    def __init__(self, input_size: int = 4, hidden_size: int = 128):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True, num_layers=2,dropout=0.2)
        self.fc   = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])