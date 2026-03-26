"""
# -*- coding: utf-8 -*-
# @Author: dr0n1
# @Link: https://www.dr0n.top/
# @Last Update: 2025/11/29
"""

import os
import sqlite3

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from styles import (
    apply_stylesheet,
    apply_stylesheets,
    style_message_box,
    BUTTON_STYLE,
    DB_DIALOG_STYLE,
    RESTORE_BUTTON_STYLE,
    TAB_WIDGET_STYLE,
    TABLE_WIDGET_STYLE,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tools.db")


def create_modules_table(cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            directory TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT '',
            sort_order INTEGER NOT NULL DEFAULT 0
        )
        '''
    )


def create_tools_table(cursor):
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            entry_path TEXT NOT NULL,
            runtime_key TEXT NOT NULL,
            arguments TEXT DEFAULT '',
            download_url TEXT DEFAULT '',
            is_enabled INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY(module_id) REFERENCES modules(id) ON DELETE CASCADE
        )
        '''
    )


def create_tables(cursor):
    # 初始化 modules/tools/config 三张表，确保基础结构存在
    create_modules_table(cursor)
    create_tools_table(cursor)
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS config
        (id INTEGER PRIMARY KEY, config_key TEXT UNIQUE, config_value TEXT)
        '''
    )


def insert_default_data(cursor):
    # 首次运行时填充默认的模块、工具条目以及配置开关
    cursor.execute('SELECT COUNT(*) FROM modules')
    if cursor.fetchone()[0] > 0:
        return

    module_defaults = [
        ("信息收集", "tools_info", "常规信息收集及敏感数据泄露检测"),
        ("框架利用工具", "tools_framework", "常见框架/中间件漏洞利用工具集合"),
        ("cms/oa利用工具", "tools_cms", "针对 CMS 与 OA 系统的利用工具"),
        ("综合利用工具", "tools_comprehensive", "多功能综合渗透工具"),
        ("内网域工具", "tools_domain", "内网域控与权限维持工具"),
        ("隧道", "tools_tunnel", "隧道与端口转发工具"),
        ("提权", "tools_privilege", "本地与远程提权工具"),
        ("WebShell管理", "tools_webshell", "常用 WebShell 管理工具"),
        ("CTF", "tools_ctf", "CTF 竞赛常用辅助工具"),
        ("reverse", "tools_reverse", "二进制/逆向工具"),
        ("misc", "tools_misc", "其他工具"),
    ]

    for order, (name, directory, description) in enumerate(module_defaults):
        cursor.execute(
            'INSERT INTO modules (name, directory, description, sort_order) VALUES (?,?,?,?)',
            (name, directory, description, order),
        )

    cursor.execute('SELECT id, name FROM modules')
    module_ids = {name: mid for mid, name in cursor.fetchall()}
    tools = get_default_tools(module_ids)
    cursor.executemany(
        '''
        INSERT INTO tools (
            module_id, name, description, entry_path, runtime_key,
            arguments, download_url, is_enabled
        ) VALUES (?,?,?,?,?,?,?,?)
        ''',
        tools,
    )

    default_configs = [
        ('use_builtin_python', 'true'),
        ('use_builtin_java', 'true'),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO config (config_key, config_value) VALUES (?,?)',
        default_configs,
    )


def get_default_tools(module_ids):
    # 构造默认工具列表并补全启用标记，便于批量写入
    legacy_defaults = [
        (module_ids["WebShell管理"], "冰蝎3", "“冰蝎”动态二进制加密网站管理客户端", "Behinder_v3.0_Beta_11.t00ls\\Behinder.jar", "java11_gui", "", "https://github.com/rebeyond/Behinder"),
        (module_ids["WebShell管理"], "冰蝎4", "“冰蝎”动态二进制加密网站管理客户端", "Behinder_v4.1.t00ls\\Behinder.jar", "java11_gui", "", "https://github.com/rebeyond/Behinder"),
        (module_ids["WebShell管理"], "哥斯拉", "哥斯拉", "Godzilla\\godzilla.jar", "java11_gui", "", "https://github.com/BeichenDream/Godzilla"),
        (module_ids["WebShell管理"], "蚁剑", "中国蚁剑是一款跨平台的开源网站管理工具", "AntSword-Loader-v4.0.3-win32-x64\\AntSword.exe", "exe_gui", "", "https://github.com/AntSwordProject/antSword"),

        (module_ids["信息收集"], "Swagger", "自动化爬取并自动测试所有swagger接口", "swagger-hack\\swagger-hack2.0.py", "python3_cli", "", "https://github.com/jayus0821/swagger-hack"),
        (module_ids["信息收集"], "dirsearch_bypass403", "目录扫描+JS文件中提取URL和子域+403状态绕过+指纹识别", "dirsearch_bypass403-3.1\\dirsearch.py", "python3_cli", "", "https://github.com/lemonlove7/dirsearch_bypass403"),
        (module_ids["信息收集"], "OneForAll", "一款功能强大的子域收集工具", "OneForAll-0.4.5\\oneforall.py", "python3_cli", "", "https://github.com/shmilylty/OneForAll"),
        (module_ids["信息收集"], "Findomain", "完整的域名识别解决方案", "findomain-windows.exe\\findomain.exe", "exe_cli", "", "https://github.com/Findomain/Findomain"),
        (module_ids["信息收集"], "TideFinger_Go", "指纹识别工具", "TideFinger_windows_amd64_v3.2.3\\TideFinger_windows_amd64_v3.2.3.exe", "exe_cli", "", "https://github.com/TideSec/TideFinger_Go"),
        (module_ids["信息收集"], "dismap", "快速识别 Web 指纹信息", "dismap\\dismap-0.4-windows-amd64.exe", "exe_cli", "", "https://github.com/zhzyker/dismap"),
        (module_ids["信息收集"], "webanalyze", "a port of Wappalyzer in Go", "webanalyze\\webanalyze.exe", "exe_cli", "", "https://github.com/rverton/webanalyze"),
        (module_ids["信息收集"], "kscan", "全方位扫描器", "kscan\\kscan_windows_amd64.exe", "exe_cli", "", "https://github.com/lcvvvv/kscan/"),
        (module_ids["信息收集"], "ENScan_GO", "一键收集控股公司ICP备案", "ENScan_GO\\enscan-v1.3.1-windows-amd64.exe", "exe_cli", "", "https://github.com/wgpsec/ENScan_GO"),
        (module_ids["信息收集"], "RustScan", "The Modern Port Scanner", "RustScan\\rustscan.exe","exe_cli", "", "https://github.com/bee-san/RustScan"),
        (module_ids["信息收集"], "ffuf", "用 Go 语言编写的快速 Web 模糊测试器", "ffuf_2.1.0_windows_amd64\\ffuf.exe", "exe_cli", "","https://github.com/ffuf/ffuf"),

        (module_ids["框架利用工具"], "Hikvision-", "Hikvision综合漏洞利用工具", "hikvision\\net8.0-windows\\hikvision漏洞利用工具.exe", "exe_gui", "", "https://github.com/MInggongK/Hikvision-"),
        (module_ids["框架利用工具"], "JumpServer", "JumpServer 堡垒机未授权综合漏洞利用", "JumpServer\\blackjump.py", "python3_cli", "", "https://github.com/tarihub/blackjump"),
        (module_ids["框架利用工具"], "SpringBoot-Scan", "针对SpringBoot的开源渗透框架", "springboot\\SpringBoot-Scan-2.7\\SpringBoot-Scan.py", "python3_cli", "", "https://github.com/AabyssZG/SpringBoot-Scan"),
        (module_ids["框架利用工具"], "OA-EXPTOOL", "OA综合利用工具", "OA-EXPTOOL-0.83\\scan.py", "python3_cli", "", "https://github.com/LittleBear4/OA-EXPTOOL"),
        (module_ids["框架利用工具"], "Thinkphp", "Thinkphp(GUI)漏洞利用工具", "thinkphp\\ThinkphpGUI-1.3-SNAPSHOT.jar", "java8_gui", "", "https://github.com/Lotus6/ThinkphpGUI"),
        (module_ids["框架利用工具"], "nacos", "Nacos漏洞综合利用GUI工具", "nacos\\NacosExploitGUI_v4.0.jar", "java8_gui", "", "https://github.com/charonlight/NacosExploitGUI"),
        (module_ids["框架利用工具"], "confluence", "Confluence CVE 2021，2022，2023 利用工具", "confluence\\confluence_memshell-1.1-SNAPSHOT.jar", "java8_gui", "", "https://github.com/Lotus6/ConfluenceMemshell"),
        (module_ids["框架利用工具"], "ShiroAttack2", "shiro反序列化漏洞综合利用", "shiro\\shiro_attack-4.7.0-SNAPSHOT-all.jar", "java8_gui", "", "https://github.com/SummerSec/ShiroAttack2"),
        (module_ids["框架利用工具"], "JDumpSpider", "HeapDump敏感信息提取工具", "springboot\\heapdump\\JDumpSpider-1.1-SNAPSHOT-full.jar", "java8_cli", "", "https://github.com/whwlsfb/JDumpSpider"),
        (module_ids["框架利用工具"], "heapdump_tool", "heapdump敏感信息查询工具", "springboot\\heapdump_tool\\heapdump_tool.jar", "java8_cli", "", "https://github.com/wyzxxz/heapdump_tool"),
        (module_ids["框架利用工具"], "SpringBootExploit", "一款针对SpringBootEnv页面进行快速漏洞利用", "springboot\\SpringBootExploit\\SpringBootExploit-1.3-SNAPSHOT-all.jar", "java8_gui", "", "https://github.com/0x727/SpringBootExploit"),
        (module_ids["框架利用工具"], "SpringExploitGUI", "一款Spring综合漏洞的利用工具", "springboot\\SpringExploitGUI\\XM-SpringExploitGUI-v2.3.jar", "java8_gui", "", "https://github.com/charonlight/SpringExploitGUI"),
        (module_ids["框架利用工具"], "JenkinsExploit-GUI", "一款Jenkins的综合漏洞利用工具", "jenkins\\JenkinsExploit-GUI-1.3-SNAPSHOT.jar", "java8_gui", "", "https://github.com/TheBeastofwar/JenkinsExploit-GUI"),
        (module_ids["框架利用工具"], "Struts2VulsScanTools", "Struts2全版本漏洞检测工具", "struts2\\Struts2_19.72.jar", "java8_gui", "", "https://github.com/abc123info/Struts2VulsScanTools"),
        (module_ids["框架利用工具"], "xxl-jobExploitGUI", "xxl-job最新漏洞利用工具", "xxl-job\\XXL-JOB.jar", "java8_gui", "", "https://github.com/charonlight/xxl-jobExploitGUI"),
        (module_ids["框架利用工具"], "WeblogicTool", "WeblogicTool，GUI漏洞利用工具", "Weblogic\\WeblogicTool_1.3.jar", "java8_gui", "", "https://github.com/KimJun1010/WeblogicTool"),
        (module_ids["框架利用工具"], "dahuaExploitGUI", "dahua综合漏洞利用工具", "dahua\\DahuaExploitGUI.jar", "java8_gui", "", "https://github.com/MInggongK/dahuaExploitGUI"),
        (module_ids["框架利用工具"], "jeecg-", "Jeecg-Boot综合漏洞利用工具", "jeecg\\jeecg-boot\\jeecgExploitss.jar", "java8_gui", "", "https://github.com/MInggongK/jeecg-"),
        (module_ids["框架利用工具"], "Jeecg_Tools", "jeecg框架漏洞利用工具", "jeecg\\jeecg\\Jeecg_Tools-1.0-java8.jar", "java8_gui", "", "https://github.com/K-7H7l/Jeecg_Tools"),
        (module_ids["框架利用工具"], "redis-rogue-server", "Redis(<=5.0.5) RCE", "redis-rogue-server-master","file_folder", "", "https://github.com/n0b0dyCN/redis-rogue-server"),

        (module_ids["cms/oa利用工具"], "若依RuoYi", "若依v4.7.8定时任务rce", "RuoYi\\RuoYiExploitGUI_v1.0.jar", "java11_gui", "", "https://github.com/charonlight/RuoYiExploitGUI"),
        (module_ids["cms/oa利用工具"], "帆软", "帆软bi反序列漏洞利用工具", "Frchannel\\FrChannel-v3.jar", "java11_gui", "", "https://github.com/7wkajk/Frchannel"),
        (module_ids["cms/oa利用工具"], "帆软 plus", "帆软bi反序列化漏洞利用工具", "Frchannel\\FrChannelPlus.jar", "java11_gui", "", "https://github.com/BambiZombie/FrchannelPlus"),
        (module_ids["cms/oa利用工具"], "用友", "用友漏洞一键探测利用", "YONYOU-TOOL\\YONYOU-TOOL-2.0.9.jar", "java11_gui", "", "https://github.com/Chave0v0/YONYOU-TOOL"),
        (module_ids["cms/oa利用工具"], "I-Wanna-Get-All", "OA漏洞利用工具", "I-Wanna-Get-All\\IWannaGetAll-v1.4.0.jar", "java8_gui", "", "https://github.com/R4gd0ll/I-Wanna-Get-All"),
        (module_ids["cms/oa利用工具"], "MYExploit", "一款基于产品的一键扫描工具", "MYExploit\\MYExploit.jar", "java11_gui", "", "https://github.com/achuna33/MYExploit"),
        (module_ids["cms/oa利用工具"], "Exp-Tools", "OA综合漏洞利用工具", "Exp-Tools\\Exp-Tools-1.3.1-encrypted.jar", "java8_gui", "-javaagent:Exp-Tools-1.3.1-encrypted.jar", "https://github.com/cseroad/Exp-Tools"),
        (module_ids["cms/oa利用工具"], "TongdaOATool", "通达OA漏洞检测工具", "tongda\\TongdaTools.jar", "java11_gui", "", "https://github.com/xiaokp7/TongdaOATool"),

        (module_ids["综合利用工具"], "mdut", "中文的数据库跨平台利用工具", "mdut\\Multiple.Database.Utilization.Tools-2.1.1-jar-with-dependencies.jar", "java11_gui", "", "https://github.com/SafeGroceryStore/MDUT"),
        (module_ids["综合利用工具"], "蓝队分析研判工具箱", "蓝队分析研判工具箱", "BlueTeamTools\\BlueTeam_ABC_123.jar", "java11_gui", "", "https://github.com/abc123info/BlueTeamTools"),
        (module_ids["综合利用工具"], "API-Explorer", "API接口管理工具", "API-Explorer\\API-Explorer.exe", "exe_gui", "", "https://github.com/mrknow001/API-Explorer"),
        (module_ids["综合利用工具"], "aliyun-accesskey-Tools", "阿里云accesskey利用工具", "aliyun\\Aliyun-.AK.Tools-V1.3.exe", "exe_gui", "", "https://github.com/mrknow001/aliyun-accesskey-Tools"),
        (module_ids["综合利用工具"], "sqlmap", "自动 SQL 注入和数据库接管工具", "sqlmap-1.9\\sqlmap.py", "python3_cli", "", "https://github.com/sqlmapproject/sqlmap"),
        (module_ids["综合利用工具"], "oracleShell", "oracle 数据库命令执行", "oracleShell\\oracleShell.jar", "java11_gui", "", "https://github.com/jas502n/oracleShell"),
        (module_ids["综合利用工具"], "DecryptTools", "DecryptTools-综合解密", "DecryptTools\\DecryptTools.jar", "java11_gui", "", "https://github.com/wafinfo/DecryptTools"),
        (module_ids["综合利用工具"], "Hyacinth", "一款java漏洞集合工具", "Hyacinth\\hyacinth-v2.1.jar", "java11_gui", "", "https://github.com/pureqh/Hyacinth"),
        (module_ids["综合利用工具"], "poc2jar", "漏洞验证、利用工具", "poc2jar-WINDOWS\\poc2jar.jar", "java11_gui", "", "https://github.com/f0ng/poc2jar"),
        (module_ids["综合利用工具"], "api-tool", "互联网厂商API利用工具", "api-tool\\API-T00L_v1.3.jar", "java11_gui", "", "https://github.com/pykiller/API-T00L"),
        (module_ids["综合利用工具"], "Postgresql", "Postgresql红队实战漏洞利用工具", "Postgresql\\postgreUtil-1.0-SNAPSHOT-jar-with-dependencies.jar", "java8_gui", "", "https://mp.weixin.qq.com/s/0s6CTAjwd5-qN6IxupwC9w"),
        (module_ids["综合利用工具"], "cloudsword", "云鉴 CloudSword", "cloudsword\\cloudsword.exe", "exe_cli", "", "https://github.com/wgpsec/cloudsword"),
        (module_ids["综合利用工具"], "unauthorized", "常见的未授权漏洞检测", "unauthorized\\unauthorizedV2.exe", "exe_gui", "", "https://github.com/xk11z/unauthorized"),

        (module_ids["内网域工具"], "fscan", "一款内网综合扫描工具", "fscan", "file_folder", "", "https://github.com/shadow1ng/fscan"),
        (module_ids["内网域工具"], "TxPortMap", "Port Scanner & Banner Identify From TianXiang", "TxPortMap", "file_folder", "", "https://github.com/4dogs-cn/TXPortMap"),
        (module_ids["内网域工具"], "ServerScan", "内网横向信息收集的高并发网络扫描、服务探测工具", "ServerScan", "file_folder", "", "https://github.com/Adminisme/ServerScan"),
        (module_ids["内网域工具"], "mimikatz", "一个用于测试 Windows 安全性的小工具", "mimikatz", "file_folder", "", "https://github.com/gentilkiwi/mimikatz"),
        (module_ids["内网域工具"], "impacket", "Impacket 是一组用于处理网络协议的 Python 类", "impacket-0.13.0", "file_folder", "", "https://github.com/fortra/impacket"),
        (module_ids["内网域工具"], "Invoke-TheHash", "PowerShell 传递哈希值工具", "Invoke-TheHash", "file_folder", "", "https://github.com/Kevin-Robertson/Invoke-TheHash/"),
        (module_ids["内网域工具"], "DSInternals", "目录服务内部机制 (DSInternals) PowerShell 模块和框架", "DSInternals", "file_folder", "", "https://github.com/MichaelGrafnetter/DSInternals"),
        (module_ids["内网域工具"], "NetExec", "The Network Execution Tool", "NetExec", "file_folder", "", "https://github.com/Pennyw0rth/NetExec"),
        (module_ids["内网域工具"], "DomainPasswordSpray", "用于对域中的用户执行密码喷洒攻击", "DomainPasswordSpray", "file_folder", "", "https://github.com/dafthack/DomainPasswordSpray"),
        (module_ids["内网域工具"], "kekeo", "一个用于在 C 语言中操作 Microsoft Kerberos 的小工具箱", "kekeo", "file_folder", "", "https://github.com/gentilkiwi/kekeo"),
        (module_ids["内网域工具"], "PowerSploit", "A PowerShell Post-Exploitation Framework", "PowerSploit", "file_folder", "", "https://github.com/PowerShellMafia/PowerSploit/"),
        (module_ids["内网域工具"], "SharpHound", "C# Data Collector for BloodHound", "SharpHound","file_folder", "", "https://github.com/SpecterOps/SharpHound"),

        (module_ids["隧道"], "Stowaway", "多级代理工具", "Stowaway", "file_folder", "", "https://github.com/ph4ntonn/Stowaway"),
        (module_ids["隧道"], "iox", "端口转发 & 内网代理工具", "iox", "file_folder", "", "https://github.com/EddieIvan01/iox"),
        (module_ids["隧道"], "frp", "高性能的反向代理应用", "frp", "file_folder", "", "https://github.com/fatedier/frp"),
        (module_ids["隧道"], "reGeorg", "The successor to reDuh", "reGeorg-master", "file_folder", "", "https://github.com/sensepost/reGeorg"),
        (module_ids["隧道"], "Neo-reGeorg", "Neo-reGeorg 是一个旨在积极重构 reGeorg 的项目", "Neo-reGeorg-5.2.1", "file_folder", "", "https://github.com/L-codes/Neo-reGeorg"),
        (module_ids["隧道"], "chisel", "A fast TCP/UDP tunnel over HTTP", "chisel", "file_folder", "", "https://github.com/jpillora/chisel"),

        (module_ids["CTF"], "焚靖", "Jinja SSTI绕过WAF的全自动脚本", "fenjing", "python3_module", "webui", "https://github.com/Marven11/Fenjing"),
        (module_ids["CTF"], "git", "提取远程 git 泄露或本地 git 的工具", "Git_Extract-master\\git_extract.py", "python3_cli", "", "https://github.com/gakki429/Git_Extract"),
        (module_ids["CTF"], "dirsearch", "Web path scanner", "dirsearch-0.4.3\\dirsearch.py", "python3_cli", "", "https://github.com/maurosoria/dirsearch"),
        (module_ids["CTF"], "arjun", "HTTP parameter discovery suite.", "arjun", "python3_module", "", "https://github.com/s0md3v/Arjun"),
        (module_ids["CTF"], "svnExploit", "SVN源代码泄露全版本Dump源码", "svnExploit\\SvnExploit.py", "python3_cli", "", "https://github.com/admintony/svnExploit"),
        (module_ids["CTF"], "ApereoCas", "ApereoCas反序列化回显与检测", "ysoserial-mangguogan-master\\ysoserial-managguogan-0.0.1-SNAPSHOT-all.jar", "java11_cui", "","https://github.com/JulianWu520/ysoserial-mangguogan"),

        (module_ids["提权"], "linux-exploit-suggester", "Linux privilege escalation auditing tool", "linux-exploit-suggester", "file_folder", "", "https://github.com/The-Z-Labs/linux-exploit-suggester/"),
        (module_ids["提权"], "windows-kernel-exploits", "Windows平台提权漏洞集合", "windows-kernel-exploits", "file_folder", "","https://github.com/SecWiki/windows-kernel-exploits"),
        (module_ids["提权"], "traitor", "linux自动提权", "traitor", "file_folder", "", "https://github.com/liamg/traitor"),
        (module_ids["提权"], "PEASS-ng", "自动提权", "PEASS-ng", "file_folder", "", "https://github.com/peass-ng/PEASS-ng"),

        (module_ids["reverse"], "GDRE", "Godot RE Tools", "GDRE_tools-v2.4.0-windows\\gdre_tools.exe", "exe_gui", "","https://github.com/GDRETools/gdsdecomp"),
        (module_ids["reverse"], "wabt", "The WebAssembly Binary Toolkit", "wabt-1.0.39\\bin", "file_folder", "","https://github.com/WebAssembly/wabt"),

        (module_ids["misc"], "ToolsFx", "跨平台密码学工具箱。", "ToolsFx-1.19.0-withjre-win-x64\\ToolsFx.exe", "exe_gui", "","https://github.com/Leon406/ToolsFx"),
        (module_ids["misc"], "busybox", "linux工具箱。", "busybox", "file_folder", "", "https://www.busybox.net/"),
    ]

    processed_defaults = []
    for (
        module_id,
        name,
        description,
        entry_path,
        runtime_key,
        arguments,
        download_url
    ) in legacy_defaults:
        processed_defaults.append((
            module_id,
            name,
            description,
            entry_path,
            runtime_key,
            arguments,
            download_url,
            1,
        ))

    return processed_defaults


def create_db():
    # 创建数据库文件并写入默认数据
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        create_tables(cursor)
        insert_default_data(cursor)
        conn.commit()


def upgrade_db():
    # 升级数据库结构并在空库时回填默认数据
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        create_tables(cursor)
        cursor.execute('SELECT COUNT(*) FROM modules')
        modules_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM tools')
        tools_count = cursor.fetchone()[0]
        if modules_count == 0 and tools_count == 0:
            insert_default_data(cursor)
        conn.commit()


def _exec_message_box(parent, title, text, icon, buttons, default_button):
    box = QMessageBox(parent)
    box.setWindowTitle(title)
    box.setText(text)
    box.setIcon(icon)
    box.setStandardButtons(buttons)
    box.setDefaultButton(default_button)
    style_message_box(box)
    return box.exec()


def _restore_database_defaults(dialog, parent, *reload_callbacks, default_button=QMessageBox.No):
    # 用户确认后清空三张表并恢复默认数据，同时刷新界面展示
    confirm = _exec_message_box(
        dialog,
        "确认恢复",
        "⚠️ 警告：此操作将删除所有自定义数据并恢复为默认配置！",
        QMessageBox.Icon.Warning,
        QMessageBox.Yes | QMessageBox.No,
        default_button,
    )
    if confirm != QMessageBox.Yes:
        return False

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tools')
            c.execute('DELETE FROM modules')
            c.execute('DELETE FROM config')
            insert_default_data(c)
            conn.commit()

        for callback in reload_callbacks:
            if callable(callback):
                callback()

        if hasattr(parent, 'load_modules'):
            parent.load_modules()

        _exec_message_box(
            dialog,
            "恢复成功",
            "数据库已成功恢复为默认配置！",
            QMessageBox.Icon.Information,
            QMessageBox.Ok,
            QMessageBox.Ok,
        )
        return True
    except Exception as exc:
        _exec_message_box(
            dialog,
            "恢复失败",
            f"恢复默认配置时发生错误：\n{exc}",
            QMessageBox.Icon.Critical,
            QMessageBox.Ok,
            QMessageBox.Ok,
        )
        return False


def restore_database_defaults(dialog, *reload_callbacks):
    # 用于全局快捷键触发的恢复默认（不依赖外层窗口回调）
    callbacks = [cb for cb in reload_callbacks if callable(cb)]
    return _restore_database_defaults(dialog, None, *callbacks, default_button=QMessageBox.Yes)


def show_database_dialog(parent):
    # 打开数据库管理对话框，加载模块/工具表格并绑定交互事件
    dialog = QDialog(parent)
    dialog.setWindowTitle("数据库管理")
    dialog.resize(1200, 800)
    dialog.setMinimumSize(1000, 700)
    dialog.setMaximumSize(1600, 1000)

    apply_stylesheet(dialog, DB_DIALOG_STYLE)

    tabs = _create_tab_widget(dialog)
    module_tab, module_table, module_buttons = _create_module_tab(tabs)
    tool_tab, tool_table, tool_buttons = _create_tool_tab(tabs)

    main_layout = QVBoxLayout(dialog)
    main_layout.addWidget(tabs)

    _load_module_data(module_table)
    _bind_module_events(
        module_table,
        module_buttons,
        dialog,
        parent,
        lambda: _load_tool_data(tool_table)
    )
    _bind_tool_events(
        tool_table,
        tool_buttons,
        dialog,
        parent,
        lambda: _load_module_data(module_table)
    )
    _load_tool_data(tool_table)

    def refresh_dialog_tables():
        _load_module_data(module_table)
        _load_tool_data(tool_table)

    if parent is not None:
        parent._db_dialog_refresh = refresh_dialog_tables

    def closeEvent(event):
        if hasattr(parent, 'load_modules'):
            parent.load_modules()
        event.accept()
    dialog.closeEvent = closeEvent

    try:
        result = dialog.exec()
    finally:
        if parent is not None and getattr(parent, "_db_dialog_refresh", None) is refresh_dialog_tables:
            parent._db_dialog_refresh = None
    return result == QDialog.Accepted


def _create_tab_widget(parent):
    # 创建带主题样式的 Tab 容器
    tabs = QTabWidget(parent)
    apply_stylesheet(tabs, TAB_WIDGET_STYLE)
    return tabs


def _create_module_tab(tabs):
    # 组装模块管理页的表格与按钮布局
    module_tab = QWidget()
    module_layout = QVBoxLayout(module_tab)
    module_layout.setSpacing(12)
    module_layout.setContentsMargins(16, 16, 16, 16)

    tableWidget = _create_table_widget()
    module_layout.addWidget(tableWidget)

    btns_layout = QHBoxLayout()
    btns_layout.setSpacing(12)
    btn_add_row = QPushButton("➕ 新增一行")
    btn_delete_row = QPushButton("🗑️ 删除选中")
    btn_restore_default = QPushButton("🔄 恢复默认")
    btn_refresh = QPushButton("🔄 刷新")
    btn_close = QPushButton("❌ 关闭")

    apply_stylesheets([btn_add_row, btn_delete_row, btn_refresh, btn_close], BUTTON_STYLE)
    apply_stylesheet(btn_restore_default, RESTORE_BUTTON_STYLE)

    btns_layout.addWidget(btn_add_row)
    btns_layout.addWidget(btn_delete_row)
    btns_layout.addWidget(btn_restore_default)
    btns_layout.addWidget(btn_refresh)
    btns_layout.addStretch()
    btns_layout.addWidget(btn_close)
    module_layout.addLayout(btns_layout)

    tabs.addTab(module_tab, "📁 模块管理")
    return module_tab, tableWidget, (btn_add_row, btn_delete_row, btn_restore_default, btn_refresh, btn_close)


def _create_tool_tab(tabs):
    # 组装工具管理页的表格与按钮布局
    tool_tab = QWidget()
    tool_layout = QVBoxLayout(tool_tab)
    tool_layout.setSpacing(12)
    tool_layout.setContentsMargins(16, 16, 16, 16)

    tool_table = _create_table_widget()
    tool_layout.addWidget(tool_table)

    tool_btns_layout = QHBoxLayout()
    tool_btns_layout.setSpacing(12)
    btn_add_row = QPushButton("➕ 新增一行")
    btn_delete_row = QPushButton("🗑️ 删除选中")
    btn_restore_default = QPushButton("🔄 恢复默认")
    btn_refresh = QPushButton("🔄 刷新")
    btn_close = QPushButton("❌ 关闭")

    apply_stylesheets([btn_add_row, btn_delete_row, btn_refresh, btn_close], BUTTON_STYLE)
    apply_stylesheet(btn_restore_default, RESTORE_BUTTON_STYLE)

    tool_btns_layout.addWidget(btn_add_row)
    tool_btns_layout.addWidget(btn_delete_row)
    tool_btns_layout.addWidget(btn_restore_default)
    tool_btns_layout.addWidget(btn_refresh)
    tool_btns_layout.addStretch()
    tool_btns_layout.addWidget(btn_close)
    tool_layout.addLayout(tool_btns_layout)

    tabs.addTab(tool_tab, "🔧 工具管理")
    return tool_tab, tool_table, (btn_add_row, btn_delete_row, btn_restore_default, btn_refresh, btn_close)


def _create_table_widget():
    # 统一创建带交替行色与主题样式的表格控件
    tableWidget = QTableWidget()
    tableWidget.setAlternatingRowColors(True)
    tableWidget.setFocusPolicy(Qt.NoFocus)
    tableWidget.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
    tableWidget.verticalHeader().setDefaultSectionSize(50)
    tableWidget.verticalHeader().setMinimumSectionSize(45)

    apply_stylesheet(tableWidget, TABLE_WIDGET_STYLE)
    return tableWidget


def _load_module_data(tableWidget):
    # 从 modules 表加载数据填充表格，保持排序与只读 ID
    tableWidget.blockSignals(True)
    tableWidget.setSortingEnabled(False)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, name, directory, description, sort_order FROM modules ORDER BY sort_order, id')
            modules = c.fetchall()

        tableWidget.clearContents()
        tableWidget.setRowCount(len(modules))
        tableWidget.setColumnCount(5)
        tableWidget.setHorizontalHeaderLabels(['模块名称', '目录', '描述', '排序', 'ID'])

        for row, (module_id, name, directory, description, sort_order) in enumerate(modules):
            name_item = QTableWidgetItem(name)
            name_item.setToolTip(name)
            tableWidget.setItem(row, 0, name_item)
            dir_item = QTableWidgetItem(directory)
            dir_item.setToolTip(directory)
            tableWidget.setItem(row, 1, dir_item)
            desc_text = description or ''
            desc_item = QTableWidgetItem(desc_text)
            desc_item.setToolTip(desc_text)
            tableWidget.setItem(row, 2, desc_item)
            tableWidget.setItem(row, 3, QTableWidgetItem(str(sort_order)))
            id_item = QTableWidgetItem(str(module_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            tableWidget.setItem(row, 4, id_item)
    finally:
        tableWidget.blockSignals(False)
        tableWidget.setSortingEnabled(True)

    tableWidget.setColumnHidden(4, True)
    header = tableWidget.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Stretch)


def _bind_module_events(tableWidget, buttons, dialog, parent, tool_reload=None):
    # 绑定模块表格的增删改事件并自动持久化到数据库
    btn_add_row, btn_delete_row, btn_restore_default, btn_refresh, btn_close = buttons
    btn_close.clicked.connect(dialog.accept)

    def auto_save():
        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute('SELECT id, name, directory, description, sort_order FROM modules')
                existing_modules = {
                    row[0]: (row[1], row[2], row[3] or '', row[4])
                    for row in c.fetchall()
                }

                retained_ids = set()
                desired_updates = {}
                new_entries = []

                for row in range(tableWidget.rowCount()):
                    name_item = tableWidget.item(row, 0)
                    directory_item = tableWidget.item(row, 1)
                    description_item = tableWidget.item(row, 2)
                    order_item = tableWidget.item(row, 3)
                    id_item = tableWidget.item(row, 4)

                    name = name_item.text().strip() if name_item and name_item.text() else ''
                    directory = directory_item.text().strip() if directory_item and directory_item.text() else ''
                    if not name or not directory:
                        continue
                    description = description_item.text().strip() if description_item and description_item.text() else ''
                    try:
                        sort_order = int(order_item.text()) if order_item and order_item.text() else row
                    except ValueError:
                        sort_order = row

                    module_id = int(id_item.text()) if id_item and id_item.text().isdigit() else None
                    if module_id is not None:
                        retained_ids.add(module_id)
                        desired_updates[module_id] = (name, directory, description, sort_order)
                    else:
                        new_entries.append((row, name, directory, description, sort_order))

                for module_id in set(existing_modules) - retained_ids:
                    c.execute('DELETE FROM tools WHERE module_id = ?', (module_id,))
                    c.execute('DELETE FROM modules WHERE id = ?', (module_id,))

                for module_id, data in desired_updates.items():
                    if existing_modules.get(module_id) != data:
                        name, directory, description, sort_order = data
                        c.execute(
                            'UPDATE modules SET name = ?, directory = ?, description = ?, sort_order = ? WHERE id = ?',
                            (name, directory, description, sort_order, module_id)
                        )

                if new_entries:
                    for row_index, name, directory, description, sort_order in new_entries:
                        c.execute(
                            'INSERT INTO modules (name, directory, description, sort_order) VALUES (?,?,?,?)',
                            (name, directory, description, sort_order)
                        )
                        new_id = c.lastrowid
                        tableWidget.blockSignals(True)
                        tableWidget.setItem(row_index, 4, QTableWidgetItem(str(new_id)))
                        tableWidget.blockSignals(False)

                conn.commit()

                if hasattr(parent, 'load_modules'):
                    parent.load_modules()
                if tool_reload:
                    tool_reload()
        except Exception as e:
            print(f"自动保存失败: {e}")

    def add_row():
        new_row = tableWidget.rowCount()
        tableWidget.insertRow(new_row)
        tableWidget.blockSignals(True)
        tableWidget.setItem(new_row, 3, QTableWidgetItem(str(new_row)))
        tableWidget.setItem(new_row, 4, QTableWidgetItem(''))
        tableWidget.blockSignals(False)
        tableWidget.setCurrentCell(new_row, 0)
        tableWidget.edit(tableWidget.currentIndex())

    def delete_selected():
        rows = sorted({i.row() for i in tableWidget.selectedIndexes()}, reverse=True)
        if rows:
            for r in rows:
                tableWidget.removeRow(r)
            auto_save()

    def restore_default():
        callbacks = [lambda: _load_module_data(tableWidget)]
        if tool_reload:
            callbacks.append(tool_reload)
        _restore_database_defaults(dialog, parent, *callbacks)

    def refresh_modules():
        _load_module_data(tableWidget)

    def on_item_changed():
        auto_save()

    btn_add_row.clicked.connect(add_row)
    btn_delete_row.clicked.connect(delete_selected)
    btn_restore_default.clicked.connect(restore_default)
    btn_refresh.clicked.connect(refresh_modules)
    tableWidget.itemChanged.connect(on_item_changed)


def _bind_tool_events(tool_table, buttons, dialog, parent, module_reload=None):
    # 绑定工具表格的增删查改逻辑并与模块列表联动
    btn_add_row, btn_delete_row, btn_restore_default, btn_refresh, btn_close = buttons
    btn_close.clicked.connect(dialog.accept)

    def _get_text(row, column):
        item = tool_table.item(row, column)
        return item.text().strip() if item and item.text() else ''

    def _select_row_by_id(tool_id):
        if not tool_id:
            return
        for row in range(tool_table.rowCount()):
            id_item = tool_table.item(row, 8)
            if id_item and id_item.text() == str(tool_id):
                tool_table.selectRow(row)
                tool_table.scrollToItem(id_item)
                break

    def add_row():
        new_row = tool_table.rowCount()
        tool_table.insertRow(new_row)
        tool_table.blockSignals(True)
        for column in range(8):
            tool_table.setItem(new_row, column, QTableWidgetItem(""))
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT name FROM modules ORDER BY sort_order, id LIMIT 1')
            first_module = c.fetchone()
        tool_table.setItem(new_row, 6, QTableWidgetItem(first_module[0] if first_module else ""))
        tool_table.setItem(new_row, 7, QTableWidgetItem("1"))
        id_item = QTableWidgetItem('')
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        tool_table.setItem(new_row, 8, id_item)
        tool_table.blockSignals(False)
        tool_table.setCurrentCell(new_row, 0)
        tool_table.edit(tool_table.currentIndex())

    def delete_selected():
        rows = sorted({i.row() for i in tool_table.selectedIndexes()}, reverse=True)
        if rows:
            tool_ids = []
            for r in rows:
                item = tool_table.item(r, 8)
                if item and item.text().isdigit():
                    tool_ids.append(int(item.text()))
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                if tool_ids:
                    c.executemany('DELETE FROM tools WHERE id = ?', [(tool_id,) for tool_id in tool_ids])
                    conn.commit()
            _load_tool_data(tool_table)
            if hasattr(parent, 'load_modules'):
                parent.load_modules()
            if module_reload:
                module_reload()

    def restore_default():
        callbacks = [lambda: _load_tool_data(tool_table)]
        if module_reload:
            callbacks.append(module_reload)
        _restore_database_defaults(dialog, parent, *callbacks)

    def refresh_tools():
        _load_tool_data(tool_table)

    def save_row(row):
        name = _get_text(row, 0)
        entry_path = _get_text(row, 2)
        runtime_key = _get_text(row, 3)
        module_name = _get_text(row, 6)

        if not name or not entry_path or not runtime_key or not module_name:
            return None

        description = _get_text(row, 1)
        arguments = _get_text(row, 4)
        download_url = _get_text(row, 5)
        enabled_text = _get_text(row, 7).lower()
        is_enabled = 0 if enabled_text in {'0', 'false', 'no', '禁用'} else 1

        id_item = tool_table.item(row, 8)
        tool_id = int(id_item.text()) if id_item and id_item.text().isdigit() else None

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM modules WHERE name = ?', (module_name,))
            module_row = c.fetchone()
            if not module_row:
                _exec_message_box(
                    dialog,
                    "保存失败",
                    f"模块“{module_name}”不存在，请先在模块管理中创建或选择有效模块。",
                    QMessageBox.Icon.Warning,
                    QMessageBox.Ok,
                    QMessageBox.Ok,
                )
                _load_tool_data(tool_table)
                return None

            module_id = module_row[0]
            values = (module_id, name, description, entry_path, runtime_key, arguments, download_url, is_enabled)

            if tool_id:
                c.execute(
                    '''
                    UPDATE tools
                    SET module_id = ?, name = ?, description = ?, entry_path = ?, runtime_key = ?,
                        arguments = ?, download_url = ?, is_enabled = ?
                    WHERE id = ?
                    ''',
                    (*values, tool_id)
                )
                conn.commit()
                saved_id = tool_id
            else:
                c.execute(
                    '''
                    INSERT INTO tools (
                        module_id, name, description, entry_path, runtime_key,
                        arguments, download_url, is_enabled
                    ) VALUES (?,?,?,?,?,?,?,?)
                    ''',
                    values
                )
                conn.commit()
                saved_id = c.lastrowid

        _load_tool_data(tool_table)
        _select_row_by_id(saved_id)
        if hasattr(parent, 'load_modules'):
            parent.load_modules()
        return saved_id

    def on_item_changed(item):
        if item.column() == 8:
            return
        save_row(item.row())

    btn_add_row.clicked.connect(add_row)
    btn_delete_row.clicked.connect(delete_selected)
    btn_restore_default.clicked.connect(restore_default)
    btn_refresh.clicked.connect(refresh_tools)
    tool_table.itemChanged.connect(on_item_changed)


def _load_tool_data(tool_table):
    # 从 tools 与 modules 联表查询工具数据并填充表格
    tool_table.blockSignals(True)
    tool_table.setSortingEnabled(False)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT
                    t.id,
                    t.name,
                    t.description,
                    t.entry_path,
                    t.runtime_key,
                    t.arguments,
                    t.download_url,
                    t.is_enabled,
                    m.name
                FROM tools t
                LEFT JOIN modules m ON t.module_id = m.id
                ORDER BY LOWER(IFNULL(m.name, '')), LOWER(t.name), t.id
                '''
            )
            tools = c.fetchall()

        tool_table.clearContents()
        tool_table.setRowCount(len(tools))
        tool_table.setColumnCount(9)
        tool_table.setHorizontalHeaderLabels([
            '工具名称', '描述', '入口路径', '运行环境', '运行参数',
            '下载地址', '所属模块', '启用', 'ID'
        ])

        for row, (
            tool_id,
            tool_name,
            description,
            entry_path,
            runtime_key,
            arguments,
            download_url,
            is_enabled,
            module_name
        ) in enumerate(tools):
            name_text = tool_name or ''
            name_item = QTableWidgetItem(name_text)
            name_item.setToolTip(name_text)
            tool_table.setItem(row, 0, name_item)

            desc_text = description or ''
            desc_item = QTableWidgetItem(desc_text)
            desc_item.setToolTip(desc_text)
            tool_table.setItem(row, 1, desc_item)

            entry_text = entry_path or ''
            entry_item = QTableWidgetItem(entry_text)
            entry_item.setToolTip(entry_text)
            tool_table.setItem(row, 2, entry_item)

            runtime_item = QTableWidgetItem(runtime_key or '')
            tool_table.setItem(row, 3, runtime_item)

            args_text = arguments or ''
            args_item = QTableWidgetItem(args_text)
            args_item.setToolTip(args_text)
            tool_table.setItem(row, 4, args_item)

            download_text = download_url or ''
            download_item = QTableWidgetItem(download_text)
            download_item.setToolTip(download_text)
            tool_table.setItem(row, 5, download_item)

            module_text = module_name or ''
            module_item = QTableWidgetItem(module_text)
            module_item.setToolTip(module_text)
            tool_table.setItem(row, 6, module_item)

            enabled_item = QTableWidgetItem("1" if is_enabled else "0")
            tool_table.setItem(row, 7, enabled_item)

            id_item = QTableWidgetItem(str(tool_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            tool_table.setItem(row, 8, id_item)

        tool_table.setColumnHidden(8, True)
        header = tool_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    finally:
        tool_table.blockSignals(False)
        tool_table.setSortingEnabled(True)


__all__ = ["DB_PATH", "create_db", "upgrade_db", "restore_database_defaults", "show_database_dialog"]
