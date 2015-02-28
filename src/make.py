#!/usr/bin/env python
# -*- coding: utf-8 -*-

def load_proxy(data):
    lines = data.splitlines()
    return '"{};"'.format(';'.join(lines))

def load_range(data):
    lines = data.splitlines()
    lines.append('0.0.0.0/8')
    lines.append('10.0.0.0/8')
    lines.append('127.0.0.0/8')
    lines.append('169.254.0.0/16')
    lines.append('172.16.0.0/12')
    lines.append('192.0.0.0/24')
    lines.append('192.0.2.0/24')
    lines.append('192.88.99.0/24')
    lines.append('192.168.0.0/16')
    lines.append('198.18.0.0/15')
    lines.append('198.51.100.0/24')
    lines.append('203.0.113.0/24')
    lines.append('224.0.0.0/4')
    lines.append('240.0.0.0/4')

    lines = list(set(lines))
    lines = sorted(lines, key=lambda ip: reduce(lambda x, y: (x << 8) + y, map(int, ip.split('/')[0].split('.'))))

    codelist = [[] for _ in range(256)]
    masklist = [[] for _ in range(256)]

    for line in lines:
        item = line.split('/')
        atom = item[0].split('.')
        codelist[int(atom[0])].append(int(atom[1]) << 8 | int(atom[2]) << 0)
        masklist[int(atom[0])].append(24 - int(item[1]))

    codelist = ['[{}]'.format(','.join(map(str, x))) for x in codelist]
    masklist = ['[{}]'.format(','.join(map(str, x))) for x in masklist]

    codelist = '[{}]'.format(','.join(codelist).replace('[]','0'))
    masklist = '[{}]'.format(','.join(masklist).replace('[]','0'))

    return codelist, masklist

def load_domain(data):
    lines = filter(lambda x: not x.startswith('#') and x, data.splitlines())
    domains = []
    for line in lines:
        if sum(map(line.endswith, lines)) == 1:
            domains.append(line)
    return '{{{}}}'.format(','.join(map('"{}":1'.format, domains)))

def main():
    with open('mono.js') as f:
        payload = f.read()

    with open('proxyList') as f:
        proxylist = load_proxy(f.read())

    with open('whiteList') as f:
        whitelist = load_domain(f.read())

    with open('blackList') as f:
        blacklist = load_domain(f.read())

    with open('ipList') as f:
        codelist, masklist = load_range(f.read())

    payload = payload.replace('__proxyList__', proxylist)
    payload = payload.replace('__whiteList__', whitelist)
    payload = payload.replace('__blackList__', blacklist)
    payload = payload.replace('__codeList__', codelist)
    payload = payload.replace('__maskList__', masklist)

    print(payload)

if __name__ == '__main__':
    main()