# loads model, runs inference

import logging
import numpy as np
import torch
import torch.nn as nn
from torchvision.models import resnet34
from PIL import Image

from app.core.vocab import(
    VOCAB_SIZE,PAD_ID,SOS_ID,EOS_ID,index_to_char
)

from app.utils.image_utils import process_image

logger=logging.getLogger(__name__)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

EMBED_DIM = 256
NUM_HEADS = 8
FF_DIM = 1024
ENC_LAYERS = 2
DEC_LAYERS = 4
DROPOUT = 0.1
MAX_LEN = 150


class PositionalEncoding(nn.Module):
    def __init__(self, embed_dim, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        pe = torch.zeros(max_len, embed_dim)
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(
            torch.arange(0, embed_dim, 2).float() * -(np.log(10000.0) / embed_dim)
        )
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return self.dropout(x + self.pe[:, : x.size(1)])


class CNNBackbone(nn.Module):
    def __init__(self, dropout=0.1):
        super().__init__()
        backbone = resnet34(weights=None)
        self.features = nn.Sequential(
            backbone.conv1, backbone.bn1, backbone.relu, backbone.maxpool,
            backbone.layer1, backbone.layer2, backbone.layer3,
        )
        for p in self.features.parameters():
            p.requires_grad = False
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.dropout(self.features(x))


class HMERModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.cnn = CNNBackbone(DROPOUT)
        self.enc_pe = PositionalEncoding(EMBED_DIM, max_len=128 * 256, dropout=DROPOUT)

        enc_layer = nn.TransformerEncoderLayer(
            d_model=EMBED_DIM, nhead=NUM_HEADS, dim_feedforward=FF_DIM,
            dropout=DROPOUT, batch_first=True, norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=ENC_LAYERS)

        self.tok_emb = nn.Embedding(VOCAB_SIZE, EMBED_DIM, padding_idx=PAD_ID)
        self.dec_pe = PositionalEncoding(EMBED_DIM, max_len=MAX_LEN, dropout=DROPOUT)

        dec_layer = nn.TransformerDecoderLayer(
            d_model=EMBED_DIM, nhead=NUM_HEADS, dim_feedforward=FF_DIM,
            dropout=DROPOUT, batch_first=True, norm_first=True,
        )
        self.decoder = nn.TransformerDecoder(dec_layer, num_layers=DEC_LAYERS)
        self.fc_out = nn.Linear(EMBED_DIM, VOCAB_SIZE)

    def encode(self, images):
        feats = self.cnn(images)
        B, C, H, W = feats.shape
        feats = feats.flatten(2).permute(0, 2, 1)
        feats = self.enc_pe(feats)
        return self.encoder(feats)

    def decode(self, enc_out, dec_inp):
        T = dec_inp.size(1)
        tgt = self.dec_pe(self.tok_emb(dec_inp))
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(
            T, device=dec_inp.device, dtype=torch.bool
        )
        pad_mask = dec_inp == PAD_ID
        out = self.decoder(
            tgt, enc_out, tgt_mask=tgt_mask, tgt_key_padding_mask=pad_mask
        )
        return self.fc_out(out)

    def forward(self, images, dec_inp):
        return self.decode(self.encode(images), dec_inp)


class ModelService:
    _model = None

    @classmethod
    def load(cls, model_path: str):
        cls._model = HMERModel().to(DEVICE)
        ckpt = torch.load(model_path, map_location=DEVICE, weights_only=False)
        cls._model.load_state_dict(ckpt["model"])
        cls._model.eval()
        logger.info("Model loaded on %s", DEVICE)

    @classmethod
    def predict(cls, pil_img: Image.Image) -> str:
        if cls._model is None:
            raise RuntimeError("Model is not loaded.")

        img_tensor = process_image(pil_img).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            enc_out = cls._model.encode(img_tensor)
            dec_inp = torch.tensor([[SOS_ID]], device=DEVICE)
            result = []

            for _ in range(MAX_LEN):
                logits = cls._model.decode(enc_out, dec_inp)
                next_id = logits[:, -1, :].argmax(-1).item()
                if next_id == EOS_ID:
                    break
                result.append(next_id)
                dec_inp = torch.cat(
                    [dec_inp, torch.tensor([[next_id]], device=DEVICE)], dim=1
                )

        return " ".join(index_to_char.get(i, "<unk>") for i in result)
