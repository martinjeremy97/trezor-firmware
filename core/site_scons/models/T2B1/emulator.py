from __future__ import annotations

from .. import get_hw_model_as_number


def configure(
    env: dict,
    features_wanted: list[str],
    defines: list[str | tuple[str, str]],
    sources: list[str],
    paths: list[str],
) -> list[str]:

    features_available: list[str] = []
    board = "T2B1/boards/t2b1-unix.h"
    hw_model = get_hw_model_as_number("T2B1")
    hw_revision = 0
    mcu = "STM32F427xx"

    if "new_rendering" in features_wanted:
        defines += ["XFRAMEBUFFER", "DISPLAY_MONO"]
        features_available.append("xframebuffer")
        features_available.append("display_mono")

    defines += [mcu]
    defines += [f'TREZOR_BOARD=\\"{board}\\"']
    defines += [f"HW_MODEL={hw_model}"]
    defines += [f"HW_REVISION={hw_revision}"]
    defines += [f"MCU_TYPE={mcu}"]
    defines += ["FLASH_BIT_ACCESS=1"]
    defines += ["FLASH_BLOCK_WORDS=1"]

    if "sbu" in features_wanted:
        sources += ["embed/trezorhal/unix/sbu.c"]
    defines += ["USE_SBU=1"]

    if "optiga" in features_wanted:
        sources += ["embed/trezorhal/unix/optiga_hal.c"]
        sources += ["embed/trezorhal/unix/optiga.c"]
        features_available.append("optiga")
    defines += ["USE_OPTIGA=1"]

    if "input" in features_wanted:
        sources += ["embed/trezorhal/unix/button.c"]
        features_available.append("button")
    defines += ["USE_BUTTON=1"]

    sources += ["embed/trezorhal/stm32f4/layout.c"]

    return features_available
