<p align="center">
<h2 align="center">FastAPI-Serve: FastAPI to the Cloud, Batteries Included! ☁️🔋🚀</h2>
</p>

<p align=center>
<a href="https://pypi.org/project/fastapi-serve/"><img alt="PyPI" src="https://img.shields.io/pypi/v/fastapi-serve?label=Release&style=flat-square"></a>
<a href="https://discord.jina.ai"><img src="https://img.shields.io/discord/1106542220112302130?logo=discord&logoColor=white&style=flat-square"></a>
<a href="https://pypistats.org/packages/fastapi-serve"><img alt="PyPI - Downloads from official pypistats" src="https://img.shields.io/pypi/dm/fastapi-serve?style=flat-square"></a>
<a href="https://github.com/jina-ai/fastapi-serve/actions/workflows/cd.yml"><img alt="Github CD status" src="https://github.com/jina-ai/fastapi-serve/actions/workflows/cd.yml/badge.svg"></a>
</p>

Welcome to `fastapi-serve`, a framework designed to take the pain out of deploying your local FastAPI applications to the cloud. Built using our open-source framework [Jina](https://github.com/jina-ai/jina), `fastapi-serve` offers out-of-the-box support for automated deployments on `cloud.jina.ai`, our scalable and robust cloud platform. 🌩️ 

## Features 😍 

- 🌐 **Automatic DNS**: Get a unique URL for your app automatically.
- 🔗 **HTTP/WebSocket Support**: Full compatibility with both protocols.
- ↕️  **Scaling**: Scale your app manually or let it auto-scale based on RPS, CPU, and Memory.
- 🗝️ **Environment Management**: Secure handling of secrets and environment variables.
- 🎛️ **Hardware Configuration**: Tailor the deployment to suit your hardware needs.
- 💾 **Persistent Storage**: Store data persistently and securely on the network.
- 🔎 **Integrated Observability**: Access logs, metrics, and traces all in one place.
- 📦 **Automated Containerization**: Hassle-free containerization of your Python codebase and Dockerfiles.

## Requirements 📋 

To use `fastapi-serve`, you need to have:

- Python 3.7 or higher

## Getting Started 💡

First, install the `fastapi-serve` package using pip:

```bash
pip install fastapi-serve
```

Then, simply use the `fastapi-serve` command to deploy your FastAPI application:

```bash
fastapi-serve .
```

You can also specify the name of your app:

```bash
fastapi-serve . --name my_awesome_app
```

You'll get a URL to access your newly deployed application. 🎉 

## Support 💪 

If you encounter any problems or have questions, feel free to open an issue on the GitHub repository or reach out to us directly at support@jina.ai.

## Contribute 🤝 

We welcome all contributions! If you're interested in contributing, please refer to our [Contribution Guide](CONTRIBUTING.md) for details.

## Our Cloud Platform 🌐 

`cloud.jina.ai` is our robust and scalable cloud platform designed to run your FastAPI applications with minimum hassle and maximum efficiency. With features like auto-scaling, integrated observability, and automated containerization, it provides a seamless and worry-free deployment experience.

---

`fastapi-serve` is more than just a deployment tool, it's a bridge that connects your local development environment with our powerful cloud infrastructure. Start using `fastapi-serve` today, and experience the joy of effortless deployments! 🎊 
