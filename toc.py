#!/usr/bin/env python
import os

"""
- FlowEngine
  - API
    - [API文档](FlowEngine/API/API文档)
  - [流量引擎文档](FlowEngine/流量引擎文档)


list [
    map{
        level: 1,
        type: file or dir
        title: ,
        path: ,
    }
]
"""

md_list = []

def listfiles(path):
    files = sorted(os.listdir(path))

    dirs = []
    fs = []
    for f in files:
        new_path = os.path.join(path, f)
        if os.path.isdir(new_path):
            dirs.append(new_path)
        else:
            if not f.endswith(".md"):
                continue
            name = f[0:-3]
            if path.startswith("./"):
                parentpath = path[2:]
            else:
                parentpath = path
            
            mdpath = parentpath + "/" + name if parentpath != "" else name
            # path.find
            md_list.append({"level": mdpath.count("/"), "title": name, "path": mdpath, "parent": parentpath})
    for d in dirs:
        listfiles(d)

lines = []
type_maps = {}

def types(path):
    paths = path.split('/')
    for i in range(0, len(paths)):
        subPath = '/'.join(paths[0:i+1])
        if type_maps.get(subPath) is None:
            lines.append("    " * i + "- " + paths[i])
            type_maps[subPath] = 1

def render():
    # [FlowEngine-AdEngine-Render-主信息流-API](FlowEngine/API/FlowEngine-AdEngine-Render-主信息流-API)
    content = ""
    dirs = {}
    for item in md_list:
        types(item["parent"])
        lines.append("    " * item["level"]+"- [%s](%s)" %(item['title'], item['path']) )

render_message = '''
> 目录生成方式: 
克隆最新的wiki仓库到本地, 在wiki根路径下执行`python3 toc.py`, 生成`toc.md`后提交即可
'''

def main():
    listfiles("./")
    # 按md_list 生成文档
    render()
    content = '## 目录\n\n' + '\n'.join(lines) + "<br><br>" + render_message
    # 写入toc.md
    with open('toc.md', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    main()
