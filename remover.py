#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, re, sys

regex = re.compile('^(?P<name>.+\.(?:asm|prt|drw)\.)(?P<version>\d+$)')
rmfilelst = tuple(map(re.compile, (
                                         '^trail\.txt\.\d+$'
                                        ,'.+\.log(?:\.\d+)?$'
                                        ,'^current_session\.pro$'
                                        ,'^std\.out$'
                                        ,'.+\.bak$'
                                        ,'^std\.err$'
                                        ,'\.dwl\d?$'
                                    )))

def remover(path):
    print('开始清理文件夹{}...'.format(path))
    os.chdir(path)
    for root, dlst, flst in os.walk(path):
        maxversion = {}
        errornames = []
        for f in flst:
            if any(r.match(f) for r in rmfilelst):
                #确认是否是垃圾文件
                full = os.path.join(root, f)
                try:
                    os.remove(full)
                except:
                    print('删除垃圾文件{}失败！可能有程序正在访问此文件。'.format(full))
                else:
                    print('垃圾文件{}已被删除。'.format(full))
                continue

            m = regex.match(f)
            if m is None:
                continue

            name, version = m.group('name').lower(), int(m.group('version'))

            if name in errornames:
                continue

            if name not in maxversion:
                maxversion[name] = version
            else:
                if maxversion[name] < version:
                    maxversion[name], version = version, maxversion[name]
                old = os.path.join(root, name + str(version))
                try:
                    os.remove(old)
                except:
                    print('删除旧版文件{}失败！可能有程序正在访问此文件。'.format(old))
                    errornames.append(name)
                else:
                    print('旧版文件<{}>已被删除。'.format(old))
        
        versionto1 = {k:str(v) for k,v in maxversion.items() if not (k in errornames or v is 1)}
        for k,v in versionto1.items():
            old = os.path.join(root, k + v)
            try:
                os.rename(old, os.path.join(root, k + '1'))
            except:
                print('将文件{}的版本改为1失败！可能有程序正在访问此文件。'.format(old))
            else:
                print('文件<{}>的版本号已被改为1。'.format(old))
            
def confirm(path):
    print('''确定要清理文件夹<{}>吗？
=========================================================================
该文件夹（包括子文件夹）下的所有旧版本文件将被删除，且删除操作不可恢复!!!
========================================================================='''.format(path))
    return input("确认操作请输入‘yes', 输入其它字符可取消:").lower() == 'yes'


if __name__ == '__main__':
    path = os.getcwd()
    if confirm(path):
        remover(path)
        os.system('pause')
        sys.exit(0)
    else:
        sys.exit(1)

