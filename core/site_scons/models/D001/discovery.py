from __future__ import annotations

from .. import get_hw_model_as_number
from ..stm32f4_common import stm32f4_common_files


def configure(
    env: dict,
    features_wanted: list[str],
    defines: list[str | tuple[str, str]],
    sources: list[str],
    paths: list[str],
) -> list[str]:
    features_available: list[str] = []
    board = "D001/boards/stm32f429i-disc1.h"
    display = "ltdc.c"
    hw_model = get_hw_model_as_number("D001")
    hw_revision = 0

    mcu = "STM32F429xx"

    stm32f4_common_files(env, defines, sources, paths)

    env.get("ENV")[
        "CPU_ASFLAGS"
    ] = "-mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16"
    env.get("ENV")[
        "CPU_CCFLAGS"
    ] = "-mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -mtune=cortex-m4 "
    env.get("ENV")["RUST_TARGET"] = "thumbv7em-none-eabihf"

    defines += [mcu]
    defines += [f'TREZOR_BOARD=\\"{board}\\"']
    defines += [f"HW_MODEL={hw_model}"]
    defines += [f"HW_REVISION={hw_revision}"]

    if "new_rendering" in features_wanted:
        sources += [
            "embed/trezorhal/xdisplay_legacy.c",
            "embed/trezorhal/stm32f4/xdisplay/stm32f429i-disc1/display_driver.c",
            "embed/trezorhal/stm32f4/xdisplay/stm32f429i-disc1/display_ltdc.c",
            "embed/trezorhal/stm32f4/xdisplay/stm32f429i-disc1/ili9341_spi.c",
        ]
    else:
        sources += [f"embed/trezorhal/stm32f4/displays/{display}"]
        sources += ["embed/trezorhal/stm32f4/displays/ili9341_spi.c"]

    if "new_rendering" in features_wanted:
        sources += ["embed/trezorhal/stm32u5/dma2d_bitblt.c"]
    else:
        sources += ["embed/trezorhal/stm32u5/dma2d.c"]

    sources += [
        "vendor/micropython/lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma2d.c"
    ]
    sources += [
        "vendor/micropython/lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma.c"
    ]
    defines += ["USE_DMA2D"]
    defines += ["USE_RGB_COLORS=1"]
    defines += ["FRAMEBUFFER"]
    features_available.append("dma2d")
    features_available.append("framebuffer")

    if "new_rendering" in features_wanted:
        defines += ["XFRAMEBUFFER"]
        defines += ["DISPLAY_RGB565"]
        features_available.append("xframebuffer")
        features_available.append("display_rgb565")

    sources += ["embed/trezorhal/stm32f4/sdram.c"]
    defines += ["USE_SDRAM=1"]

    if "input" in features_wanted:
        sources += ["embed/trezorhal/stm32f4/i2c_bus.c"]
        sources += ["embed/trezorhal/stm32f4/touch/stmpe811.c"]
        features_available.append("touch")
    defines += ["USE_TOUCH=1"]
    defines += ["USE_I2C=1"]

    if "usb" in features_wanted:
        sources += [
            "embed/trezorhal/stm32f4/usb/usb_class_hid.c",
            "embed/trezorhal/stm32f4/usb/usb_class_vcp.c",
            "embed/trezorhal/stm32f4/usb/usb_class_webusb.c",
            "embed/trezorhal/stm32f4/usb/usb.c",
            "embed/trezorhal/stm32f4/usb/usbd_conf.c",
            "embed/trezorhal/stm32f4/usb/usbd_core.c",
            "embed/trezorhal/stm32f4/usb/usbd_ctlreq.c",
            "embed/trezorhal/stm32f4/usb/usbd_ioreq.c",
            "vendor/micropython/lib/stm32lib/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll_usb.c",
        ]
        features_available.append("usb")

    defines += ["USE_PVD=1"]

    return features_available
