import json

class p_txt_tool:
    def __init__(self,txt_path=None):
        self.txt_path = txt_path

    def txt_write(self,content,way = 'w'):
        allowed_values = ['w','a']
        if way not in allowed_values:
            raise ValueError("写入方式错误！目前只能为覆盖：'w'和追加：'a'嗷！")
        try:
            with open(self.txt_path,way) as file:
                file.write(content)
                print('Done！')
        except Exception as e:
            print(f'Oops!出错 {e}')

    def txt_read(self,encoding='utf-8'):
        try:
            with open(self.txt_path, 'r', encoding) as file:
                content = file.read()
                return content
        except FileNotFoundError:
                print('文件搁哪儿呢？我没找到啊，看看文件路径有没有问题。')

    def json_read(self,json_path,encoding='utf-8'):
        try:
            with open(json_path, 'r', encoding) as file:
                data = json.load(file)
                print(data)
        except FileNotFoundError:
            print("文件搁哪儿呢？我没找到啊，看看文件路径有没有问题。")
        except json.JSONDecodeError:
            print("碰到无法解析的 JSON 数据了")
        except Exception as e:
            print(f"Oops!出错 {e}")

    def txt_tell(self,encoding='utf-8'):
        try:
            with open(self.txt_path, 'r', encoding) as file:
                position = file.tell()
                print(f'当前指针位置: {position}')
        except FileNotFoundError:
            print('文件搁哪儿呢？我没找到啊，看看文件路径有没有问题。')
        except Exception as e:
            print(f'Oops!出错 {e}')

    def txt_seek(self,seek,encoding='utf-8'):
        try:
            with open(self.txt_path, 'r+', encoding) as file:
                first_five_chars = file.read(seek)
                return first_five_chars
        except FileNotFoundError:
            print('文件搁哪儿呢？我没找到啊，看看文件路径有没有问题。')
        except Exception as e:
            print(f'Oops!出错 {e}')