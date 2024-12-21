#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/miuicamera-ruby',
]

blob_fixups: blob_fixups_user_type = {
    'system_ext/priv-app/MiuiCamera/MiuiCamera.apk': blob_fixup()
        .apktool_patch('blob-patches/MIUICamera.patch'),
    ('system_ext/lib64/libcamera_algoup_jni.xiaomi.so', 'system_ext/lib64/libcamera_mianode_jni.xiaomi.so'): blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system_ext/lib64/libcamera_ispinterface_jni.xiaomi.so': blob_fixup()
        .add_needed('libgui_shim_miuicamera.so')
        .replace_needed('vendor.mediatek.hardware.camera.isphal@1.0.so', 'vendor.mediatek.hardware.camera.isphal@1.0_system.so'),
    'system_ext/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V5-ndk.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'miuicamera-ruby',
    'xiaomi',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()