import os
import re

class FileStructureGenerator:
    def __init__(self, base_output_dir="generated_files"):
        """
        初始化文件结构生成器。

        Args:
            base_output_dir (str): 生成文件的根目录。
        """
        self.base_output_dir = base_output_dir
        if not os.path.exists(self.base_output_dir):
            os.makedirs(self.base_output_dir)

    def extract_structure_from_llm_response(self, llm_response: str) -> dict:
        """
        从大模型回复中提取文件结构和内容。

        这个函数是关键，需要根据大模型回复的具体格式来实现解析逻辑。
        这是一个示例，假设大模型回复使用Markdown的代码块来表示文件和内容。

        Args:
            llm_response (str): 大模型的回复字符串。

        Returns:
            dict: 包含文件结构和内容的字典。
                  示例格式：
                  {
                      "path/to/directory/": {},
                      "path/to/file.py": "print('Hello, World!')",
                      "another_file.txt": "This is a text file."
                  }
                  对于空文件夹，值为一个空字典。
        """
        file_structure = {}
        current_file_path = None
        current_file_content = []

        # 寻找Markdown代码块
        code_blocks = re.findall(r"```(.*?)```", llm_response, re.DOTALL)

        for block in code_blocks:
            # 尝试识别文件路径标记，例如在代码块的第一行
            lines = block.strip().split('\n')
            if lines and lines[0].startswith("path:"):
                # 假设路径以 path: 开头，并去掉语言标记（例如 python）
                path_line = lines[0].strip()
                # 移除可能的语言标记，例如 ```python\npath: ...
                path_line = re.sub(r'^(\w+\n)?path:', '', path_line).strip()

                # 确保路径是相对路径或绝对路径，这里假设是相对路径到输出目录
                file_path = path_line.lstrip('/')  # 移除开头的斜杠
                current_file_path = file_path
                current_file_content = lines[1:] # 从第二行开始是内容
                file_structure[current_file_path] = "\n".join(current_file_content)
                current_file_path = None # 重置，准备下一个文件
                current_file_content = []
            elif current_file_path is not None:
                # 如果没有新的路径标记，且有当前文件路径，则认为是当前文件的内容
                current_file_content.extend(lines)
        
        # 处理没有明确标记路径，但可能出现在代码块中的内容（需要更复杂的逻辑）
        # 简单示例，这里假设如果一个代码块没有 path: 标记，它可能不是文件内容的一部分，
        # 或者需要更复杂的模式识别
        # 如果你的大模型有不同的表示方法，需要修改这里的解析逻辑。
        print(f"Parsed file structure: {file_structure}") # 调试输出
        return file_structure

    def generate_files_from_structure(self, file_structure: dict):
        """
        根据文件结构字典生成文件和文件夹。

        Args:
            file_structure (dict): 包含文件结构和内容的字典。
        """
        print(f"Generating files in: {self.base_output_dir}")
        for path, content in file_structure.items():
            full_path = os.path.join(self.base_output_dir, path)

            if isinstance(content, dict):  # 如果是字典，表示是一个目录
                print(f"Creating directory: {full_path}")
                os.makedirs(full_path, exist_ok=True)
                # 递归处理子目录，如果需要的话（当前示例结构是平坦的）
                # self.generate_files_from_structure(content) # 如果结构是嵌套的
            elif isinstance(content, str):  # 如果是字符串，表示一个文件
                print(f"Creating file: {full_path}")
                # 确保父目录存在
                parent_dir = os.path.dirname(full_path)
                if parent_dir:
                    os.makedirs(parent_dir, exist_ok=True)
                try:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except IOError as e:
                    print(f"Error writing file {full_path}: {e}")
            else:
                print(f"Warning: Skipping unknown type for path {path}: {type(content)}")

    def get_folder_structure_and_content(self, folder_path: str) -> dict:
        """
        获取指定文件夹的目录结构和 Python 文件的内容。
        过滤掉非 Python 文件。

        Args:
            folder_path (str): 要扫描的文件夹路径。

        Returns:
            dict: 包含目录结构和 Python 文件内容的字典。
                  示例格式：
                  {
                      "dir1/": {},
                      "dir1/file1.py": "print('Hello')",
                      "dir2/sub_dir/": {}, # 如果子目录只包含非Python文件，它仍然会被包含
                      "dir2/sub_dir/another_dir/": {} # 子目录下的子目录
                  }
                  空目录值为一个空字典。
        """
        folder_structure = {}
        print(f"Scanning folder: {folder_path}")

        if not os.path.isdir(folder_path):
            print(f"Error: Folder not found or not a directory: {folder_path}")
            return folder_structure

        for root, dirs, files in os.walk(folder_path):
            # 获取相对于输入文件夹的路径
            relative_root = os.path.relpath(root, folder_path)
            if relative_root == '.': # 处理根目录的相对路径
                relative_root = ''

            # 添加当前目录到结构（即使它是空的或只包含非py文件）
            if relative_root and not relative_root.startswith('.'): # 避免添加 '.' 和隐藏目录
                 folder_structure[relative_root + os.sep] = {}

            # 添加子目录到结构（确保它们不是隐藏目录）
            for d in dirs:
                 if not d.startswith('.'):
                     relative_dir_path = os.path.join(relative_root, d)
                     folder_structure[relative_dir_path + os.sep] = {}

            # 添加 Python 文件内容
            for file in files:
                if file.endswith(".py") and not file.startswith('.'): # 同时过滤隐藏的.py文件
                    full_file_path = os.path.join(root, file)
                    relative_file_path = os.path.join(relative_root, file)
                    try:
                        with open(full_file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        folder_structure[relative_file_path] = content
                        print(f"Read content from {relative_file_path}")
                    except IOError as e:
                        print(f"Error reading file {full_file_path}: {e}")
                        # 读取失败的 py 文件可以标记为None或者不添加，这里选择不添加
                        # folder_structure[relative_file_path] = None

        # 清理掉那些只包含了非.py文件的目录，如果需要的话。
        # 当前逻辑是保留所有目录，这通常在展示结构时更有用。
        # 如果你想只保留包含.py文件或子目录的目录，需要额外的清理步骤。

        print(f"Scanned folder structure (Python only): {folder_structure}")
        return folder_structure
    
    def format_structure_for_llm(self, structure: dict) -> str:
        """
        将包含目录结构和 Python 文件内容的字典转换为方便大模型理解的文本格式。
        跳过非 Python 文件（None值）。

        Args:
            structure (dict): 包含文件结构和内容的字典。

        Returns:
            str: 格式化后的文本字符串。
        """
        formatted_text = ""
        # 对路径进行排序
        sorted_paths = sorted(structure.keys())

        for path in sorted_paths:
            content = structure[path]

            if isinstance(content, dict): # 目录
                # 可以在这里选择是否只包含非空的目录（包含py文件或子目录的目录）
                # 当前逻辑是包含所有扫描到的目录
                formatted_text += f"```\npath: {path}\n# Directory\n```\n\n" # 标记目录更明确
            elif isinstance(content, str): # Python 文件内容
                formatted_text += f"```python\npath: {path}\n{content}\n```\n\n"
            # 过滤掉 content is None 的情况

        return formatted_text.strip()


