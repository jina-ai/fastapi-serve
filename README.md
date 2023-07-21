<p align="center">
<h2 align="center">FastAPI-Serve: FastAPI to the Cloud, Batteries Included! ☁️🔋🚀</h2>
</p>

<p align=center>
<a href="https://pypi.org/project/fastapi-serve/"><img alt="PyPI" src="https://img.shields.io/pypi/v/fastapi-serve?label=Release&style=flat-square"></a>
<a href="https://discord.jina.ai"><img src="https://img.shields.io/discord/1106542220112302130?logo=discord&logoColor=white&style=flat-square"></a>
<a href="https://pypistats.org/packages/fastapi-serve"><img alt="PyPI - Downloads from official pypistats" src="https://img.shields.io/pypi/dm/fastapi-serve?style=flat-square"></a>
<a href="https://github.com/jina-ai/fastapi-serve/actions/workflows/cd.yml"><img alt="Github CD status" src="https://github.com/jina-ai/fastapi-serve/actions/workflows/cd.yml/badge.svg"></a>
</p>

Welcome to **fastapi-serve**, your one-stop solution for seamless FastAPI application deployments. Powered by our open-source framework [Jina](https://github.com/jina-ai/jina), `fastapi-serve` provides an effortless transition from your local setup to [cloud.jina.ai](https://cloud.jina.ai/), our robust and scalable cloud platform. 🌩️

Designed with developers in mind, `fastapi-serve` simplifies the deployment process by packing robust functionality, ease-of-use, and automated procedures into one comprehensive package. With `fastapi-serve`, we aim to streamline the "last mile" of FastAPI application development, allowing you to focus on what truly matters - writing great code!


## 😍 Features 

- 🌎 **HTTPS**: Auto-provisioned DNS and TLS certificates for your app.
- 🔗 **Protocols**: Full compatibility with HTTP, WebSocket, and GraphQL.
- ↕️ **Scaling**: Scale your app manually or let it auto-scale based on RPS, CPU, and Memory.
- 🗝️ **Secrets**: Secure handling of secrets and environment variables.
- 🎛️ **Hardware**: Choose the right compute resources for your app's needs with ease.
- 🔒 **Authorization**: Built-in `OAuth2.0` token-based security to secure your endpoints. 
- 💾 **App Storage**: Persistent and secure network storage for your app data.
- 🔄 **Blob Storage**: Built-in support for seamless user file uploads and downloads.
- 🔎 **Observability**: Integrated access to logs, metrics, and traces. (Alerting coming soon!)
- 📦 **Containerization**: Effortless containerization of your Python codebase with our integrated registry.
- 🛠️ **Self-Hosting**: Export your app for self-hosting with ease, including docker-compose and Kubernetes YAMLs.

## 💡 Getting Started

First, install the `fastapi-serve` package using pip:

```bash
pip install fastapi-serve
```

Then, simply use the `fastapi-serve` command to deploy your FastAPI application:

```bash
fastapi-serve deploy jcloud main:app
```

You'll get a URL to access your newly deployed application along with the Swagger UI.

## 📚 Documentation

Dive into understanding `fastapi-serve` through our comprehensive documentation and examples:

- 🚀 **Getting Started**
    - 🧱 [Deploy a Simple FastAPI Application](docs/simple/)
    - 🖥️ [Dig deep into the `fastapi-serve` CLI](docs/CLI.md)
    - ⚙️ [Understanding Configuration and Pricing on Jina AI Cloud](docs/CONFIG.MD)
    - 🔄 [Upgrade your FastAPI applications with zero downtime](docs/upgrades/)
    - 🏢 Managing Larger Applications with Complex Directory Structure (🚧Documentation in progress)
- ↕️ **Scaling**
    - 💹 [Auto-scaling endpoints based on CPU usage](docs/autoscaling/cpu/)
    - 📉 [Serverless (scale-to-zero) deployments based on RPS](docs/autoscaling/serverless/) 
- 🧩 **Config & Credentials**
    - 🌍 [Leverage Environment Variables for app configuration](docs/envs/)
    - 🗝️ [Use Secrets for Redis-Powered Rate Limiting](docs/rate_limit/)
- 💾 **Storage**
    - 📁 [Manage File Uploads and Downloads with built-in Blob Storage](docs/file_handling/)
    - 🌐 Network Storage for persisting and securely accessing app data (🚧Documentation in progress)
- 🔒 **Security**
    - 👮‍♂️ [Secure Your Endpoints with built-in OAuth2.0 Authorization](docs/authorization/)
- 🐳 **Deployment Options**
    - 🚢 Deployment with Custom Dockerfile (🚧Documentation in progress)
    - ☸️ [Export Your App for Self-Hosting with docker-compose / Kubernetes](docs/export/)
- 📈 **Observability**
    - 📊 Access Logs, Metrics, and Traces for your app (🚧Documentation in progress)
    - 🚨 Set up Alerts for your app (🚧Documentation in progress)


## 💪 Support

If you encounter any problems or have questions, feel free to open an issue on the GitHub repository. You can also join our [Discord](https://discord.jina.ai/) to get help from our community members and the Jina team.


## 🌐 Our Cloud Platform  

Our robust and scalable cloud platform `cloud.jina.ai` is designed to run your FastAPI applications with minimum hassle and maximum efficiency. With features like auto-scaling, integrated observability, and automated containerization, it provides a seamless and worry-free deployment experience.

---

`fastapi-serve` is more than just a deployment tool, it's a bridge that connects your local development environment with our powerful cloud infrastructure. Start using `fastapi-serve` today, and experience the joy of effortless deployments! 🎊 
