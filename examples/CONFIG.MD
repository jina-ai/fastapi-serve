# 💡 Jina AI Cloud

## ⚙️ Configurations

For JCloud deployment, you can configure your application infrastructure by providing a YAML configuration file using the `--config` option. The supported configurations are:

  - Instance type (`instance`), as defined by [Jina AI Cloud](https://docs.jina.ai/concepts/jcloud/configuration/#cpu-tiers).
  - Minimum number of replicas for your application (`autoscale_min`). Setting it 0 enables [serverless](https://en.wikipedia.org/wiki/Serverless_computing).
  - Disk size (`disk_size`), in GB. The default value is 1 GB.

For example:

```
instance: C4
autoscale_min: 0
disk_size: 1.5G
```

You can alternatively include a `jcloud.yaml` file in your application directory with the desired configurations. However, please note that if the `--config` option is explicitly used in the command line interface, the local jcloud.yaml file will be disregarded. The command line provided configuration file will take precedence.

If you don't provide a configuration file or a specific configuration isn't specified, the following default settings will be applied: 

```
instance: C3
autoscale_min: 1
disk_size: 1G
```

## 💰 Pricing

Applications hosted on JCloud are priced in two categories:

**Base credits**

- Base credits are charged to ensure high availability for your application by maintaining at least one instance running continuously, ready to handle incoming requests. If you wish to stop the serving application, you can either remove the app completely or put it on pause, the latter allows you to resume the app serving based on persisted configurations (refer to [`fastapi-serve` CLI section](#-fastapi-serve-cli) for more information). Both options will halt the consumption of credits.
- Actual credits charged for base credits are calculated based on the [instance type as defined by Jina AI Cloud](https://docs.jina.ai/concepts/jcloud/configuration/#cpu-tiers).
- By default, instance type `C3` is used with a minimum of 1 instance and [Amazon EFS](https://aws.amazon.com/efs/) disk of size 1G, which means that if your application is served on JCloud, you will be charged ~10 credits per hour.
- You can change the instance type and the minimum number of instances by providing a YAML configuration file using the `--config` option. For example, if you want to use instance type `C4` with a minimum of 0 replicas, and 2G EFS disk, you can provide the following configuration file:
  ```yaml
  instance: C4
  autoscale_min: 0
  disk_size: 2G
  ```

**Serving credits**

- Serving credits are charged when your application is actively serving incoming requests.
- Actual credits charged for serving credits are calculated based on the credits for the instance type multiplied by the duration for which your application serves requests. 
- You are charged for each second your application is serving requests.


**Total credits charged = Base credits + Serving credits**. ([Jina AI Cloud](https://cloud.jina.ai/pricing) defines each credit as €0.005)

### Examples

<details>
<summary><b>Example 1</b></summary>

Consider an HTTP application that has served requests for `10` minutes in the last hour and uses a custom config:
```
instance: C4
autoscale_min: 0
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
```
instance: C3
autoscale_min: 1
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