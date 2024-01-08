import torch, torchinfo
import torchvision.models as models
# import matplotlib.pyplot as plt
# from torchvision.models.alexnet import AlexNet, AlexNet_Weights
# from torchvision.models.vgg import VGG
# from torchvision.models.googlenet import GoogLeNet
# from torchvision.models.resnet import ResNet


# モデルの定義
model = models.alexnet() #ooo
# model = models.vgg11()
# model = models.vgg13()
# model = models.vgg16() #ooo
# model = models.googlenet() #ooo
# model = models.resnet18()
# model = models.resnet34()
# model = models.resnet50() #ooo
# model = models.resnet101()
# model = models.resnet152()
# model = models.densenet121()
# model = models.densenet169()
# model = models.densenet201()
# model = models.densenet161() #after 201
# model = models.mobilenet_v2() #ooo
# model = models.efficientnet_b0() #224
# model = models.efficientnet_b1() #240
# model = models.efficientnet_b2() #260
# model = models.efficientnet_b3() #300
# model = models.efficientnet_b4() #380
# model = models.efficientnet_b5() #456
# model = models.efficientnet_b6() #528
# model = models.efficientnet_b7() #600
# model = models.efficientnet_v2_s()
# model = models.efficientnet_v2_m()
# model = models.efficientnet_v2_l()
torchinfo.summary(model, (1, 3, 224, 224))

# 学習済みモデルをロード
# alexnet = models.alexnet(weights=AlexNet_Weights.DEFAULT)



# モデルのパラメータを取得
# params = list(alexnet.parameters())
# for i in range(0, 16):
#     if i % 2 == 0:
#         print(f'input ch: {len(params[i][i])}')
#         print(f'output ch: {len(params[i])}')
#         # print(f'kernel size: {len(params[i][i][i])}')
#         # print(f'kernel size: {len(params[i][i][i][i])}')
#     else:
#         print(f'bias: {len(params[i])}')

# ヒストグラムを表示
# for i, param in enumerate(params):
#     plt.figure(figsize=(8, 6))
#     plt.hist(param.cpu().detach().numpy().flatten(), bins=50, density=True, alpha=0.7, color='b')
#     plt.title(f'Layer {i + 1} Parameter Histogram')
#     plt.xlabel('Value')
#     plt.ylabel('Frequency')
#     plt.show()
