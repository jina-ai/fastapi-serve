import os
from dataclasses import dataclass, field
from typing import Dict

import click
import yaml

from fastapi_serve.cloud.errors import (
    InvalidAutoscaleMaxError,
    InvalidAutoscaleMinError,
    InvalidDiskSizeError,
    InvalidInstanceError,
)

# jcloud args
VALID_AUTOSCALE_METRICS = ['cpu', 'memory', 'rps']

# default values
DEFAULT_TIMEOUT = 120
DEFAULT_DISK_SIZE = '1G'
DEFAULT_LABEL = 'fastapi-serve'
APP_NAME = 'fastapi'
JINA_VERSION = '3.18.0'
DOCARRAY_VERSION = '0.21.0'

# jcloud urls
APP_LOGS_URL = "[https://cloud.jina.ai/](https://cloud.jina.ai/user/flows?action=detail&id={app_id}&tab=logs)"
PRICING_URL = "****{cph}**** ([Read about pricing here](https://github.com/jina-ai/langchain-serve#-pricing))"


@dataclass
class Defaults:
    instance: str = 'C3'
    autoscale_min: int = 1  # min number of replicas
    autoscale_max: int = 10  # max number of replicas
    autoscale_metric: str = 'cpu'  # cpu, memory, rps
    autoscale_cpu_target: int = 70  # 70% cpu usage
    autoscale_rps_target: int = 10  # 10 requests per second
    autoscale_stable_window: int = DEFAULT_TIMEOUT
    autoscale_revision_timeout: int = DEFAULT_TIMEOUT
    disk_size: str = DEFAULT_DISK_SIZE


@dataclass
class AutoscaleConfig:
    min: int = Defaults.autoscale_min
    max: int = Defaults.autoscale_max
    metric: str = Defaults.autoscale_metric
    target: int = Defaults.autoscale_cpu_target
    stable_window: int = Defaults.autoscale_stable_window
    revision_timeout: int = Defaults.autoscale_revision_timeout

    def __post_init__(self):
        try:
            self.min = str(self.min)
            if self.min < 1:
                raise InvalidAutoscaleMinError(self.min)
        except ValueError:
            raise InvalidAutoscaleMinError(self.min)

        try:
            self.max = str(self.max)
            if self.max < 1:
                raise InvalidAutoscaleMaxError(self.max)
        except ValueError:
            raise InvalidAutoscaleMaxError(self.max)

        if self.min > self.max:
            raise InvalidAutoscaleMaxError(self.max)

        if self.target < 1:
            raise ValueError(
                f'Invalid autoscale target {self.target}. Must be greater than 1'
            )

        if self.metric not in VALID_AUTOSCALE_METRICS:
            raise ValueError(
                f'Invalid autoscale metric {self.metric}. Valid options are {VALID_AUTOSCALE_METRICS}'
            )

        if self.metric in ['cpu', 'memory'] and self.min == 0:
            print(f'Cannot autoscale to 0 for {self.metric}. Resetting it to 1')
            self.min = 1

    def to_dict(self) -> Dict:
        return {
            'autoscale': {
                'min': self.min,
                'max': self.max,
                'metric': self.metric,
                'target': self.target,
                'stable_window': self.stable_window,
                'revision_timeout': self.revision_timeout,
            }
        }

    @classmethod
    def from_dict(cls, config: Dict):
        _autoscale = config.get('autoscale', {})
        return cls(
            min=_autoscale.get('min', cls.min),
            max=_autoscale.get('max', cls.max),
            metric=_autoscale.get('metric', cls.metric),
            target=_autoscale.get('target', cls.target),
        )


@dataclass
class JCloudConfig:
    timeout: int = DEFAULT_TIMEOUT
    instance: str = Defaults.instance
    disk_size: str = Defaults.disk_size
    autoscale: AutoscaleConfig = field(init=False)

    def __post_init__(self):
        if self.instance and not (
            self.instance.startswith(("C", "G")) and self.instance[1:].isdigit()
        ):
            raise InvalidInstanceError(self.instance)

        if self.disk_size is not None:
            if (
                isinstance(self.disk_size, str)
                and not self.disk_size.endswith(("M", "MB", "Mi", "G", "GB", "Gi"))
            ) or (isinstance(self.disk_size, int) and self.disk_size != 0):
                raise InvalidDiskSizeError(self.disk_size)

        if self.timeout < 1:
            raise ValueError(f'Invalid timeout {self.timeout}. Must be greater than 1')

        self.autoscale = AutoscaleConfig(
            stable_window=self.timeout, revision_timeout=self.timeout
        )

    def to_dict(self) -> Dict:
        jcloud_dict = {
            'jcloud': {
                'expose': True,
                'resources': {
                    'instance': self.instance,
                    'capacity': 'spot',
                },
                'network': {'healthcheck': False},
                'timeout': self.timeout,
                **self.autoscale.to_dict(),
            }
        }

        # Don't add the volume block if self.disk_size is 0
        if isinstance(self.disk_size, str):
            jcloud_dict['jcloud']['resources']['storage'] = {
                'kind': 'efs',
                'size': self.disk_size,
            }

        return jcloud_dict

    @classmethod
    def from_dict(cls, config: Dict):
        '''Sample config
        {
            "instance": "C3",
            "timeout": 120,
            "autoscale": {
                "min": 1,
                "max": 10,
                "metric": "cpu",
                "target": 70,
            },
            "disk_size": "1G"
        }
        '''
        return cls(
            instance=config.get('instance', cls.instance),
            disk_size=config.get('disk_size', cls.disk_size),
            timeout=config.get('timeout', cls.timeout),
            autoscale=AutoscaleConfig.from_dict(config.get('autoscale', {})),
        )

    @classmethod
    def from_file(cls, config_path: str):
        with open(config_path, "r") as f:
            config_data: Dict = yaml.safe_load(f)
            return cls.from_dict(config_data)


def validate_jcloud_config_callback(ctx, param, value):
    if not value:
        return None
    try:
        JCloudConfig.from_file(value)
    except InvalidInstanceError as e:
        raise click.BadParameter(
            f"Invalid instance '{e.instance}' found in config file', please refer to https://docs.jina.ai/concepts/jcloud/configuration/#cpu-tiers for instance definition."
        )
    except InvalidAutoscaleMinError as e:
        raise click.BadParameter(
            f"Invalid instance '{e.min}' found in config file', it should be a number >= 0."
        )
    except InvalidDiskSizeError as e:
        raise click.BadParameter(
            f"Invalid disk size '{e.disk_size}' found in config file."
        )

    return value


def resolve_jcloud_config(config, app_dir: str):
    # config given from CLI takes higher priority
    if config:
        return config

    # Check to see if jcloud YAML/YML file exists at app dir
    config_path_yml = os.path.join(app_dir, "jcloud.yml")
    config_path_yaml = os.path.join(app_dir, "jcloud.yaml")

    if os.path.exists(config_path_yml):
        config_path = config_path_yml
    elif os.path.exists(config_path_yaml):
        config_path = config_path_yaml
    else:
        return None

    try:
        JCloudConfig.from_file(config_path)
    except (InvalidAutoscaleMinError, InvalidInstanceError, InvalidDiskSizeError) as e:
        # If it's malformed, we treated as non-existed
        print(f'config file {config_path} is malformed: {e}')
        return None

    print(f'JCloud config file at app directory will be applied: {config_path}')
    return config_path


def get_jcloud_config(
    config_path: str = None, timeout: int = DEFAULT_TIMEOUT
) -> JCloudConfig:
    default_config = JCloudConfig(timeout=timeout)
    if not config_path:
        return default_config

    if not os.path.exists(config_path):
        print(f'config file {config_path} not found')
        return default_config

    with open(config_path, 'r') as f:
        config_data: Dict = yaml.safe_load(f)
        if not config_data:
            return default_config
        return JCloudConfig.from_dict(config_data)
