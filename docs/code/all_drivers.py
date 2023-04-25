from squirrel_datasets_core.driver import (
    HubDriver,
    HuggingfaceDriver,
    TorchvisionDriver,
    # SklearnDriver
)

HuggingfaceDriver("cifar100").get_iter("train").take(1).map(print).join()
# prints
# {
#     "img": <PIL.PngImagePlugin.PngImageFile image mode=RGB size=32x32 at 0x1424D6310>,
#     "fine_label": 19,
#     "coarse_label": 11,
# }

HubDriver("hub://activeloop/cifar100-train").get_iter().take(1).map(print).join()
# prints
# {
#     "images": Tensor(key="images", index=Index([0])),
#     "labels": Tensor(key="labels", index=Index([0])),
# }

TorchvisionDriver("cifar100", download=True).get_iter().take(1).map(print).join()
# prints
# (
#     <PIL.Image.Image image mode=RGB size=32x32 at 0x143BD77C0>,
#     6,
# )
