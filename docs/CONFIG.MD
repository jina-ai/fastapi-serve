# 💡 Jina AI Cloud

## ⚙️ Configurations

For deployment to Jina AI Cloud, you can configure your application infrastructure by providing a YAML configuration file and using the `--config` option. The supported configurations are:

  - Instance type (`instance`), as defined by [Jina AI Cloud](https://docs.jina.ai/concepts/jcloud/configuration/#cpu-tiers).
  - Minimum number of replicas for your application (`autoscale_min`). Setting it 0 enables [serverless computing](https://en.wikipedia.org/wiki/Serverless_computing).
  - Disk size (`disk_size`), in GB. The default value is 1 GB.

For example:

```yaml
instance: C4
autoscale:
  min: 0
  max: 2
disk_size: 1.5G
```

You can alternatively include a `jcloud.yaml` file in your application directory with the desired configurations. However, please note that if the `--config` option is explicitly used in the command line interface, the local jcloud.yaml file will be disregarded. The command-line-provided configuration file will take precedence.

If you don't provide a configuration file or a specific configuration isn't specified, the following default settings will be applied: 

```yaml
instance: C3
timeout: 120
autoscale:
  min: 1
  max: 10
  metric: cpu
  target: 70
disk_size: 1G
```

## 💰 Pricing

Applications hosted on Jina AI Cloud are priced in two categories:

**Base credits**

- Base credits are what you are charged to make sure at least one instance of your application is always running and ready to handle incoming requests, ensuring high availability. If you wish to stop the application, you must either remove the app completely or put it on pause. A pause allows you to resume the app later with the same configuration. (See [`fastapi-serve` CLI section](#-fastapi-serve-cli) for more information.) Both options will halt the consumption of credits.
- Charges for base credits are calculated based on the [instance type as defined by Jina AI Cloud](https://docs.jina.ai/concepts/jcloud/configuration/#cpu-tiers).
- By default, instance type `C3` is used with a minimum of 1 instance and [Amazon EFS](https://aws.amazon.com/efs/) disk of size 1GB, which means that if your application is served on Jina AI Cloud, you will be charged ~10 credits per hour.
- You can change the instance type and the minimum number of instances by providing a YAML configuration file to the deployment with the `--config` option. For example, if you want to use instance type `C4` with a minimum of 0 replicas, and 2GB EFS disk, you can provide the following configuration file:
  ```yaml
  instance: C4
  autoscale:
    min: 0
  disk_size: 2G
  ```

**Serving credits**

- Serving credits are charged when your application is actively serving incoming requests.
- Charges for serving credits are calculated based on the credits for the instance type multiplied by the amount of time your application is serving requests. 
- You are charged for each second your application is serving requests.


**Total credits charged = Base credits + Serving credits**. ([Jina AI Cloud](https://cloud.jina.ai/pricing) defines each credit as €0.005)

### Examples

<details>
<summary><b>Example 1</b></summary>

Consider an HTTP application that has served requests for `10` minutes in the last hour and uses a custom config:
```yaml
instance: C4
autoscale:
  min: 0
disk_size: 2G
```

Total credits per hour charged would be `3.33`. The calculation is as follows:
```
C4 instance has an hourly credit rate of 20.
EFS has hourly credit rate of 0.104 per GB.
Base credits = 0 + 2 * 0.104 = 0.208 (since `autoscale_min` is 0)
Serving credits = 20 * 10/60 = 3.33
Total credits per hour = 0.208 + 3.33 = 3.538
```

</details>


<details>
<summary><b>Example 2</b></summary>

Consider a WebSocket application that had active connections for 20 minutes in the last hour and uses the default configuration.
```yaml
instance: C3
autoscale:
  min: 1
disk_size: 1G
```

Total credits per hour charged would be `13.33`. The calculation is as follows:
```
C3 instance has an hourly credit rate of 10.
EFS has hourly credit rate of 0.104 per GB.
Base credits = 10 + 1 * 0.104 = 10.104 (since `autoscale_min` is 1)
Serving credits = 10 * 20/60 = 3.33
Total credits per hour = 10.104 + 3.33 = 13.434
```

</details>
