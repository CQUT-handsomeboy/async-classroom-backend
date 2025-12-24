> [!NOTE]  
> 不可使用Python 3.13或更高版本，经测试会导致Manim-Voiceover依赖安装失败。
> 建议直接使用Python 3.11.9与笔者保持一致。


```powershell
# 安装依赖。
mkdir .venv && py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 运行
python meta.py
manim -pql .\result.py MainAnimation --disable_caching
```

编辑`.env`环境变量文件。
```
TTS_URL=https://api.siliconflow.cn/v1
TTS_KEY=sk-xxx # 需要硅基流动的API
```

## 🐳 Docker 部署

### 构建Docker镜像

```bash
# 构建镜像
docker build -t async-classroom-backend .

# 查看构建的镜像
docker images | grep async-classroom-backend
```

### 运行容器

```bash
# 基本运行（数据保存在容器内部，容器删除后数据会丢失）
docker run -d -p 8080:8080 --name async-classroom async-classroom-backend

# 持久化数据到宿主机（推荐）
docker run -d \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  --name async-classroom \
  async-classroom-backend

# 使用自定义端口（例如使用9000端口）
docker run -d \
  -p 9000:8080 \
  -v $(pwd)/data:/app/data \
  --name async-classroom \
  async-classroom-backend

# 查看运行状态
docker ps | grep async-classroom
```

### 容器管理

```bash
# 查看容器日志
docker logs async-classroom

# 实时查看日志
docker logs -f async-classroom

# 进入容器shell
docker exec -it async-classroom /bin/bash

# 停止容器
docker stop async-classroom

# 启动已停止的容器
docker start async-classroom

# 重启容器
docker restart async-classroom

# 删除容器
docker rm async-classroom

# 删除镜像
docker rmi async-classroom-backend
```