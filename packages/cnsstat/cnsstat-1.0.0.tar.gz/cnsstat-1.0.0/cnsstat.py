# SPDX-License-Identifier: MIT
"""Cheap-n-nasty text system status via psutil"""

import psutil
from shutil import disk_usage
from time import time, sleep
import sys
import os

# sample time for cpu & network
_TESTLEN = 4.0

# Prefix threshold
_PFXTHRESH = 0.8

# SI prefixes (base 10)
_KILO = 1000
_MEGA = _KILO * _KILO
_GIGA = _KILO * _MEGA
_TERA = _KILO * _GIGA


def getIfs(match=[]):
    """Get list of all up network interfaces, skip lo unless requested"""
    ret = []
    netIfs = psutil.net_if_stats()
    for i in netIfs:
        if i != 'lo':
            if not match or i in match:
                if netIfs[i].isup:
                    ret.append(i)
        elif match and i in match:
            ret.append(i)
    return ret


def getTemp():
    """Get platform temperature or a list of cpu package temperatures"""
    ret = []
    try:
        sense = psutil.sensors_temperatures()
        curtemp = None
        if 'acpitz' in sense:
            ret.append(sense['acpitz'][0].current)
        elif 'coretemp' in sense:
            for t in sense['coretemp']:
                if t.label.startswith('Package'):
                    ret.append(t.current)
    except Exception:
        pass
    return ret


def getHdds():
    """Get list of hard disk volumes, skipping any mounted under /boot"""
    ret = []
    for hd in psutil.disk_partitions():
        if not hd.mountpoint.startswith('/boot'):
            ret.append(hd)
    return ret


def fmtRate(hdr, startTraf, endTraf, dt):
    """Format net device traffic"""
    ret = '%s: -- n/a --' % (hdr, )
    if dt > 0.01:
        dtx = endTraf.bytes_sent - startTraf.bytes_sent
        drx = endTraf.bytes_recv - startTraf.bytes_recv
        txrate = 8 * dtx / dt
        rxrate = 8 * drx / dt
        rate = max(txrate, rxrate)
        if rate < _PFXTHRESH * _MEGA:
            ret = '%s: %0.0f | %0.0f\u2006kbit/s' % (
                hdr,
                txrate / _KILO,
                rxrate / _KILO,
            )
        elif rate < _PFXTHRESH * _GIGA:
            ret = '%s: %0.1f | %0.1f\u2006Mbit/s' % (
                hdr,
                txrate / _MEGA,
                rxrate / _MEGA,
            )
        else:
            ret = '%s: %0.2f | %0.2f\u2006Gbit/s' % (
                hdr,
                txrate / _GIGA,
                rxrate / _GIGA,
            )
    return ret


def fmtTemp(hdr):
    """Format temperature listing"""
    ret = '%s: -- n/a --' % (hdr)
    try:
        ts = getTemp()
        if len(ts) == 1:
            ret = '%s: %0.1f\u2006\u00b0C' % (hdr, ts[0])
        elif ts:
            i = 0
            rv = []
            for t in ts:
                rv.append('[%d] %0.1f\u2006\u00b0C' % (i, t))
                i += 1
            ret = '%s: %s' % (hdr, ', '.join(rv))
    except Exception:
        pass
    return ret


def fmtCpu(hdr):
    """Format cpu use and load averages"""
    ret = '%s: -- n/a --' % (hdr)
    try:
        cp = psutil.cpu_percent()
        nc = psutil.cpu_count()
        la = psutil.getloadavg()
        ret = '%s: %0.0f\u2006%%, %0.1f, %0.1f, %0.1f' % (
            hdr, cp, la[0] / nc, la[1] / nc, la[2] / nc)
    except Exception:
        pass
    return ret


def fmtMem(hdr):
    """Format memory usage"""
    ret = '%s: -- n/a --' % (hdr, )
    try:
        mem = psutil.virtual_memory()
        if mem.total > _PFXTHRESH * _TERA:
            ret = '%s: %0.0f\u2006%%, %0.2f/%0.1f\u2006TB' % (
                hdr, mem.percent, mem.used / _TERA, mem.total / _TERA)
        else:
            ret = '%s: %0.0f\u2006%%, %0.1f/%0.0f\u2006GB' % (
                hdr, mem.percent, mem.used / _GIGA, mem.total / _GIGA)
    except Exception:
        pass
    return ret


def fmtDf(hdr, volume='/'):
    """Format disk usage on named volume"""
    ret = '%s: -- n/a --' % (hdr, )
    try:
        du = disk_usage(volume)
        dpct = 100.0 * du.used / du.total
        if du.total > _PFXTHRESH * _TERA:
            ret = '%s: [%s] %0.0f\u2006%%, %0.2f/%0.1f\u2006TB' % (
                hdr,
                volume,
                dpct,
                du.used / _TERA,
                du.total / _TERA,
            )
        else:
            ret = '%s: [%s] %0.0f\u2006%%, %0.1f/%0.0f\u2006GB' % (
                hdr,
                volume,
                dpct,
                du.used / _GIGA,
                du.total / _GIGA,
            )
    except Exception:
        pass
    return ret


def main():
    # choose network interface(s)
    netIfs = []
    if len(sys.argv) > 1:
        for netIf in sys.argv[1:]:
            netIfs.append(netIf)
    netIfs = getIfs(netIfs)

    # sample
    if sys.stdout.isatty():
        print('  Sampling ~%0.0f\u2006s ...' % (_TESTLEN, ),
              file=sys.stderr,
              end='\r',
              flush=True)
    psutil.cpu_percent()
    if netIfs:
        rateStart = time()
        startTraf = psutil.net_io_counters(pernic=True)
    sleep(_TESTLEN)
    if netIfs:
        rateEnd = time()
        endTraf = psutil.net_io_counters(pernic=True)

    # report
    if sys.stdout.isatty():
        print('                                       ',
              file=sys.stderr,
              end='\r',
              flush=True)
    print(fmtCpu('Load'))
    print(fmtTemp('Temp'))
    print(fmtMem('Mem'))
    vols = getHdds()
    for vol in vols:
        hdr = vol.device.split('/')[-1]
        print(fmtDf(hdr, vol.mountpoint))
    for netIf in netIfs:
        print(
            fmtRate(netIf, startTraf[netIf], endTraf[netIf],
                    rateEnd - rateStart))


if __name__ == "__main__":
    sys.exit(main())
