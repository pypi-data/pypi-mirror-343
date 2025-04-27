import torch

def load_model(model_class, weights_url, pretrained=True, map_location="cpu"):
    model = model_class()
    if pretrained:
        state_dict = torch.hub.load_state_dict_from_url(
            weights_url,
            map_location=map_location,
            progress=True,
            check_hash=True,
        )
        model.load_state_dict(state_dict)
    model.eval()
    return model
