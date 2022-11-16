# ccleaner-scripts
# Whatever...
import os
import shutil
import zipfile

import lxml.html
import requests


def getLatestPortableURL():
    '''获取最新Portable'''
    url = 'https://www.ccleaner.com/zh-cn/ccleaner/builds'
    r = requests.get(url)
    doc = lxml.html.fromstring(r.content)
    id = 'GTM__download--cc-portable-build'
    return doc.xpath(f'//*[@id="{id}"]/@href')[0]


def downloadURL(url):
    '''下载文件'''
    r = requests.get(url, allow_redirects=True)
    open('ccleaner.zip', 'wb').write(r.content)


def extractZipTo(zip, folder):
    '''解压文件到文件夹'''
    with zipfile.ZipFile(zip, 'r') as zip_ref:
        zip_ref.extractall(folder)


def copyFilesInFolderTo(folder1, folder2):
    '''复制文件夹内的文件到另一个文件夹'''
    for file in os.listdir(folder1):
        shutil.copy(os.path.join(folder1, file), folder2)


def make_archive(source, destination):
    # http://www.seanbehan.com/how-to-use-python-shutil-make_archive-to-zip-up-a-directory-recursively-including-the-root-folder/
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    print(source, destination, archive_from, archive_to)
    shutil.make_archive(name, format, archive_from, archive_to)
    shutil.move('%s.%s' % (name, format), destination)


# A database of extended cleaning routines for popular Windows PC based maintenance software.
winapp2 = 'https://raw.githubusercontent.com/MoscaDotTo/Winapp2/master/Winapp2.ini'


def main():
    # 下载最新的Portable
    print('Downloading...')
    url = getLatestPortableURL()
    print(f'URL: {url}')
    downloadURL(url)
    # 解压到ccleaner目录
    print('Extracting...')
    extractZipTo('ccleaner.zip', 'ccleaner')
    # 检查CCleaner.exe是否存在
    if not os.path.exists('ccleaner/CCleaner.exe'):
        raise Exception('CCleaner.exe not found')
    # 下载winapp2.ini
    print('Downloading winapp2.ini...')
    r = requests.get(winapp2, allow_redirects=True)
    open('ccleaner/Winapp2.ini', 'wb').write(r.content)
    # 复制assets内的文件到ccleaner目录
    copyFilesInFolderTo('assets', 'ccleaner')
    # 重命名ccleaner.zip为ccleaner.zip.bak
    os.rename('ccleaner.zip', 'ccleaner.zip.bak')
    # 压缩ccleaner目录为ccleaner.zip
    print('Compressing...')
    make_archive('ccleaner', 'ccleaner.zip')
    print('Done')


if __name__ == '__main__':
    main()
