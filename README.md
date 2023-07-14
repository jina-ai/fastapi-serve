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

- 🌐 **DNS**: Automatic URL generation for your app.
- 🔗 **Protocols**: Full compatibility with HTTP, WebSocket, and GraphQL.
- ↕️ **Scaling**: Scale your app manuallly or let it auto-scale based on RPS, CPU, and Memory.
- 🗝️ **Secrets**: Secure handling of secrets and environment variables.
- 🎛️ **Hardware**: Tailor your deployment to suit specific needs.
- 💾 **Storage**: Persistent and secure network storage.
- 🔎 **Observability**: Integrated access to logs, metrics, and traces.
- 📦 **Containerization**: Effortless containerization of your Python codebase with our integrated registry.

## 💡 Getting Started

First, install the `fastapi-serve` package using pip:

```bash
pip install fastapi-serve
```

Then, simply use the `fastapi-serve` command to deploy your FastAPI application:

```bash
fastapi-serve deploy jcloud app:app
```

You can also specify the name of your app:

```bash
fastapi-serve deploy jcloud app:app --name my-app
```

You'll get a URL to access your newly deployed application along with the Swagger UI.

## 📚 Examples

We have a few examples to help you get acquainted with `fastapi-serve`:

1. [Quickstart Guide](examples/simple/) to deploy a simple FastAPI application.
2. [Redis-powered Rate Limiting](examples/rate_limit/) to learn how to use `fastapi-serve` with secrets.


## 🖥️ `fastapi-serve` CLI 

`fastapi-serve` comes with a simple CLI that allows you to deploy your FastAPI applications to the cloud with ease.

| Description | Command | 
| --- | ---: |
| Deploy your app locally | `fastapi-serve deploy local app:app` |
| Deploy your app on JCloud | `fastapi-serve deploy jcloud app:app` |
| Update existing app on JCloud | `fastapi-serve deploy jcloud app:app --app-id <app-id>` |
| Get app status on JCloud | `fastapi-serve status <app-id>` |
| List all apps on JCloud | `fastapi-serve list` |
| Remove app on JCloud | `fastapi-serve remove <app-id>` |


## ⚙️💰 Configuration and Pricing

Read our [Configuration & Pricing Guide](examples/CONFIG.MD) to learn more about the various configuration options available to you and the pricing model for `fastapi-serve`.

## 💪 Support

If you encounter any problems or have questions, feel free to open an issue on the GitHub repository. You can also join our [Discord](https://discord.jina.ai/) to get help from our community members and the Jina team.


## Our Cloud Platform 🌐 

`cloud.jina.ai` is our robust and scalable cloud platform designed to run your FastAPI applications with minimum hassle and maximum efficiency. With features like auto-scaling, integrated observability, and automated containerization, it provides a seamless and worry-free deployment experience.

---

`fastapi-serve` is more than just a deployment tool, it's a bridge that connects your local development environment with our powerful cloud infrastructure. Start using `fastapi-serve` today, and experience the joy of effortless deployments! 🎊 
