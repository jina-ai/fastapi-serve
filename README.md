<p align="center">
<h2 align="center">FastAPI-Serve: FastAPI to the Cloud, Batteries Included! ☁️🔋🚀</h2>
</p>

<p align=center>
<a href="https://pypi.org/project/fastapi-serve/"><img alt="PyPI" src="https://img.shields.io/pypi/v/fastapi-serve?label=Release&style=flat-square"></a>
<a href="https://discord.jina.ai"><img src="https://img.shields.io/discord/1106542220112302130?logo=discord&logoColor=white&style=flat-square"></a>
<a href="https://pypistats.org/packages/fastapi-serve"><img alt="PyPI - Downloads from official pypistats" src="https://img.shields.io/pypi/dm/fastapi-serve?style=flat-square"></a>
<a href="https://github.com/jina-ai/fastapi-serve/actions/workflows/cd.yml"><img alt="Github CD status" src="https://github.com/jina-ai/fastapi-serve/actions/workflows/cd.yml/badge.svg"></a>
</p>

Welcome to **fastapi-serve**, a framework designed to take the pain out of deploying your local FastAPI applications to the cloud. Built using our open-source framework [Jina](https://github.com/jina-ai/jina), `fastapi-serve` offers out-of-the-box support for automated deployments on `cloud.jina.ai`, our scalable and robust cloud platform. 🌩️ 

## 😍 Features 

- 🌎 **HTTPS**: Auto-provisioned DNS and TLS certificates for your app.
- 🔗 **Protocols**: Full compatibility with HTTP, WebSocket, and GraphQL.
- ↕️ **Scaling**: Scale your app manuallly or let it auto-scale based on RPS, CPU, and Memory.
- 🗝️ **Secrets**: Secure handling of secrets and environment variables.
- 🎛️ **Hardware**: Tailor your deployment to suit specific needs.
- 🔒 **Authorization**: Built-in OAuth2.0 token-based security to secure your endpoints. 
- 💾 **App Storage**: Persistent and secure network storage for your app data.
- 🔄 **Blob Storage**: Built-in support for seamless user file uploads and downloads.
- 🔎 **Observability**: Integrated access to logs, metrics, and traces.
- 📦 **Containerization**: Effortless containerization of your Python codebase with our integrated registry.
- 🛠️ **Self-Hosting**: Export your app for self-hosting with ease, including docker-compose and Kubernetes yamls.

## 💡 Getting Started

First, install the `fastapi-serve` package using pip:

```bash
pip install fastapi-serve
```

Then, simply use the `fastapi-serve` command to deploy your FastAPI application:

```bash
fastapi-serve deploy jcloud app:app
```

You'll get a URL to access your newly deployed application along with the Swagger UI.

## 📚 Documentation

Dive into understanding `fastapi-serve` through our comprehensive documentation and examples:

- 🚀 **Getting Started**
    - 🧱 [Deploy a Simple FastAPI Application](docs/simple/)
    - 🖥️ [Dig deep into the `fastapi-serve` CLI](docs/CLI.md)
    - ⚙️ [Understanding Configuration and Pricing](docs/CONFIG.MD)
- ↕️ **Scaling**
    - 💹 [**Auto-scaling** endpoints based on CPU usage](docs/autoscaling/cpu/)
    - 📉 [**Serverless** (scale-to-zero) deployments based on requests-per-second](docs/autoscaling/serverless/) 
- 🧩 **Config & Credentials**
    - 🌍 Leverage **Environment Variables** for app configuration (Example TBD!)
    - 🗝️ [Use **Secrets** for Redis-Powered Rate Limiting](docs/rate_limit/)
- 💾 **Storage**
    - 📁 [Handle File Uploads and Downloads with built-in **Blob Storage**](docs/file_handling/)
    - 🌐 Network Storage for persisting and securely accessing app data (Example TBD!)
- 🔒 **Security**
    - 👮‍♂️ [Secure Your Endpoints with built-in **OAuth2.0 Authorization**](docs/authorization/)
- 🐳 **Deployment Options**
    - 🚢 Deployment with **Custom Dockerfile** (Coming Soon!)
    - 🛠️ Export Your App for **Self-Hosting** with docker-compose / Kubernetes (Coming Soon!)


## 💪 Support

If you encounter any problems or have questions, feel free to open an issue on the GitHub repository. You can also join our [Discord](https://discord.jina.ai/) to get help from our community members and the Jina team.


## 🌐 Our Cloud Platform  

`cloud.jina.ai` is our robust and scalable cloud platform designed to run your FastAPI applications with minimum hassle and maximum efficiency. With features like auto-scaling, integrated observability, and automated containerization, it provides a seamless and worry-free deployment experience.

---

`fastapi-serve` is more than just a deployment tool, it's a bridge that connects your local development environment with our powerful cloud infrastructure. Start using `fastapi-serve` today, and experience the joy of effortless deployments! 🎊 
