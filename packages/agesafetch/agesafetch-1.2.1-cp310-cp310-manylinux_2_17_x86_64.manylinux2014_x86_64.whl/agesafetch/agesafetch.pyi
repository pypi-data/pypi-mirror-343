# SPDX-FileCopyrightText: Benedikt Vollmerhaus <benedikt@vollmerhaus.org>
# SPDX-License-Identifier: MIT

class AGESAVersion:
    version_string: str
    absolute_address: int


def find_agesa_version() -> AGESAVersion | None: ...


class DevMemOpenError: ...


class IomemReadError: ...


class ByteReadError: ...
