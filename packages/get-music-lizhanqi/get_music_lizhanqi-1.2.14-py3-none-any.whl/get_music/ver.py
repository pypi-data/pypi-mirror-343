import requests,re
from rich.console import Console
def ver(ip=True):
    console=Console()
    if ip==True:
            try:
                html=requests.get('https://qifu-api.baidubce.com/ip/local/geo/v1/district?')
                d=html.json()
                ip=d.get('ip')
                area=' '.join([d['data']['isp'],d['data']['prov'],d['data']['city'],d['data']['district']])
                console.print('\n[b green]信息一:本机外网ip地址为:[b red]{}[/]，归属:[b red]{}[/]'.format(ip,area))
                
            except:
                console.print("\n[b red]ip地址信息一查询失败！")
            try:
                url='http://nstool.netease.com/'
                html=requests.get(url,timeout=1)
                txt=html.text
                url=re.findall("src\='(.*?)'",txt)[0]
                html=requests.get(url,timeout=1)
                msg=html.text.split('<br>')
                ip=msg[1].split(': ')[-1].split(' ')
                dns=msg[2].split(': ')[-1].split(' ')
                msg=msg[3]
                console.print('\n[b green]信息二:本机外网ip地址为:[b red]{}[/]，归属:[b red]{}[/]'.format(ip[0],ip[-1]))
                console.print('[b green]DNS服务器地址:[b red]{}[/],归属:[b red]{}[/],提示信息:[b red]{}[/]'.format(dns[0],dns[-1],msg))
            except:
                console.print("\n[b red]ip地址信息查二询失败！")

            try:
                url = 'http://api.ip33.com/ip/search?s='                     
                d = requests.get(url,timeout=1).json()                                                       
                console.print('\n[b green]信息三:本机外网ip地址为:[b red]{}[/]，归属:[b red]{}[/]'.format(d['ip'],d['area']))
            except:
                console.print("\n[b red]ip地址信息查三询失败！")
            return
    version = '1.2.14'
    console.print("[b red]当前版本:[b green]"+"v"+version)
    url = 'https://pypi.org/project/get-music-lizhanqi/'
    try:
        with console.status("[b green]检查最新版中..."):
            html = requests.get(url,timeout = 5)
            
            txt = html.text
            pattern = r'<h1 class="package-header__name">(.*?)</h1>'
            result = re.search(pattern, txt, re.DOTALL)
            if result:
                crad =result.group(1).strip()
                crad=crad.split()[1]
            else:
                exit()
            ver = crad
            ver1 = version.split('.')
            ver2 = ver.split('.')
            ls= []
            for i in range(3):
                v1 = ver1[i]
                v2 = ver2[i]
                if v2 > v1:
                    ls.append(False)
                elif v2 == v1:
                    ls.append(True)
                else:
                    ls.append(False)
        if False in ls:
            console.print('[b red]最新版本是:[b green]v'+ver+'[/],您可以用"[b green]pip install --upgrade get-music-lizhanqi[/]"命令进行更新')
            result = re.search(r'<h2>更新记录</h2>\n<ul>\n<li>(.*?)</li>', txt, re.DOTALL)
            console.print('\n[b red]更新内容:\n[b green]'+result.group(1).strip())
        else:
           console.print('[b red]最新版本是:[b green]v'+ver+'[/],您已是最新版本!')
        
    except:
##        try:
##            html=requests.get('https://pypi.tuna.tsinghua.edu.cn/simple/get-music-lizhanqi/',timeout=5)
##            s=re.findall('get-music-lizhanqi-(.*?).tar.gz',html.text)
##            s=set(s)
##            for i in s:
##                if version<i:
##                    break
##                console.print('[b red]来自清华源的最新版本是:[b green]v'+i+'[/],您可以用"[b green]pip install --upgrade get-music-lizhanqi[/]"命令进行更新')
##        except:
##            pass
        console.print("[b red]获取最新版本信息失败！请检查是否是网络的问题！")


