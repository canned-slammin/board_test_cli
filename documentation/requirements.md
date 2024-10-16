# Board Test CLI Requirements

| Requirement | MoSCoW | Notes | Fulfilled By |
| :---------- | :----- |:----- | :----------- |
| NRF: GPIO: Configure I/O | MUST |  | Zephyr default GPIO shell
| NRF: GPIO: Set/clear output | MUST |  | Zephyr default GPIO shell
| NRF: GPIO: Read input | MUST |  | Zephyr default GPIO shell
| STM32: GPIO: Configure I/O | MUST |  | Zephyr default GPIO shell
| STM32: GPIO: Set/clear output | MUST |  | Zephyr default GPIO shell
| STM32: GPIO: Read input | MUST |  | Zephyr default GPIO shell
| NRF: I2C: Write bytes | MUST |  | Zephyr default I2C shell
| NRF: I2C: Read bytes | MUST |  | Zephyr default I2C shell
| STM32: I2C: Write bytes | MUST |  | Zephyr default I2C shell
| STM32: I2C: Read bytes | MUST |  | Zephyr default I2C shell
| NRF: SPI: Configure | MUST | Potentially fulfilled by Zephyr default SPI shell  | TBD
| NRF: SPI: Read bytes | MUST | Potentially fulfilled by Zephyr default SPI shell | TBD
| NRF: SPI: Write bytes | MUST | Potentially fulfilled by Zephyr default SPI shell | TBD
| STM32: SPI: Configure | MUST | Potentially fulfilled by Zephyr default SPI shell | TBD
| STM32: SPI: Read bytes | MUST | Potentially fulfilled by Zephyr default SPI shell | TBD
| STM32: SPI: Write bytes | MUST | Potentially fulfilled by Zephyr default SPI shell | TBD
| NRF: PWM: Configure | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| NRF: PWM: Enable/Disable | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| NRF: PWM: Set pulse | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| NRF: PWM: Set period | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| STM32: PWM: Configure | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| STM32: PWM: Enable/Disable | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| STM32: PWM: Set pulse | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| STM32: PWM: Set period | MUST | Potentially fulfilled by Zephyr default PWM shell | TBD
| Customer PCBA: GPIO | SHOULD | Requires building device tree overlay | TBD
| Customer PCBA: I2C | SHOULD | Requires building device tree overlay | TBD
| Customer PCBA: SPI | SHOULD | Requires building device tree overlay | TBD
| Customer PCBA: PWM | SHOULD | Requires building device tree overlay | TBD
| PICO: GPIO | SHOULD |  | TBD
| PICO: I2C | SHOULD |  | TBD
| PICO: SPI | SHOULD |  | TBD
| PICO: PWM | SHOULD |  | TBD
