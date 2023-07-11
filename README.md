# FastAPI-Serve: Effortlessly Deploy your FastAPI Applications! 🚀 

Welcome to `fastapi-serve`, a framework designed to take the pain out of deploying your local FastAPI applications to the cloud. Built using our open-source framework [Jina](https://github.com/jina-ai/jina), `fastapi-serve` offers out-of-the-box support for automated deployments on `cloud.jina.ai`, our scalable and robust cloud platform. 🌩️ 

## Features 😍 

- 🌐 **Automatic DNS**: No more manual DNS configurations. Your app gets a unique, accessible URL automatically.
- 🔗 **HTTP/WebSocket Support**: Full support for both HTTP and WebSocket protocols.
- ↕️ **Manual Scaling**: Easily scale your app according to your needs.
- 📈 **Auto-Scaling**: Intelligent auto-scaling based on RPS (Requests Per Second), CPU, and memory usage.
- 🗝️ **Support for Secrets & Environment Variables**: Securely store and manage secrets and environment variables.
- 🔎 **Observability Stack**: Get all your logs, metrics, and traces in one place without worrying about infrastructure management.
- 📦 **Automated Containerization**: We take care of the containerization of your Python codebase, requirements.txt, and optional Dockerfiles.

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

## License 📜

`fastapi-serve` is released under the Apache 2.0 License. Check out the [LICENSE](LICENSE) file for more information.

## Contribute 🤝 

We welcome all contributions! If you're interested in contributing, please refer to our [Contribution Guide](CONTRIBUTING.md) for details.

## Our Cloud Platform 🌐 

`cloud.jina.ai` is our robust and scalable cloud platform designed to run your FastAPI applications with minimum hassle and maximum efficiency. With features like auto-scaling, integrated observability, and automated containerization, it provides a seamless and worry-free deployment experience.

---

`fastapi-serve` is more than just a deployment tool, it's a bridge that connects your local development environment with our powerful cloud infrastructure. Start using `fastapi-serve` today, and experience the joy of effortless deployments! 🎊 
