import torch
import tinytorch
import numpy as np

np.random.seed(69420)


def test_add():
    x = np.random.rand(3, 3)
    y = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    z_t = x_t + y_t
    z_t.sum().backward()

    z_tt = x_tt + y_tt
    z_tt.sum().backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Addition results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match between PyTorch and tinytorch."
    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match between PyTorch and tinytorch."


def test_mul():
    x = np.random.rand(3, 3)
    y = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    z_t = x_t * y_t
    z_t.sum().backward()

    z_tt = x_tt * y_tt
    z_tt.sum().backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Multiplication results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match between PyTorch and tinytorch."
    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match between PyTorch and tinytorch."


def test_div():
    x = np.random.rand(3, 3) + 1  # Adding 1 to avoid division by zero
    y = np.random.rand(3, 3) + 1

    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    z_t = x_t / y_t
    z_t.sum().backward()

    z_tt = x_tt / y_tt
    z_tt.sum().backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Division results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match between PyTorch and tinytorch."
    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match between PyTorch and tinytorch."


def test_sub():
    x = np.random.rand(3, 3)
    y = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    z_t = x_t - y_t
    z_t.sum().backward()

    z_tt = x_tt - y_tt
    z_tt.sum().backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Subtraction results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match between PyTorch and tinytorch."
    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match between PyTorch and tinytorch."


def test_sum():
    x = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    z_t = x_t.sum()
    z_t.backward()

    z_tt = x_tt.sum()
    z_tt.backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Sum results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients do not match between PyTorch and tinytorch."


def test_sum_axis(axis=1):
    x = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    z_t = x_t.sum(dim=axis)
    z_t.sum().backward()  # Summing again to get a scalar for backward()

    z_tt = x_tt.sum(axis=axis)
    z_tt.sum().backward()  # Summing again to get a scalar for backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), f"Sum along axis {axis} results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), f"Gradients along axis {axis} do not match between PyTorch and tinytorch."


def test_reshape():
    x = np.random.rand(2, 3, 4)

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    new_shape = (3, 2, 4)
    z_t = x_t.reshape(new_shape)
    z_t.sum().backward()

    z_tt = x_tt.reshape(new_shape)
    z_tt.sum().backward()

    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Reshape results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients do not match between PyTorch and tinytorch."


def test_custom_eq():
    # Define custom function f(x, y) within the scope of test_custom_eq
    def f(x, y):
        return x * x + (x * y) / (x + y) + x * (x + y)

    x = np.random.rand(3, 3)
    y = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    # Compute f(x, y) using PyTorch
    z_t = f(x_t, y_t)
    z_t.sum().backward()

    # Compute f(x, y) using tinytorch
    z_tt = f(x_tt, y_tt)
    z_tt.sum().backward()

    # Assertions to check if both results match
    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Custom eq results do not match between PyTorch and tinytorch."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match between PyTorch and tinytorch."
    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match between PyTorch and tinytorch."


def test_matmul():
    x = np.random.rand(3, 4)
    y = np.random.rand(4, 3)

    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    z_t = x_t @ y_t
    z_t.sum().backward()

    z_tt = x_tt @ y_tt
    z_tt.sum().backward()

    # Assertions
    assert np.allclose(z_t.detach().numpy(), z_tt.data), "Matmul results do not match."
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match."
    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match."


def test_pow():
    x = np.random.rand(3, 3)
    exponent = 2

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    z_t = x_t ** (exponent)
    z_t.sum().backward()

    z_tt = x_tt ** (exponent)
    z_tt.sum().backward()

    # Assertions
    assert np.allclose(z_t.detach().numpy(), z_tt.data), "Pow results do not match."
    assert np.allclose(x_t.grad.numpy(), x_tt.grad.data), "Gradients do not match."


def test_tanh():
    x = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    z_t = torch.tanh(x_t)
    z_t.sum().backward()

    z_tt = tinytorch.tanh(x_tt)
    z_tt.sum().backward()

    # Assertions
    assert np.allclose(z_t.detach().numpy(), z_tt.data), "Tanh results do not match."
    assert np.allclose(x_t.grad.numpy(), x_tt.grad.data), "Gradients do not match."


def test_relu():
    x = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    z_t = torch.relu(x_t)
    z_t.sum().backward()

    z_tt = tinytorch.relu(x_tt)
    z_tt.sum().backward()

    # Assertions
    assert np.allclose(z_t.detach().numpy(), z_tt.data), "ReLU results do not match."
    assert np.allclose(x_t.grad.numpy(), x_tt.grad.data), "Gradients do not match."


def test_mse_loss():
    y_pred = np.random.rand(2, 2)
    y_true = np.random.rand(2, 2)

    y_pred_t = torch.tensor(y_pred, requires_grad=True)
    y_true_t = torch.tensor(y_true, requires_grad=False)

    y_pred_tt = tinytorch.tensor(y_pred, requires_grad=True)
    y_true_tt = tinytorch.tensor(y_true, requires_grad=False)

    loss_t = torch.nn.functional.mse_loss(y_pred_t, y_true_t)
    loss_t.backward()

    loss_tt = tinytorch.mse_loss(y_pred_tt, y_true_tt)
    print(loss_t, loss_tt)
    loss_tt.backward()

    # Assertions
    assert np.allclose(
        loss_t.detach().numpy(), loss_tt.data
    ), "MSE Loss results do not match."
    assert np.allclose(
        y_pred_t.grad.numpy(), y_pred_tt.grad.data
    ), "Gradients do not match."


def test_cross_entropy():
    # Create random logits and labels
    logits = np.random.rand(5, 3)  # 5 samples, 3 classes
    labels = np.random.randint(0, 3, size=(5,))  # 5 samples, labels from 0 to 2

    print(f"{labels.shape=}")

    # Convert to PyTorch tensors
    logits_t = torch.tensor(logits, requires_grad=True)
    labels_t = torch.tensor(labels, requires_grad=False, dtype=torch.long)

    # Convert to tinytorch tensors
    logits_tt = tinytorch.tensor(logits, requires_grad=True)
    labels_tt = tinytorch.tensor(labels, requires_grad=False)

    # Compute loss using PyTorch
    loss_t = torch.nn.functional.cross_entropy(logits_t, labels_t)
    loss_t.backward()

    print(f"{logits.shape=} {labels_t.shape=} {loss_t.shape=}")

    # Compute loss using tinytorch (assuming cross_entropy is implemented)
    loss_tt = tinytorch.cross_entropy(logits_tt, labels_tt)
    loss_tt.sum().backward()

    # print(f"{loss_t=}")
    # print(f"{loss_tt=}")
    # Assertions
    assert np.allclose(
        loss_t.detach().numpy(), loss_tt.detach().numpy(), atol=1e-5
    ), "Cross-entropy Loss results do not match."
    assert np.allclose(
        logits_t.grad.numpy(), logits_tt.grad.data, atol=1e-7
    ), "Gradients do not match."


def test_transpose():
    x = np.random.rand(3, 4)  # Create a 3x4 random matrix

    x_t = torch.tensor(x, requires_grad=True)  # Create a PyTorch tensor
    x_tt = tinytorch.tensor(x, requires_grad=True)  # Create a tinytorch tensor

    # Perform the transpose operation using PyTorch
    z_t = x_t.t()
    z_t.sum().backward()  # Compute the gradients via backpropagation

    # Perform the transpose operation using tinytorch
    z_tt = x_tt.t()
    z_tt.sum().backward()  # Compute the gradients via backpropagation

    # Assert that the transpose operation results are the same for both PyTorch and tinytorch
    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Transpose results do not match between PyTorch and tinytorch."

    # Assert that the gradients are the same for both PyTorch and tinytorch
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients do not match between PyTorch and tinytorch."


def test_max():
    x = np.random.rand(2, 3)  # Create a random 2x3 array
    axis = 1  # Axis along which to compute max

    x_t = torch.tensor(x, requires_grad=True)  # Create a PyTorch tensor
    x_tt = tinytorch.tensor(x, requires_grad=True)  # Create a tinytorch tensor

    # Compute max using PyTorch
    y_t, _ = torch.max(x_t, dim=axis)
    loss_t = y_t.sum()
    loss_t.backward()

    # Compute max using tinytorch
    y_tt, _ = x_tt.max(axis=axis)
    # print(f"{x_tt.shape=} {y_tt.shape=}")
    loss_tt = y_tt.sum()
    loss_tt.backward()

    # Assertions
    assert np.allclose(y_t.detach().numpy(), y_tt.data), "Max results do not match."

    assert np.allclose(x_t.grad.numpy(), x_tt.grad.data), "Gradients do not match."


def test_stack_with_square():
    x = np.random.rand(3, 3)
    y = np.random.rand(3, 3)

    # Convert to PyTorch tensors
    x_t = torch.tensor(x, requires_grad=True)
    y_t = torch.tensor(y, requires_grad=True)

    # Perform stack operation in PyTorch
    z_t = torch.stack([x_t, y_t], dim=0)
    z_t = z_t**2  # Square the tensor
    z_t.sum().backward()

    # Assuming you've implemented stack and power operation in tinytorch
    # Convert to tinytorch tensors
    x_tt = tinytorch.tensor(x, requires_grad=True)
    y_tt = tinytorch.tensor(y, requires_grad=True)

    # Perform stack operation in tinytorch
    z_tt = tinytorch.stack([x_tt, y_tt], axis=0)
    z_tt = z_tt**2  # Square the tensor
    z_tt.sum().backward()

    # Verify that the output from PyTorch and tinytorch are the same
    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Stack operation results do not match between PyTorch and tinytorch."

    # Verify that the gradients are the same for both PyTorch and tinytorch
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data
    ), "Gradients for x do not match between PyTorch and tinytorch."

    assert np.allclose(
        y_t.grad.numpy(), y_tt.grad.data
    ), "Gradients for y do not match between PyTorch and tinytorch."


def test_sigmoid():
    x = np.random.rand(3, 3)

    x_t = torch.tensor(x, requires_grad=True)
    x_tt = tinytorch.tensor(x, requires_grad=True)

    z_t = torch.sigmoid(x_t)
    z_t.sum().backward()

    z_tt = tinytorch.sigmoid(x_tt)
    z_tt.sum().backward()

    assert np.allclose(z_t.detach().numpy(), z_tt.data), "Sigmoid results do not match."
    assert np.allclose(x_t.grad.numpy(), x_tt.grad.data), "Gradients do not match."


def softmax(x: torch.Tensor, dim: int = 0) -> torch.Tensor:
    m, _ = x.max(axis=dim, keepdims=True)
    e_x = (x - m).exp()
    return e_x / e_x.sum(axis=dim, keepdims=True)


def test_softmax():
    x = np.random.rand(5, 3)  # Create a random 5x3 matrix

    # Convert to PyTorch tensor
    x_t = torch.tensor(x, requires_grad=True)

    # Convert to tinytorch tensor
    x_tt = tinytorch.tensor(x, requires_grad=True)

    # Perform the softmax operation using PyTorch
    z_t = softmax(x_t, dim=1)
    z_t.sum().backward()

    # Perform the softmax operation using tinytorch (assuming softmax is implemented)
    z_tt = softmax(x_tt, dim=1)
    z_tt.sum().backward()

    # Assert that the softmax operation results are the same for both PyTorch and tinytorch
    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Softmax results do not match between PyTorch and tinytorch."

    # Assert that the gradients are the same for both PyTorch and tinytorch
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data, atol=1e-5
    ), "Gradients do not match between PyTorch and tinytorch."


def test_softmax2():
    x = np.random.rand(5, 3)  # Create a random 5x3 matrix
    x[-1][-1] = -np.inf

    # Convert to PyTorch tensor
    x_t = torch.tensor(x, requires_grad=True)

    # Convert to tinytorch tensor
    x_tt = tinytorch.tensor(x, requires_grad=True)

    # Perform the softmax operation using PyTorch
    z_t = softmax(x_t, dim=1)
    z_t.sum().backward()

    # Perform the softmax operation using tinytorch (assuming softmax is implemented)
    z_tt = softmax(x_tt, dim=1)
    z_tt.sum().backward()

    # Assert that the softmax operation results are the same for both PyTorch and tinytorch
    assert np.allclose(
        z_t.detach().numpy(), z_tt.data
    ), "Softmax results do not match between PyTorch and tinytorch."

    # Assert that the gradients are the same for both PyTorch and tinytorch
    assert np.allclose(
        x_t.grad.numpy(), x_tt.grad.data, atol=1e-5
    ), "Gradients do not match between PyTorch and tinytorch."


def test_attention():
    def softmax(x: torch.Tensor, dim: int = 0) -> torch.Tensor:
        m, _ = x.max(axis=dim, keepdims=True)
        e_x = (x - m).exp()
        return e_x / e_x.sum(axis=dim, keepdims=True)

    def attention(k, q, v, mask):
        B, n_head, T, C = k.shape
        wei = (q @ k.transpose(-1, -2)) * (C**-0.5)
        wei = mask[:, :, :T, :T] + wei
        wei = softmax(wei, dim=-1)
        x = wei @ v
        return x

    B, n_head, T, C = 3, 5, 7, 9
    seq_len = 20
    k = np.random.rand(*(B, n_head, T, C))
    q = np.random.rand(*(B, n_head, T, C))
    v = np.random.rand(*(B, n_head, T, C))

    mask = np.tril(np.zeros((1, 1, seq_len, seq_len))) + np.triu(
        -np.inf * np.ones((1, 1, seq_len, seq_len)),
        k=1,
    )

    kt = torch.tensor(k, requires_grad=True)
    qt = torch.tensor(q, requires_grad=True)
    vt = torch.tensor(v, requires_grad=True)
    maskt = torch.tensor(mask, requires_grad=True)
    outt = attention(kt, qt, vt, maskt)
    outt.sum().backward()

    ktt = tinytorch.tensor(k, requires_grad=True)
    qtt = tinytorch.tensor(q, requires_grad=True)
    vtt = tinytorch.tensor(v, requires_grad=True)
    masktt = tinytorch.tensor(mask, requires_grad=True)
    outtt = attention(ktt, qtt, vtt, masktt)
    outtt.sum().backward()

    assert np.allclose(
        outt.detach().numpy(), outtt.detach().numpy(), atol=1e-5
    ), "Gradients do not match between PyTorch and tinytorch."

    assert np.allclose(
        kt.grad.numpy(), ktt.grad.data, atol=1e-5
    ), "Gradients do not match between PyTorch and tinytorch."

    assert np.allclose(
        qt.grad.numpy(), qtt.grad.data, atol=1e-5
    ), "Gradients do not match between PyTorch and tinytorch."

    assert np.allclose(
        vt.grad.numpy(), vtt.grad.data, atol=1e-5
    ), "Gradients do not match between PyTorch and tinytorch."


def test_xor_matmul_backward():
    class XorNet(tinytorch.Module):
        def __init__(self):
            super().__init__()
            self.l1 = tinytorch.Linear(2, 2)
            self.l2 = tinytorch.Linear(2, 1)

        def forward(self, x):
            x = self.l1(x)
            x = tinytorch.tanh(x)
            x = self.l2(x)
            x = tinytorch.tanh(x)
            return x

    x = tinytorch.tensor(
        [
            [0, 0],
            [1, 0],
            [0, 1],
            [1, 1],
        ]
    )
    y = tinytorch.tensor(
        [
            [0],
            [1],
            [1],
            [0],
        ]
    )
    model = XorNet()
    loss = tinytorch.Tensor([0.0])
    for i in range(2):
        for x1, y1 in zip(x, y):
            pred = model(x1)
            loss += tinytorch.mse_loss(pred, y1)
    loss.backward()
