import torch

# Ensure data is converted to a PyTorch tensor
def convert_to_tensor(data):
    if not isinstance(data, torch.Tensor):
        data = torch.tensor(data, dtype=torch.float32)
    return data

# Gaussian noise function
def apply_gaussian(data, severity=1):
    data = convert_to_tensor(data)
    noise = torch.randn_like(data) * 0.1 * severity
    return data + noise

# Shot noise function
def apply_shot_noise(data, severity=1):
    shot_prob = 0.1 * severity
    mask = (torch.rand_like(data) < shot_prob).float()
    result = data * (1 - mask) + mask * torch.rand_like(data)
    return result

# Impulse noise function
def apply_impulse_noise(data, severity=1):
    data = convert_to_tensor(data)
    impulse_prob = 0.1 * severity
    mask = (torch.rand_like(data) < impulse_prob).float()
    return data * mask

# Speckle noise function
def apply_speckle_noise(data, severity=1):
    data = convert_to_tensor(data)
    noise = torch.randn_like(data) * 0.1 * severity
    return data + data * noise

# Gradual concept drift function
def apply_gradual_drift(data, severity=1, steps=100):
    data = convert_to_tensor(data)
    drift_amount = torch.linspace(0, 0.1 * severity, steps).unsqueeze(1).unsqueeze(2).unsqueeze(3)
    for i in range(min(steps, data.size(0))):
        data[i] += drift_amount[i]
    return data

# Sudden concept drift function
def apply_sudden_drift(data, severity=1):
    data = convert_to_tensor(data)
    shift = 0.1 * severity
    data[int(data.size(0) / 2):] += shift  # Apply drift to the second half of the data
    return data

# Function to apply all selected modifiers
def apply_modifiers(data, modifiers):
    data = convert_to_tensor(data)
    if "gaussian" in modifiers:
        data = apply_gaussian(data, severity=modifiers["gaussian"])
    if "shot_noise" in modifiers:
        data = apply_shot_noise(data, severity=modifiers["shot_noise"])
        print("Shot noise applied")
    if "impulse_noise" in modifiers:
        data = apply_impulse_noise(data, severity=modifiers["impulse_noise"])
    if "speckle_noise" in modifiers:
        data = apply_speckle_noise(data, severity=modifiers["speckle_noise"])
    # if "gradual_drift" in modifiers:
    #     data = apply_gradual_drift(data, severity=modifiers["gradual_drift"])
    if "sudden_drift" in modifiers:
        data = apply_sudden_drift(data, severity=modifiers["sudden_drift"])
    return data
