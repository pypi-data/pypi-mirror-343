# beswarm

beswarm: be swarm

beswarm is a tool for creating a swarm of agents to complete a task.

## 任务

```
DiT-Air 架构与MMDiT和PixArt的区别是什么？详细分析三个模型的架构，并给出代码实现。
```

```
arXiv:2502.14831v2 和 arXiv:2503.10618v2 的 渐进式 VAE 训练方法有一定的相似性，请详细分析这两种方法的异同，底层原理的异同。
```

```
论文地址：'/Users/yanyuming/Library/Mobile Documents/iCloud~QReader~MarginStudy~easy/Documents/论文/EQ-VAE Equivariance Regularized Latent Space for Improved Generative Image Modeling.pdf'
仓库地址：https://github.com/zelaki/eqvae
```

```
论文地址：'/Users/yanyuming/Library/Mobile Documents/iCloud~QReader~MarginStudy~easy/Documents/论文/Vector Quantized Diffusion Model for Text-to-Image Synthesis.pdf'

查看代码库，我需要将论文的公式，代码，理论，实验结果，总结，形成一个文档。请进行彻底的分析。

找到每一个数学概念对应的代码实现。整理成文档保存到本地。
```

```
docker build --platform linux/amd64 -t beswarm .
docker tag beswarm:latest yym68686/beswarm:latest
docker push yym68686/beswarm:latest
```

```
cd ~/Downloads/GitHub/beswarm && docker run --rm \
--env-file .env \
-v ./work:/app/work beswarm \
--goal "分析这个仓库 https://github.com/cloneofsimo/minRF"
```